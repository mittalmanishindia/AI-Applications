document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const body = document.body;

    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        if (query.length > 0) {
            body.classList.add('searching');
            debounceTimer = setTimeout(() => performSearch(query), 300);
        } else {
            body.classList.remove('searching');
            resultsContainer.innerHTML = `
                <div class="placeholder-text">
                    <p>Type something to start exploring.</p>
                </div>
            `;
        }
    });

    async function performSearch(query) {
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            renderResults(results);
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = '<p style="text-align:center; color: #ef4444;">Something went wrong. Please try again.</p>';
        }
    }

    function renderResults(results) {
        resultsContainer.innerHTML = '';

        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="placeholder-text">
                    <p>No results found for your query.</p>
                </div>
            `;
            return;
        }

        results.forEach((result, index) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.style.animationDelay = `${index * 0.1}s`; // Staggered animation

            card.innerHTML = `
                <a href="${result.url}" class="result-url" target="_blank">${result.url}</a>
                <a href="${result.url}" class="result-title" target="_blank">${result.title}</a>
                <p class="result-snippet">${result.snippet}</p>
            `;

            resultsContainer.appendChild(card);
        });
    }
});
