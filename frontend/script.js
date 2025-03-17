const API_URL = "http://127.0.0.1:8000/movies/";

async function fetchMovies() {
    const response = await fetch(API_URL);
    const movies = await response.json();
    const movieList = document.getElementById("movie-list");
    movieList.innerHTML = movies.length ? "" : "<p>No movies yet.</p>";
    movies.forEach(movie => {
        const div = document.createElement("div");
        div.className = "movie";
        div.innerHTML = `
            <h2><a href="${movie.url}" target="_blank">${movie.title}</a> (${movie.rating})</h2>
            <p>Director: ${movie.director}</p>
            <p>Actors: ${movie.actors.join(", ")}</p>
            <p>Comments:</p>
            <ul>${movie.comments.map(c => `<li>${c}</li>`).join("")}</ul>
            <p>Scraped at: ${movie.scraped_at}</p>
        `;
        movieList.appendChild(div);
    });
}

async function addMovie() {
    const name = document.getElementById("movie-name").value;
    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });
    document.getElementById("movie-name").value = "";
    fetchMovies();
}

window.onload = fetchMovies;