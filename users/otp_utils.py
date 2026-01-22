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
    api_url = getattr(settings, 'MSG_CLUB_API_URL', 'https://msg.msgclub.net/rest/sms/json')
    api_key = getattr(settings, 'MSG_CLUB_API_KEY', '')
    sender_id = getattr(settings, 'MSG_CLUB_SENDER_ID', 'DENTAL')
    
    if not api_key:
        return False, "MSG_CLUB_API_KEY not configured"
    
    # Format mobile number (ensure it's 10 digits)
    mobile = str(mobile).strip()
    if len(mobile) == 10:
        mobile = f"91{mobile}"  # Add country code for India
    elif not mobile.startswith('91'):
        mobile = f"91{mobile}"
    
    # Prepare message
    message = f"Your OTP for Dental App login is {otp_code}. Valid for 5 minutes. Do not share this OTP with anyone."
    
    # Prepare payload
    payload = {
        'apikey': api_key,
        'sender': sender_id,
        'numbers': mobile,
        'message': message
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Check if SMS was sent successfully
        # msg.msgclub.net typically returns success in 'type' field
        if response.status_code == 200:
            return True, "OTP sent successfully"
        else:
            return False, f"Failed to send OTP: {result.get('message', 'Unknown error')}"
            
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
