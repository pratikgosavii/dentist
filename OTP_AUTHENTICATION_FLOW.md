# OTP-Based Authentication Flow Documentation

## Overview
We have replaced Firebase authentication with OTP-based authentication using msg.msgclub.net SMS service.

---

## 🔄 Complete Authentication Flow

### **Flow 1: User Login (Existing User)**

#### Step 1: Send OTP
**Endpoint:** `POST /users/send-otp/`

**Request:**
```json
{
    "mobile": "9876543210"
}
```

**Response (Success):**
```json
{
    "message": "OTP sent successfully",
    "mobile": "9876543210"
}
```

**Response (Error):**
```json
{
    "error": "Invalid mobile number"
}
```

#### Step 2: Verify OTP & Login
**Endpoint:** `POST /users/login/`

**Request:**
```json
{
    "mobile": "9876543210",
    "otp": "123456",
    "user_type": "doctor"  // Optional: "doctor" or "customer"
}
```

**Response (Success):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "mobile": "9876543210",
        "role": "doctor"
    },
    "created": false,
    "is_subscribed": true,
    "user_details": {
        "id": 1,
        "mobile": "9876543210",
        "first_name": "John",
        "email": "john@example.com",
        ...
    }
}
```

**Response (Error):**
```json
{
    "error": "Invalid OTP code"
}
```
or
```json
{
    "error": "OTP has expired. Please request a new one."
}
```

---

### **Flow 2: User Signup (New User)**

#### Step 1: Send OTP
**Endpoint:** `POST /users/send-otp/`

**Request:**
```json
{
    "mobile": "9876543210"
}
```

**Response:** Same as Login Step 1

#### Step 2: Verify OTP & Signup
**Endpoint:** `POST /users/signup/`

**Request:**
```json
{
    "mobile": "9876543210",
    "otp": "123456",
    "user_type": "doctor",  // Required: "doctor" or "customer"
    "city": 1,              // Required: City ID
    "area": 1,              // Required: Area ID
    "name": "John Doe",     // Optional
    "email": "john@example.com"  // Optional
}
```

**Response (Success):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "mobile": "9876543210",
        "email": "john@example.com",
        "name": "John Doe",
        "city": "Mumbai",
        "area": "Andheri",
        "user_type": "doctor",
        "created": true
    }
}
```

**Response (Error):**
```json
{
    "error": "Mobile, OTP, user_type, city, and area are required"
}
```
or
```json
{
    "error": "This number is already registered as a customer. Cannot register again as doctor."
}
```

---

### **Flow 3: Password Reset**

#### Step 1: Send OTP
**Endpoint:** `POST /users/send-otp/`

**Request:**
```json
{
    "mobile": "9876543210"
}
```

#### Step 2: Verify OTP & Reset Password
**Endpoint:** `POST /users/reset-password/`

**Request:**
```json
{
    "mobile": "9876543210",
    "otp": "123456",
    "new_password": "newSecurePassword123"
}
```

**Response (Success):**
```json
{
    "message": "Password updated successfully."
}
```

---

### **Flow 4: Doctor Verifies Customer (Doctor Only)**

This is used when a doctor wants to register a customer directly.

#### Step 1: Send OTP to Customer's Mobile
**Endpoint:** `POST /users/send-otp/`

**Request:**
```json
{
    "mobile": "9876543210"
}
```

#### Step 2: Doctor Verifies Customer OTP
**Endpoint:** `POST /doctor/verify-customer-otp/`

**Headers:**
```
Authorization: Bearer <doctor_access_token>
```

**Request:**
```json
{
    "mobile": "9876543210",
    "otp": "123456",
    "first_name": "Jane",      // Optional
    "last_name": "Doe",         // Optional
    "dob": "1990-01-01",        // Optional: YYYY-MM-DD
    "gender": "female"           // Optional: "male" or "female"
}
```

**Response (Success):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 2,
        "mobile": "9876543210",
        "first_name": "Jane",
        "last_name": "Doe",
        "dob": "1990-01-01",
        "gender": "female",
        "customer_id": 1,
        "created_by_doctor": 1
    }
}
```

---

## 📋 API Endpoints Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/users/send-otp/` | POST | Send OTP to mobile number | No |
| `/users/verify-otp/` | POST | Verify OTP and get basic JWT tokens | No |
| `/users/login/` | POST | Login with OTP (full user details) | No |
| `/users/signup/` | POST | Signup with OTP | No |
| `/users/reset-password/` | POST | Reset password with OTP | No |
| `/doctor/verify-customer-otp/` | POST | Doctor verifies customer OTP | Yes (Doctor) |

---

## 🔑 Key Points

### **OTP Validity**
- OTP expires after **5 minutes** (configurable in `settings.py`)
- OTP is **6 digits** (configurable in `settings.py`)
- Each mobile number can have only **one active unverified OTP** at a time
- Once verified, OTP cannot be reused

### **Mobile Number Format**
- Accepts any format: `"9876543210"`, `"+91 9876543210"`, `"98765 43210"`
- Automatically cleaned to digits only
- For SMS sending, automatically adds `91` country code if not present

### **JWT Tokens**
- After successful OTP verification, you receive:
  - `access`: Access token (valid for 30 days)
  - `refresh`: Refresh token (valid for 60 days)
- Use `access` token in `Authorization: Bearer <token>` header for protected endpoints

### **Error Handling**
Common error responses:
- `400 Bad Request`: Missing required fields, invalid OTP, expired OTP
- `403 Forbidden`: Unauthorized access (e.g., non-doctor trying doctor endpoint)
- `404 Not Found`: User not found

---

## 🔄 Migration from Firebase

### **Old Flow (Firebase):**
1. Frontend gets Firebase ID token from Firebase Auth
2. Send `idToken` to `/users/login/` or `/users/signup/`
3. Backend verifies token with Firebase

### **New Flow (OTP):**
1. Frontend calls `/users/send-otp/` with mobile number
2. User receives OTP via SMS
3. Frontend sends mobile + OTP to `/users/login/` or `/users/signup/`
4. Backend verifies OTP and generates JWT tokens

---

## 🛠️ Configuration

All configuration is in `dentist/settings.py`:

```python
MSG_CLUB_API_URL = "https://msg.msgclub.net/rest/sms/json"
MSG_CLUB_API_KEY = "your_api_key_here"
MSG_CLUB_SENDER_ID = "DEMOOS"
OTP_EXPIRY_MINUTES = 5
OTP_LENGTH = 6
```

---

## 📱 Frontend Integration Example

### **Login Flow:**
```javascript
// Step 1: Send OTP
const sendOTP = async (mobile) => {
    const response = await fetch('/users/send-otp/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile })
    });
    return response.json();
};

// Step 2: Verify OTP and Login
const login = async (mobile, otp, userType) => {
    const response = await fetch('/users/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            mobile, 
            otp, 
            user_type: userType 
        })
    });
    const data = await response.json();
    
    if (response.ok) {
        // Store tokens
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        // Use access_token in subsequent API calls
    }
    return data;
};
```

---

## ✅ Testing Checklist

1. ✅ Send OTP to valid mobile number
2. ✅ Verify OTP with correct code
3. ✅ Verify OTP with incorrect code (should fail)
4. ✅ Verify expired OTP (wait 5+ minutes)
5. ✅ Login with verified OTP
6. ✅ Signup with verified OTP
7. ✅ Reset password with verified OTP
8. ✅ Doctor verify customer OTP (with doctor token)

---

## 🚨 Important Notes

1. **OTP is single-use**: Once verified, it cannot be used again
2. **Rate Limiting**: Consider adding rate limiting to prevent OTP spam
3. **Security**: Never expose OTP in logs or error messages
4. **SMS Delivery**: If SMS fails to send, OTP record is deleted
5. **Mobile Validation**: Currently accepts any 10+ digit number, consider adding validation

---

## 📞 Support

If you encounter issues:
1. Check `MSG_CLUB_API_KEY` is set correctly in `settings.py`
2. Verify SMS service is working (check msg.msgclub.net dashboard)
3. Check Django logs for error messages
4. Verify OTP table exists in database (run migrations)
