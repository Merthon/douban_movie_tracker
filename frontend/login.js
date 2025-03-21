const API_URL = "http://127.0.0.1:8000";

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "index.html";
    } else {
        alert(data.detail);
    }
}

async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (response.ok) {
        alert("Registered! Please login.");
    } else {
        alert(data.detail);
    }
}