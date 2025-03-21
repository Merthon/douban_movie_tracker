const API_URL = "http://127.0.0.1:8000";

function checkLogin() {
    if (!localStorage.getItem("token")) {
        window.location.href = "login.html";
    }
}

async function fetchMovies() {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_URL}/movies/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    if (!response.ok) return;
    const movies = await response.json();
    const movieList = document.getElementById("movie-list");
    movieList.innerHTML = movies.length ? "" : "<p>No movies yet.</p>";
    movies.forEach(movie => {
        const div = document.createElement("div");
        div.className = "movie";
        div.innerHTML = `
            <h3><a href="${movie.url}" target="_blank">${movie.title}</a> (${movie.rating})</h3>
            <p>Director: ${movie.director}</p>
            <p>Actors: ${movie.actors.join(", ")}</p>
            <p>Comments:</p>
            <ul>${movie.comments.map(c => `<li>${c}</li>`).join("")}</ul>
            <p>Scraped at: ${movie.scraped_at}</p>
        `;
        movieList.appendChild(div);
    });
}

async function fetchHistory() {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_URL}/history/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    if (!response.ok) return;
    const history = await response.json();
    const historyList = document.getElementById("history-list");
    historyList.innerHTML = history.length ? "" : "<p>No history yet.</p>";
    history.forEach(item => {
        const div = document.createElement("div");
        div.className = "movie";
        div.innerHTML = `
            <h3><a href="${item.movie.url}" target="_blank">${item.movie.title}</a> (${item.movie.rating})</h3>
            <p>Searched at: ${item.searched_at}</p>
        `;
        historyList.appendChild(div);
    });
}

async function addMovie() {
    const token = localStorage.getItem("token");
    const name = document.getElementById("movie-name").value;
    await fetch(`${API_URL}/movies/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name })
    });
    document.getElementById("movie-name").value = "";
    fetchMovies();
    fetchHistory();
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

window.onload = function() {
    checkLogin();
    fetchMovies();
    fetchHistory();
};