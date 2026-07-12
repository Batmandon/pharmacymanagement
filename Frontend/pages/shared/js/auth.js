export async function checkAuth() {
    try {
        const response = await fetch("http://127.0.0.1:8000/me", {
            method: "GET",
            credentials: "include"
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Authenticated user data:", data);
        } else {
            console.log("User is not authenticated");
        }

        if (response.status === 401) {
            const refreshResponse = await fetch("http://127.0.0.1:8000/refreshtoken", {
                method: "POST",
                credentials: "include"
            });
            const refreshTokenData = await refreshResponse.json();
            if (refreshResponse.ok) {
                console.log("Refresh token successful:", refreshTokenData);
            } else {
                console.log("Refresh token failed:", refreshTokenData);
                window.location.href = "login.html"; // Redirect to login page if refresh fails
            }
        }

    } catch (error) {
    console.error("Auth check failed:", error);
}
}

export async function logout() {
    try {
        const response = await fetch("http://127.0.0.1:8000/logout", {
            method: "POST",
            credentials: "include"
        });
        window.location.href = "../login/login.html"; // Redirect to login page after logout
        const data = await response.json();
        console.log("Logout response:", data);
    } catch (error) {
        console.error("Logout failed:", error);
    }
}

const logoutButton = document.querySelector(".btn");
logoutButton.addEventListener("click", (event) => {
    console.log("Logout button clicked");
    event.preventDefault();
    logout();
});

