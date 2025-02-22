document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function (event) {
            let inputs = form.querySelectorAll("input");
            for (let input of inputs) {
                if (input.value.trim() === "") {
                    alert("Please fill in all fields.");
                    event.preventDefault();
                    return;
                }
            }
        });
    }
});

function requestOTP() {
    let aadhaarNumber = document.getElementById("aadhaar").value;

    if (!/^\d{12}$/.test(aadhaarNumber)) {
        alert("Please enter a valid 12-digit Aadhaar number.");
        return;
    }

    fetch("/api/request-otp/", {
        method: "POST",
        body: new URLSearchParams({ "aadhaar_number": aadhaarNumber }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message + " OTP: " + data.otp);
        }
    })
    .catch(error => console.error("Error:", error));
}