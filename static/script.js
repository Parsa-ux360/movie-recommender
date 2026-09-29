const moviesGrid = document.getElementById('moviesGrid');
const resultsDiv = document.getElementById('results');
const resultsGrid = document.getElementById('resultsGrid');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const selectedMovie = document.getElementById('selectedMovie');
const selectedTitle = document.getElementById('selectedTitle');

let searchTimeout = null;

async function fetchRecommendations(title) {
    selectedTitle.textContent = title;
    selectedMovie.classList.remove('hidden');

    const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });

    const data = await response.json();

    if (data.recommendations) {
        displayResults(data.recommendations);
    } else {
        resultsGrid.innerHTML = '<p class="empty">No recommendations found.</p>';
        resultsDiv.classList.remove('hidden');
    }
}

function displayResults(movies) {
    resultsGrid.innerHTML = '';
    movies.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'result-card';
        const year = movie.year > 0 ? movie.year : 'N/A';
        const poster = movie.poster
            ? `<img src="${movie.poster}" alt="${movie.title}" loading="lazy">`
            : `<div class="poster-placeholder">${movie.title[0]}</div>`;

        card.innerHTML = `
            <div class="similarity-badge">${movie.similarity}% match</div>
            <div class="poster-wrapper">${poster}</div>
            <div class="card-info">
                <h3>${movie.title}</h3>
                <div class="meta">
                    <span>${year}</span>
                    <span class="rating">${Number(movie.rating).toFixed(1)}</span>
                </div>
                <div class="genres">${movie.genres}</div>
                <p class="overview">${movie.overview}</p>
            </div>
        `;
        resultsGrid.appendChild(card);
    });
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

moviesGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.movie-card');
    if (!card) return;
    fetchRecommendations(card.dataset.title);
});

searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(searchTimeout);

    if (query.length < 2) {
        searchResults.classList.add('hidden');
        return;
    }

    searchTimeout = setTimeout(async () => {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.results.length === 0) {
            searchResults.innerHTML = '<div class="search-item">No results found</div>';
        } else {
            searchResults.innerHTML = '';
            data.results.forEach(movie => {
                const item = document.createElement('div');
                item.className = 'search-item';
                const year = movie.year > 0 ? movie.year : 'N/A';
                const thumb = movie.poster
                    ? `<img src="${movie.poster}" alt="">`
                    : `<div class="thumb-placeholder">${movie.title[0]}</div>`;
                item.innerHTML = `${thumb}<span>${movie.title} (${year})</span>`;
                item.addEventListener('click', () => {
                    fetchRecommendations(movie.title);
                    searchResults.classList.add('hidden');
                    searchInput.value = '';
                });
                searchResults.appendChild(item);
            });
        }

        searchResults.classList.remove('hidden');
    }, 250);
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
        searchResults.classList.add('hidden');
    }
});