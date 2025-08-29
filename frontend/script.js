document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'http://127.0.0.1:8001';

    // Get all the HTML elements, including the pagination buttons.
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const downloadButton = document.getElementById('downloadButton');
    const resultsBody = document.getElementById('resultsBody');
    const loader = document.getElementById('loader');
    const resultsInfo = document.getElementById('resultsInfo');
    const paginationControls = document.getElementById('paginationControls');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const pageInfo = document.getElementById('pageInfo');

    // --- State Variables ---
    // Keep track of our current position in the search results.
    let currentPage = 1;
    let totalResults = 0;
    const resultsPerPage = 15;

    // This function sends the search request to your Python backend for a specific page.
// REPLACE your old performSearch function with this one.
async function performSearch(page = 1) {
    const query = searchInput.value;
    currentPage = page;
    
    console.log("--- Starting search for page:", currentPage, "---"); // <-- Checkpoint 1

    loader.classList.remove('hidden');
    resultsBody.innerHTML = '';
    resultsInfo.textContent = '';
    paginationControls.classList.add('hidden');

    const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query, page: currentPage }),
    });

    const data = await response.json();
    totalResults = data.total;
    
    console.log("Data received from backend:", data); // <-- Checkpoint 2

    loader.classList.add('hidden');
    displayResults(data.results);
    updatePagination();
}

// REPLACE your old displayResults function with this one.
function displayResults(results) {
    resultsBody.innerHTML = '';

    console.log("Attempting to display", results.length, "new results."); // <-- Checkpoint 3
    if (results.length > 0) {
        console.log("First new result is:", results[0]); // <-- Checkpoint 4
    }

    if (results.length === 0) {
        resultsInfo.textContent = 'No users found for this page.';
        resultsBody.innerHTML = '<tr><td colspan="4">No results found.</td></tr>';
        return;
    }

    resultsInfo.textContent = `Showing results for page ${currentPage}.`;
    
    results.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.user_id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.country}</td>
        `;
        resultsBody.appendChild(row);
    });
}

    // This function displays the results in the HTML table.
    // In script.js, replace your displayResults function with this one.

function displayResults(results) {
    // This line is crucial! It clears all old data from the table.
    resultsBody.innerHTML = '';

    if (results.length === 0) {
        resultsInfo.textContent = 'No users found for this page.';
        resultsBody.innerHTML = '<tr><td colspan="4">No results found.</td></tr>';
        return;
    }

    resultsInfo.textContent = `Showing results for page ${currentPage}.`;
    
    // This loop adds the new rows for the current page.
    results.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.user_id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.country}</td>
        `;
        resultsBody.appendChild(row);
    });
}
    
    // This function updates the pagination buttons and text.
    function updatePagination() {
        if (totalResults > resultsPerPage) {
            const totalPages = Math.ceil(totalResults / resultsPerPage);
            pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
            
            prevButton.disabled = currentPage === 1;
            nextButton.disabled = currentPage === totalPages;

            paginationControls.classList.remove('hidden');
        } else {
            paginationControls.classList.add('hidden');
        }
    }

    // This function handles the download request.
    async function performDownload() {
        const query = searchInput.value;
        downloadButton.textContent = 'Downloading...';
        downloadButton.disabled = true;

        try {
            const response = await fetch(`${API_URL}/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query }),
            });
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'user_results.json';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } finally {
            downloadButton.textContent = 'Download Filtered Results';
            downloadButton.disabled = false;
        }
    }

    // --- Set up the buttons ---
    searchButton.addEventListener('click', () => performSearch(1));
    prevButton.addEventListener('click', () => performSearch(currentPage - 1));
    nextButton.addEventListener('click', () => performSearch(currentPage + 1));
    downloadButton.addEventListener('click', performDownload);

    // Also search when the user presses "Enter".
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch(1);
        }
    });
});