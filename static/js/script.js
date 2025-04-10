document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function (event) {
            let inputs = form.querySelectorAll("input");
            for (let input of inputs) {
                // Skip hidden inputs and inputs with type submit
                if (input.type === 'hidden' || input.type === 'submit') {
                    continue;
                }
                if (input.value.trim() === "" && !input.hasAttribute('optional')) {
                    alert("Please fill in all required fields.");
                    event.preventDefault();
                    return;
                }
            }
        });
    }
});

// Function to show status messages
function showStatus(message, type) {
    console.log(`Status (${type}): ${message}`);

    // Create or get status container
    let statusContainer = document.getElementById('status_container');
    if (!statusContainer) {
        statusContainer = document.createElement('div');
        statusContainer.id = 'status_container';
        statusContainer.style.position = 'fixed';
        statusContainer.style.bottom = '20px';
        statusContainer.style.right = '20px';
        statusContainer.style.zIndex = '1000';
        document.body.appendChild(statusContainer);
    }

    // Create status message element
    const statusElement = document.createElement('div');
    statusElement.textContent = message;
    statusElement.style.padding = '10px 15px';
    statusElement.style.marginTop = '10px';
    statusElement.style.borderRadius = '4px';
    statusElement.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';

    // Set color based on type
    if (type === 'error') {
        statusElement.style.backgroundColor = '#f8d7da';
        statusElement.style.color = '#721c24';
    } else if (type === 'success') {
        statusElement.style.backgroundColor = '#d4edda';
        statusElement.style.color = '#155724';
    } else if (type === 'info') {
        statusElement.style.backgroundColor = '#d1ecf1';
        statusElement.style.color = '#0c5460';
    } else {
        statusElement.style.backgroundColor = '#e2e3e5';
        statusElement.style.color = '#383d41';
    }

    // Add to container
    statusContainer.appendChild(statusElement);

    // Remove after 5 seconds
    setTimeout(() => {
        statusElement.style.opacity = '0';
        statusElement.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            statusContainer.removeChild(statusElement);
        }, 500);
    }, 5000);
}

function fetchWithCSRF(url, options = {}) {
    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        console.error("CSRF token not found.");
        alert("An error occurred. Please refresh the page and try again.");
        return Promise.reject("CSRF token missing");
    }

    options.headers = {
        ...options.headers,
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || "An error occurred");
                });
            }
            return response.json();
        })
        .catch(error => {
            console.error("Error:", error.message);
            alert(error.message || "An error occurred. Please try again.");
            throw error;
        });
}

function requestOTP() {
    const aadhaarNumber = document.getElementById("aadhaar").value;

    // Validate Aadhaar number format (12 digits)
    if (!aadhaarNumber || !/^\d{12}$/.test(aadhaarNumber)) {
        alert("Please enter a valid 12-digit Aadhaar number.");
        return;
    }

    const sendOTPButton = document.getElementById("send_otp_btn");
    sendOTPButton.disabled = true;
    sendOTPButton.textContent = "Sending...";

    fetchWithCSRF('/accounts/aadhaar_verification/', {
        method: 'POST',
        body: JSON.stringify({ aadhaar_number: aadhaarNumber })
    })
    .then(data => {
        sendOTPButton.disabled = false;
        sendOTPButton.textContent = "Send OTP";

        if (data.success) {
            alert(data.message);
            document.getElementById("otp_section").style.display = "block";
        }
    })
    .catch(() => {
        sendOTPButton.disabled = false;
        sendOTPButton.textContent = "Send OTP";
    });
}

function verifyOTP() {
    const aadhaarNumber = document.getElementById("aadhaar")?.value;
    const otp = document.getElementById("otp")?.value;

    if (!aadhaarNumber || !otp) {
        showStatus("Please enter both Aadhaar number and OTP.", "error");
        return;
    }

    // Validate OTP format
    if (!/^\d{6}$/.test(otp)) {
        showStatus("Please enter a valid 6-digit OTP.", "error");
        return;
    }

    // Disable verify button during verification
    const verifyButton = document.getElementById("verify_otp_btn");
    if (verifyButton) {
        verifyButton.disabled = true;
        verifyButton.textContent = "Verifying...";
    }

    fetchWithCSRF('/accounts/verify_otp/', {
        method: 'POST',
        body: JSON.stringify({
            aadhaar_number: aadhaarNumber,
            otp: otp
        }),
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (verifyButton) {
            verifyButton.disabled = false;
            verifyButton.textContent = "Verify OTP";
        }

        if (data.success) {
            showStatus("OTP verified successfully", "success");
            enableLoginSection();
        } else {
            const errorMessage = data.error || "Failed to verify OTP. Please try again.";
            showStatus(errorMessage, "error");
        }
    })
    .catch(error => {
        console.error('Error during OTP verification:', error);
        if (verifyButton) {
            verifyButton.disabled = false;
            verifyButton.textContent = "Verify OTP";
        }
        showStatus("An error occurred while verifying OTP. Please try again.", "error");
    });
}

function enableLoginSection() {
    // Enable password section
    const passwordSection = document.getElementById("password_section");
    if (passwordSection) {
        passwordSection.style.display = "block";
        passwordSection.style.opacity = "1";
    }

    // Enable password field and login button
    const passwordField = document.getElementById("password");
    const loginButton = document.getElementById("login_btn");

    if (passwordField) {
        passwordField.disabled = false;
        passwordField.focus();
    }

    if (loginButton) {
        loginButton.disabled = false;
    }

    // Disable Aadhaar field and OTP section to prevent changes
    const aadhaarField = document.getElementById("aadhaar");
    if (aadhaarField) {
        aadhaarField.readOnly = true;
    }

    // Disable the Send OTP button
    const sendOTPButton = document.getElementById("send_otp_btn");
    if (sendOTPButton) {
        sendOTPButton.disabled = true;
    }

    // Disable the OTP field and verify button
    const otpField = document.getElementById("otp");
    if (otpField) {
        otpField.readOnly = true;
    }

    const verifyButton = document.getElementById("verify_otp_btn");
    if (verifyButton) {
        verifyButton.disabled = true;
    }
}

function getCookie(name) {
    // First try to get from cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                console.log(`Found ${name} cookie:`, cookieValue);
                break;
            }
        }
    }

    // If not found in cookie, try to get from meta tag (for CSRF token)
    if (!cookieValue && name === 'csrftoken') {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            cookieValue = metaTag.getAttribute('content');
            console.log('Found CSRF token in meta tag:', cookieValue);
        }
    }

    return cookieValue;
}

function handleLoginError(errorMessage) {
    alert(errorMessage);
    showStatus(errorMessage, "error");

    // Re-enable login button
    const loginButton = document.getElementById("login_btn");
    if (loginButton) {
        loginButton.disabled = false;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login_form");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const aadhaarField = document.getElementById("aadhaar");
            const passwordField = document.getElementById("password");
            const otpField = document.getElementById("otp");

            if (!aadhaarField.value.trim()) {
                handleLoginError("Aadhaar number is required.");
                event.preventDefault();
                return;
            }

            if (!passwordField.value.trim() && !otpField.value.trim()) {
                handleLoginError("Please provide either password or OTP.");
                event.preventDefault();
                return;
            }
        });
    }
});

function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

function updateProfile() {
    const email = sanitizeInput(document.getElementById("email").value);
    const phone = sanitizeInput(document.getElementById("phone").value);
    const firstName = sanitizeInput(document.getElementById("first_name").value);
    const lastName = sanitizeInput(document.getElementById("last_name").value);

    fetchWithCSRF('/accounts/update-profile/', {
        method: 'POST',
        body: JSON.stringify({
            email: email,
            phone: phone,
            first_name: firstName,
            last_name: lastName
        })
    })
    .then(data => {
        if (data.success) {
            alert(data.message);
            showStatus("Profile updated successfully", "success");
        }
    })
    .catch(error => {
        console.error("Error updating profile:", error);
        showStatus("Failed to update profile. Please try again.", "error");
    });
}