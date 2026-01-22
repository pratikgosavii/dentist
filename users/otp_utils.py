"""
OTP utility functions for sending and verifying OTP via msg.msgclub.net
"""
import random
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import OTP


def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_otp_via_msgclub(mobile, otp_code):
    """
    Send OTP via msg.msgclub.net API
    
    Args:
        mobile: Mobile number (10 digits, without country code)
        otp_code: The OTP code to send
        
    Returns:
        tuple: (success: bool, message: str)
    """
    api_url = getattr(settings, 'MSG_CLUB_API_URL', 'http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms')
    api_key = getattr(settings, 'MSG_CLUB_API_KEY', '')
    sender_id = getattr(settings, 'MSG_CLUB_SENDER_ID', 'TOOTHT')
    route_id = getattr(settings, 'MSG_CLUB_ROUTE_ID', '1')
    sms_content_type = getattr(settings, 'MSG_CLUB_SMS_CONTENT_TYPE', 'english')
    message_template = getattr(settings, 'OTP_MESSAGE_TEMPLATE', 'OTP {otp_code} to verify your dental record on ToothTrack. Track treatment, reports & get 24x7 dental support. Download ToothTrack App. SNEHAL DIGITAL VENTURES PRIVATE LIMITED')
    expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 5)
    
    if not api_key:
        return False, "MSG_CLUB_API_KEY not configured"
    
    # Format mobile number (keep as 10 digits, no country code needed)
    mobile = str(mobile).strip()
    # Remove country code if present
    if mobile.startswith('91') and len(mobile) == 12:
        mobile = mobile[2:]
    elif len(mobile) > 10:
        # Keep last 10 digits
        mobile = mobile[-10:]
    
    if len(mobile) != 10:
        return False, "Invalid mobile number. Must be 10 digits."
    
    # Prepare message using template
    message = message_template.format(
        otp_code=otp_code,
        expiry_minutes=expiry_minutes
    )
    
    # Prepare query parameters (msg.msgclub.net uses GET with query params)
    params = {
        'AUTH_KEY': api_key,
        'message': message,
        'senderId': sender_id,
        'routeId': route_id,
        'mobileNos': mobile,
        'smsContentType': sms_content_type
    }
    
    try:
        # msg.msgclub.net uses GET request with query parameters
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        # Try to parse JSON response
        try:
            result = response.json()
            # Check response code
            response_code = str(result.get('responseCode', ''))
            response_msg = result.get('response', '')
            
            # Handle authentication errors (3009 = Token Not Found)
            if response_code == '3009' or 'Token Not Found' in str(response_msg) or 'AUTH_KEY' in str(response_msg):
                return False, f"Authentication failed: {response_msg}"
            
            # Code 3001 with a long numeric value is a transaction ID (success)
            # Transaction IDs are typically long numbers (10+ digits)
            if response_code == '3001' or (response_code.isdigit() and len(response_code) > 10):
                return True, f"OTP sent successfully (Transaction ID: {response_code})"
            
            # Standard success code
            if response_code == '200':
                return True, "OTP sent successfully"
            
            # If response code is a long number (transaction ID), treat as success
            if response_code and response_code.isdigit() and len(response_code) >= 10:
                return True, f"OTP sent successfully (Transaction ID: {response_code})"
            
            # If HTTP status is 200 and we got a response, assume success
            # (msg.msgclub.net may return transaction IDs as responseCode)
            if response.status_code == 200:
                if response_code:
                    return True, f"OTP sent successfully (Code: {response_code})"
                else:
                    return True, "OTP sent successfully"
            
            # Only treat as error if we have a clear error code
            if response_code and response_code not in ['200', '3001']:
                return False, f"Failed to send OTP: {response_msg} (Code: {response_code})"
            else:
                return True, "OTP sent successfully"
                
        except ValueError:
            # If response is not JSON, check status code
            if response.status_code == 200:
                return True, "OTP sent successfully"
            else:
                return False, f"Failed to send OTP: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, f"Error sending OTP: {str(e)}"


def create_and_send_otp(mobile):
    """
    Create an OTP record and send it via SMS
    
    Args:
        mobile: Mobile number
        
    Returns:
        tuple: (otp_object: OTP, success: bool, message: str)
    """
    # Clean mobile number (remove +, spaces, etc.)
    mobile = ''.join(filter(str.isdigit, str(mobile)))
    
    # Generate OTP
    otp_code = generate_otp(getattr(settings, 'OTP_LENGTH', 6))
    
    # Delete any existing OTPs for this mobile
    OTP.objects.filter(mobile=mobile, is_verified=False).delete()
    
    # Create new OTP
    expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 5)
    expires_at = timezone.now() + timedelta(minutes=expiry_minutes)
    
    otp_obj = OTP.objects.create(
        mobile=mobile,
        otp_code=otp_code,
        expires_at=expires_at
    )
    
    # Send OTP via SMS
    success, message = send_otp_via_msgclub(mobile, otp_code)
    
    if not success:
        # If sending fails, delete the OTP record
        otp_obj.delete()
        return None, False, message
    
    return otp_obj, True, message


def verify_otp(mobile, otp_code):
    """
    Verify OTP code for a mobile number
    
    Args:
        mobile: Mobile number
        otp_code: OTP code to verify
        
    Returns:
        tuple: (otp_object: OTP or None, is_valid: bool, message: str)
    """
    # Clean mobile number
    mobile = ''.join(filter(str.isdigit, str(mobile)))
    
    # Find the most recent unverified OTP for this mobile
    otp_obj = OTP.objects.filter(
        mobile=mobile,
        otp_code=otp_code,
        is_verified=False
    ).order_by('-created_at').first()
    
    if not otp_obj:
        return None, False, "Invalid OTP code"
    
    # Check if OTP has expired
    if timezone.now() > otp_obj.expires_at:
        otp_obj.delete()
        return None, False, "OTP has expired. Please request a new one."
    
    # Mark OTP as verified
    otp_obj.is_verified = True
    otp_obj.verified_at = timezone.now()
    otp_obj.save()
    
    # Delete all other unverified OTPs for this mobile
    OTP.objects.filter(mobile=mobile, is_verified=False).exclude(id=otp_obj.id).delete()
    
    return otp_obj, True, "OTP verified successfully"
