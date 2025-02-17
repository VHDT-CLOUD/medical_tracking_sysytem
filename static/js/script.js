// Toggle form based on role selection
function toggleForm() {
    let role = document.getElementById("role").value;
    document.getElementById("patient-form").style.display = (role === "patient") ? "block" : "none";
    document.getElementById("doctor-form").style.display = (role === "doctor") ? "block" : "none";
}

// Send OTP (for patients)
function sendOTP() {
    alert("OTP sent to phone number");
    document.getElementById("otp-section").style.display = "block";
}

// Verify OTP (for patients)
function verifyOTP() {
    alert("OTP verified! Proceeding to next step.");
}

// Register Doctor
function registerDoctor() {
    alert("Doctor Registration submitted. Waiting for admin approval.");
}

// Login Function
function login() {
    let loginId = document.getElementById("login_id").value;
    let password = document.getElementById("password").value;

    if (loginId && password) {
        localStorage.setItem("user", loginId);
        window.location.href = "/dashboard/";  // Corrected redirection
    } else {
        alert("Please enter valid credentials");
    }
}

// Logout Function
function logout() {
    localStorage.removeItem("user");
    window.location.href = "/login/";  // Corrected redirection
}

// Set User Name in Dashboard
window.onload = function() {
    let user = localStorage.getItem("user");
    if (document.getElementById("user-name")) {
        document.getElementById("user-name").innerText = user || "Guest";
    }
};