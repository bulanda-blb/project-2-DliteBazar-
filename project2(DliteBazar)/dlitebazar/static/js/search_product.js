document.getElementById('search-btn').addEventListener('click', function() {
    const category = document.getElementById('category').value;
    const searchInput = document.getElementById('search-input').value;

    // Just printing the values to console, you can process them with Django later
    console.log(`Category: ${category}, Search Input: ${searchInput}`);
});
