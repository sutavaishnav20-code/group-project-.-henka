# Henka Authentication System Setup

## Overview

This document explains the new authentication system added to Henka, including email login/signup and Google OAuth integration.

## Features Implemented

### 1. **Email-Based Authentication**

- **Signup**: Create an account with email, name, and preferred language
- **Login**: Sign in with email address
- Automatic user profile creation and token generation

### 2. **Google OAuth 2.0 Integration**

- One-click "Continue with Google" button
- Automatic account creation for new Google users
- Account linking for existing users

### 3. **Multi-Language Support**

- Users can select preferred language during signup/login:
  - English
  - हिन्दी (Hindi)
  - मराठी (Marathi)
  - ગુજરાતી (Gujarati)
  - ಕನ್ನಡ (Kannada)
  - தமிழ் (Tamil)

### 4. **User Profile Management**

- User profile bar displays at top of app after login
- Shows user name, language, and logout button
- Persistent login using JWT tokens (7-day expiry)

---

## Backend API Endpoints

All endpoints are available at `http://localhost:3000/api/auth/`

### 1. **POST /signup**

Creates a new user account.

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "language": "English"
}
```

**Response**: 201 Created

```json
{
  "success": true,
  "message": "Account created successfully!",
  "token": "eyJhbGc...",
  "user": {
    "id": "user_1726...",
    "email": "user@example.com",
    "name": "John Doe",
    "language": "English"
  }
}
```

### 2. **POST /login**

Logs in an existing user.

```json
{
  "email": "user@example.com",
  "language": "English"
}
```

**Response**: 200 OK

```json
{
  "success": true,
  "message": "Login successful!",
  "token": "eyJhbGc...",
  "user": { ... }
}
```

### 3. **POST /google**

Handles Google OAuth callback.

```json
{
  "googleId": "google_oauth_id",
  "email": "user@gmail.com",
  "name": "Jane Doe",
  "language": "English"
}
```

**Response**: 200 OK

```json
{
  "success": true,
  "message": "Google authentication successful!",
  "token": "eyJhbGc...",
  "user": { ... }
}
```

### 4. **GET /me** (Protected)

Retrieve current user profile.
**Headers**: `Authorization: Bearer {token}`
**Response**: 200 OK

```json
{
  "user": { ... }
}
```

### 5. **PATCH /me** (Protected)

Update user profile.

```json
{
  "name": "Updated Name",
  "language": "Hindi"
}
```

**Response**: 200 OK

### 6. **POST /logout**

Logout (clears client-side token).
**Response**: 200 OK

### 7. **GET /languages**

Get list of available languages.
**Response**: 200 OK

```json
{
  "languages": ["English", "Hindi", "Marathi", "Gujarati", "Kannada", "Tamil"]
}
```

---

## Frontend Implementation

### 1. **Authentication Flow**

#### On Page Load:

- Check for stored JWT token in `localStorage`
- If token exists and user is authenticated:
  - Hide auth modal
  - Show user profile bar
  - Load app normally
- If no token:
  - Show auth modal (login/signup forms)

#### Login Flow:

```
User enters email → Validate format → Send to /api/auth/login
→ Backend returns token + user data
→ Store in localStorage
→ Hide modal → Show profile bar
```

#### Signup Flow:

```
User enters name, email, language → Validate
→ Send to /api/auth/signup
→ Backend creates user, returns token
→ Store in localStorage
→ Hide modal → Show profile bar
```

#### Google OAuth Flow:

```
User clicks "Continue with Google"
→ Google Sign-In button loads (google.accounts.id)
→ User authenticates with Google
→ JWT credential returned
→ Decode JWT, extract googleId, email, name
→ Send to /api/auth/google
→ Backend creates or links account
→ Store token → Show profile bar
```

### 2. **Token Management**

- JWT tokens stored in `localStorage` as `henka_auth_token`
- User data stored as `henka_user` (JSON)
- Tokens expire after 7 days
- `fetchWithAuth()` helper automatically adds token to API requests

### 3. **Protected API Calls**

```javascript
// Example: Fetch mentor data with authentication
const response = await fetchWithAuth("/api/mentors");
```

---

## Configuration

### Google OAuth Client ID

To enable Google Sign-In, you must:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Google+ API"
4. Create "OAuth 2.0 Client ID" (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:3000`
   - `http://your-domain.com`
6. Copy the Client ID and update in `index.html`:
   ```javascript
   google.accounts.id.initialize({
     client_id: "YOUR_CLIENT_ID_HERE",
     callback: handleGoogleCallback,
   });
   ```

### JWT Secret

The JWT secret is set via environment variable or defaults to development secret:

```bash
export JWT_SECRET="your_production_secret_key"
node server.js
```

---

## Testing the Auth System

### Test Email Signup:

1. Open http://localhost:3000
2. Click "Sign up" tab
3. Enter: Name, Email, Language
4. Click "Create Account"
5. Should see user profile bar with name and language

### Test Email Login:

1. Logout (click logout button)
2. On login form, enter email from signup
3. Select same language
4. Click "Login"
5. Should log in successfully

### Test Google OAuth:

1. Click "Continue with Google" button
2. Select Google account
3. Should automatically create account and log in

### Test Language Persistence:

1. Sign up with "हिन्दी (Hindi)" language
2. Logout and login again
3. Profile bar should show "Hindi"

---

## Integration with Existing App

### Accessing User Data

```javascript
// Get current authenticated user
const user = AUTH_STATE.user;
console.log(user.name, user.email, user.language);

// Check if user is logged in
if (AUTH_STATE.isAuthenticated) {
  // Load user-specific data
}
```

### Protected Routes

Update existing API calls to include authentication:

```javascript
// Before
const mentors = await (await fetch("/api/mentors")).json();

// After
const response = await fetchWithAuth("/api/mentors");
const mentors = await response.json();
```

### Display User-Specific Content

```javascript
if (AUTH_STATE.user) {
  document.querySelector("#greeting").textContent =
    `Welcome, ${AUTH_STATE.user.name}!`;
}
```

---

## Troubleshooting

### "Google Sign-In not loaded"

- Check that Google Script tag is in `<head>`:
  ```html
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  ```

### Token not persisting

- Check browser's localStorage permissions
- Verify token is being saved: `localStorage.getItem('henka_auth_token')`

### CORS errors with Google

- Ensure `http://localhost:3000` is in Google Cloud Console authorized origins

### User not found on login

- Check email spelling matches signup email exactly (case-insensitive but must match)
- Create new account with correct email

---

## Security Notes

⚠️ **Development Setup**: JWT verification is simplified for demo purposes

- For production, use `jsonwebtoken` package (already in dependencies)
- Implement password hashing with bcrypt
- Use HTTPS only
- Store JWT_SECRET securely in environment variables
- Add rate limiting for auth endpoints
- Implement CSRF protection

---

## Next Steps

1. **Set up Google OAuth Client ID** (required for Google button to work)
2. **Install dependencies**: `npm install`
3. **Start server**: `npm run dev`
4. **Test auth flows** as documented above
5. **Integrate user data** with existing app features

---

For questions or issues, check the browser console for detailed error messages.
