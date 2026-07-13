document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const userData = {
        name: document.getElementById("full_name").value,
        pharmacy_name: document.getElementById("pharmacy_name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    });
    const data = await response.json();

    if (response.ok) {
        window.location.href = "/pages/login/login.html";
    } else {
        data.error
        Swal.fire("Account already exists")
    }
    
    console.log(data);
});

    