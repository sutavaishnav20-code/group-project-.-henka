# Henka Auth - Code Integration Examples

This file provides copy-paste ready code examples for common authentication integration patterns.

---

## 1. Check if User is Logged In

```javascript
// Simple check
if (AUTH_STATE.isAuthenticated) {
  console.log("User is logged in");
  console.log("User name:", AUTH_STATE.user.name);
} else {
  console.log("User not authenticated");
}

// Show/hide elements based on auth
if (AUTH_STATE.user) {
  document.getElementById("protected-content").style.display = "block";
  document.getElementById("login-prompt").style.display = "none";
} else {
  document.getElementById("protected-content").style.display = "none";
  document.getElementById("login-prompt").style.display = "block";
}
```

---

## 2. Get Current User Info

```javascript
// Get all user data
const currentUser = AUTH_STATE.user;
console.log("User:", currentUser);
// Output: { id, email, name, language }

// Access individual properties
const userName = AUTH_STATE.user.name; // e.g., "John Doe"
const userEmail = AUTH_STATE.user.email; // e.g., "john@example.com"
const userLanguage = AUTH_STATE.user.language; // e.g., "English"
const userId = AUTH_STATE.user.id; // e.g., "user_1726..."

// Display in DOM
document.getElementById("greeting").textContent = `Welcome, ${userName}!`;
document.getElementById("user-email").textContent = userEmail;
```

---

## 3. Make Protected API Calls

```javascript
// Method 1: Using fetchWithAuth helper (RECOMMENDED)
async function getProtectedData() {
  try {
    const response = await fetchWithAuth("/api/mentors");
    const data = await response.json();
    console.log("Mentors:", data);
  } catch (error) {
    console.error("Error fetching mentors:", error);
  }
}

// Method 2: Manual authorization header
async function getProtectedDataManual() {
  const response = await fetch("/api/mentors", {
    headers: {
      Authorization: `Bearer ${AUTH_STATE.token}`,
    },
  });
  const data = await response.json();
  return data;
}

// Method 3: With error handling for expired token
async function getProtectedDataWithRefresh() {
  try {
    const response = await fetchWithAuth("/api/mentors");

    if (response.status === 401) {
      // Token expired - logout user
      handleLogout();
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to fetch protected data:", error);
    return null;
  }
}
```

---

## 4. Display User Profile

```javascript
// Simple profile card
function displayUserProfile() {
  if (!AUTH_STATE.user) return;

  const html = `
    <div class="profile-card">
      <div class="avatar">${AUTH_STATE.user.name.charAt(0).toUpperCase()}</div>
      <h3>${AUTH_STATE.user.name}</h3>
      <p>${AUTH_STATE.user.email}</p>
      <p>Language: ${AUTH_STATE.user.language}</p>
    </div>
  `;

  document.getElementById("profile-container").innerHTML = html;
}

// Call on page load
if (AUTH_STATE.isAuthenticated) {
  displayUserProfile();
}
```

---

## 5. Load User-Specific Data

```javascript
// Load user preferences
async function loadUserPreferences() {
  if (!AUTH_STATE.user) return;

  const response = await fetchWithAuth("/api/user/preferences");
  const prefs = await response.json();

  // Apply user's language
  setAppLanguage(AUTH_STATE.user.language);

  // Load user's data
  console.log("Preferences:", prefs);
  return prefs;
}

// Call when user logs in
document.addEventListener("DOMContentLoaded", () => {
  initAuthUI();
  if (AUTH_STATE.isAuthenticated) {
    loadUserPreferences();
  }
});
```

---

## 6. Update User Profile

```javascript
// Change language
async function changeLanguage(newLanguage) {
  try {
    const response = await fetchWithAuth("/api/auth/me", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language: newLanguage }),
    });

    const data = await response.json();

    if (response.ok) {
      // Update local state
      AUTH_STATE.user = data.user;
      localStorage.setItem("henka_user", JSON.stringify(data.user));

      console.log("Language updated to:", newLanguage);
      return true;
    } else {
      console.error("Failed to update language:", data.error);
      return false;
    }
  } catch (error) {
    console.error("Error updating language:", error);
    return false;
  }
}

// Change name
async function changeName(newName) {
  try {
    const response = await fetchWithAuth("/api/auth/me", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName }),
    });

    const data = await response.json();

    if (response.ok) {
      AUTH_STATE.user = data.user;
      localStorage.setItem("henka_user", JSON.stringify(data.user));
      console.log("Name updated to:", newName);
      return true;
    }
  } catch (error) {
    console.error("Error updating name:", error);
    return false;
  }
}

// Usage example
changeName("Jane Doe").then((success) => {
  if (success) {
    console.log("Profile updated!");
  }
});
```

---

## 7. Handle Post-Login Actions

```javascript
// Custom initialization after login
function onUserLoggedIn() {
  // Called after successful login/signup
  console.log("User logged in:", AUTH_STATE.user.name);

  // Load user-specific data
  loadUserPreferences();

  // Show personalized content
  document.getElementById("welcome-section").innerHTML =
    `Welcome back, ${AUTH_STATE.user.name}!`;

  // Initialize user-specific features
  initializeUserDashboard();

  // Track login event
  trackEvent("user_login", {
    userId: AUTH_STATE.user.id,
    language: AUTH_STATE.user.language,
  });
}

// Hook into successful login
// (Add this to handleLogin or handleSignup functions)
```

---

## 8. Logout and Cleanup

```javascript
// Enhanced logout with cleanup
async function handleLogoutWithCleanup() {
  if (confirm("Are you sure you want to logout?")) {
    // Call logout endpoint (optional)
    try {
      await fetch(`${API_BASE}/api/auth/logout`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${AUTH_STATE.token}`,
        },
      });
    } catch (error) {
      console.warn("Error calling logout endpoint:", error);
    }

    // Clear all auth state
    localStorage.removeItem("henka_auth_token");
    localStorage.removeItem("henka_user");
    AUTH_STATE.token = null;
    AUTH_STATE.user = null;
    AUTH_STATE.isAuthenticated = false;

    // Clear user-specific data from app
    clearUserData();

    // Reset UI
    document.getElementById("userProfileBar").style.display = "none";
    showAuthOverlay();

    // Clear forms
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("loginEmail").value = "";

    console.log("Logged out successfully");
    showSuccess("See you next time! 👋");
  }
}

// Function to clear user-specific data
function clearUserData() {
  // Clear any user-specific caches
  sessionStorage.clear();

  // Clear user preferences from DOM
  const userElements = document.querySelectorAll("[data-user-specific]");
  userElements.forEach((el) => (el.innerHTML = ""));

  // Stop any user-specific websocket connections
  // if (userWebSocket) userWebSocket.close();
}
```

---

## 9. Protect Specific Routes/Features

```javascript
// Check auth before accessing protected feature
function accessMentorBooking() {
  if (!AUTH_STATE.isAuthenticated) {
    showAuthOverlay();
    showError("Please login to book a mentor session");
    return false;
  }

  // User is authenticated, proceed
  openMentorBookingModal();
  return true;
}

// Wrap button onclick
<button onclick="if (accessMentorBooking()) { /* proceed */ }">
  Book Mentor
</button>;

// Or use middleware pattern
async function withAuth(callback) {
  if (!AUTH_STATE.isAuthenticated) {
    showAuthOverlay();
    return;
  }
  await callback();
}

// Usage
withAuth(async () => {
  const mentors = await (await fetchWithAuth("/api/mentors")).json();
  displayMentors(mentors);
});
```

---

## 10. Language-Dependent Conditionals

```javascript
// Load content based on user's language
function loadLanguageSpecificContent() {
  const lang = AUTH_STATE.user?.language || "English";

  const translations = {
    English: {
      greeting: "Welcome to Henka",
      logout: "Logout",
      mentors: "Mentors",
    },
    Hindi: {
      greeting: "Henka में स्वागत है",
      logout: "लॉग आउट",
      mentors: "सलाहकार",
    },
    Marathi: {
      greeting: "Henka मध्ये स्वागतम्",
      logout: "लॉग आउट",
      mentors: "सल्लागार",
    },
  };

  const strings = translations[lang] || translations.English;

  // Apply translations to DOM
  document.getElementById("greeting").textContent = strings.greeting;
  document.getElementById("logout-btn").textContent = strings.logout;

  return strings;
}

// Call after user logs in
if (AUTH_STATE.isAuthenticated) {
  loadLanguageSpecificContent();
}
```

---

## 11. Sync Auth State Across Tabs/Windows

```javascript
// Listen for storage changes (triggered when logged in from another tab)
window.addEventListener("storage", (event) => {
  if (event.key === "henka_auth_token") {
    // Token changed in another tab
    if (event.newValue && !event.oldValue) {
      // User logged in elsewhere - refresh this page
      console.log("User logged in from another tab");
      window.location.reload();
    } else if (!event.newValue && event.oldValue) {
      // User logged out elsewhere - logout here too
      console.log("User logged out from another tab");
      handleLogout();
    }
  }
});

// Update auth state from storage
function syncAuthState() {
  const token = localStorage.getItem("henka_auth_token");
  const user = JSON.parse(localStorage.getItem("henka_user") || "null");

  AUTH_STATE.token = token;
  AUTH_STATE.user = user;
  AUTH_STATE.isAuthenticated = !!token;
}
```

---

## 12. Debug Authentication

```javascript
// Log current auth state
function debugAuth() {
  console.log("=== Henka Auth Debug ===");
  console.log("Is Authenticated:", AUTH_STATE.isAuthenticated);
  console.log(
    "Token:",
    AUTH_STATE.token ? AUTH_STATE.token.substring(0, 20) + "..." : "None",
  );
  console.log("User:", AUTH_STATE.user);
  console.log(
    "Stored Token:",
    localStorage.getItem("henka_auth_token") ? "Yes" : "No",
  );
  console.log(
    "Stored User:",
    localStorage.getItem("henka_user") ? "Yes" : "No",
  );
}

// Decode JWT payload (for debugging)
function decodeJWT(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join(""),
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

// Usage in browser console
debugAuth();
console.log("JWT Payload:", decodeJWT(AUTH_STATE.token));
```

---

## 13. Session Timeout

```javascript
// Auto-logout after inactivity
class SessionManager {
  constructor(timeoutMinutes = 30) {
    this.timeoutMinutes = timeoutMinutes;
    this.timeoutId = null;
    this.startTimer();
    this.attachListeners();
  }

  startTimer() {
    this.clearTimer();
    this.timeoutId = setTimeout(
      () => {
        console.log("Session expired due to inactivity");
        handleLogout();
      },
      this.timeoutMinutes * 60 * 1000,
    );
  }

  clearTimer() {
    if (this.timeoutId) clearTimeout(this.timeoutId);
  }

  attachListeners() {
    // Reset timer on user activity
    ["mousedown", "keydown", "scroll", "touchstart"].forEach((event) => {
      document.addEventListener(event, () => {
        if (AUTH_STATE.isAuthenticated) {
          this.startTimer();
        }
      });
    });
  }

  destroy() {
    this.clearTimer();
  }
}

// Initialize session manager when user logs in
if (AUTH_STATE.isAuthenticated) {
  const sessionManager = new SessionManager(30); // 30 minute timeout
}
```

---

## 14. Error Recovery

```javascript
// Handle network errors gracefully
async function fetchWithErrorRecovery(endpoint, options = {}) {
  const maxRetries = 3;
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const response = await fetchWithAuth(endpoint, options);

      if (response.status === 401) {
        // Token expired
        console.log("Token expired, attempting to refresh...");
        handleLogout();
        return null;
      }

      return response;
    } catch (error) {
      retries++;
      if (retries >= maxRetries) {
        console.error("Failed after", maxRetries, "attempts");
        showError("Network error. Please try again.");
        throw error;
      }

      // Wait before retrying
      await new Promise((resolve) => setTimeout(resolve, 1000 * retries));
    }
  }
}

// Usage
try {
  const response = await fetchWithErrorRecovery("/api/mentors");
  const data = await response.json();
} catch (error) {
  console.error("Final error:", error);
}
```

---

## 15. Complete App Initialization Example

```javascript
// Initialize app when page loads
document.addEventListener("DOMContentLoaded", async () => {
  console.log("Initializing Henka app...");

  // 1. Check auth state
  initAuthUI();

  // 2. If user is authenticated
  if (AUTH_STATE.isAuthenticated && AUTH_STATE.user) {
    console.log("User authenticated:", AUTH_STATE.user.name);

    // 3. Load user preferences
    try {
      const response = await fetchWithAuth("/api/mentors");
      const mentorData = await response.json();
      displayMentors(mentorData);
    } catch (error) {
      console.error("Failed to load mentors:", error);
    }

    // 4. Start session manager
    const sessionManager = new SessionManager(30);

    // 5. Initialize app-specific features
    initializeFitnessTracker();
    initializeMentalHealthModule();
    initializeDietTracker();

    console.log("App initialized successfully");
  } else {
    // 6. Show auth modal if not authenticated
    console.log("Waiting for authentication...");
  }
});
```

---

## Tips & Best Practices

✅ **DO:**

- Always check `AUTH_STATE.isAuthenticated` before accessing protected features
- Use `fetchWithAuth()` for all API calls that need authentication
- Store sensitive tokens in browser storage (handled automatically)
- Logout users after extended inactivity
- Provide clear feedback (success/error messages)

❌ **DON'T:**

- Don't expose tokens in URL or logs
- Don't make assumptions about user data - always check if authenticated
- Don't cache user data longer than needed
- Don't forget to refresh UI after logout
- Don't bypass auth checks for "convenience"

---

**More examples?** Check AUTH_SETUP.md and AUTH_CHECKLIST.md for comprehensive documentation!
