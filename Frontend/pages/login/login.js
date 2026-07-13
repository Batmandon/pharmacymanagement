document.getElementById("login-form").addEventListener("submit",async(e) => {
    e.preventDefault();

    const userData = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify(userData)

    });
    
    const data = await response.json();
    
    if (response.ok) {
        console.log(data);
        Swal.fire({
            icon: "success",
            title: "Login Successful",
            text: "Welcome " + data.name
        }).then(() => {
            window.location.href = "/pages/dashboard/dashboard.html";
        });
    } else {
        Swal.fire({
            icon: "error",
            title: "Login Failed",
            text: data.error || "Invalid email or password"
        });
    }
});