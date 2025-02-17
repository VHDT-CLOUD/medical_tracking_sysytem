document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            fetch("/login/", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Login failed: " + data.error);
                } else {
                    window.location.href = "/dashboard/";
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function() {
            fetch("/logout/")
                .then(() => window.location.href = "/");
        });
    }
});

function requestOTP() {
    let aadhaarNumber = document.getElementById("aadhaar").value;

    fetch("/api/request-otp/", {
        method: "POST",
        body: new URLSearchParams({ "aadhaar_number": aadhaarNumber }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => alert(data.message + " OTP: " + data.otp)) // Show OTP for testing
    .catch(error => console.error("Error:", error));
}

function verifyOTP() {
    let aadhaarNumber = document.getElementById("aadhaar").value;
    let otp = document.getElementById("otp").value;

    fetch("/api/verify-otp/", {
        method: "POST",
        body: new URLSearchParams({ "aadhaar_number": aadhaarNumber, "otp": otp }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error:", error));
}