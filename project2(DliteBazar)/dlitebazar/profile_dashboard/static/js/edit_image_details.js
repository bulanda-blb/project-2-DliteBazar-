// scripts.js

function openEditModal() {
    const title = document.getElementById('title-display').textContent;
    const description = document.getElementById('description-display').textContent;
    const keywords = document.getElementById('keywords-display').textContent;
    const price = document.getElementById('price-display').textContent;
    const category = document.getElementById('category-display').textContent.toLowerCase().replace(/ /g, '_');
    const subcategory = document.getElementById('subcategory-display').textContent.toLowerCase().replace(/ /g, '_');
    
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-description').value = description;
    document.getElementById('edit-keywords').value = keywords;
    document.getElementById('edit-price').value = price;
    document.getElementById('edit-category').value = category;

    const subcategorySelect = document.getElementById('edit-subcategory');
    subcategorySelect.innerHTML = '';
    populateSubcategories(getSubcategories(category));
    subcategorySelect.value = subcategory;
    
    document.getElementById('edit-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('edit-modal').style.display = 'none';
}

document.getElementById('edit-category').addEventListener('change', function() {
    const category = this.value;
    const subcategorySelect = document.getElementById('edit-subcategory');
    subcategorySelect.innerHTML = '';
    populateSubcategories(getSubcategories(category));
});

function getSubcategories(category) {
    const subcategories = {
        nature: ['Mountains', 'Deserts', 'Sunsets', 'Stars and galaxies', 'Trees', 'Rivers', 'Flowers', 'Forests', 'Beaches', 'Rainbows', 'Lightning', 'Cloud and sky', 'night sky'],
        wildlife: ['Birds', 'Mammals', 'Reptiles', 'Insects', 'Marine Life'],
        urban: ['Architecture', 'Street Life', 'Nightlife', 'Markets', 'Urban Landscapes'],
        portraits: ['Candid', 'Studio', 'Fashion', 'Lifestyle', 'Environmental'],
        abstract: ['Patterns', 'Colors', 'Textures', 'Shapes', 'Reflections'],
        events: ['Weddings', 'Concerts', 'Religious events', 'Holiday', 'Birthday', 'Sports', 'Festivals', 'Conferences'],
        macro: ['Flowers', 'Insects', 'Textures', 'Water Drops', 'Miniatures'],
        aerial: ['Landscapes', 'Urban Areas', 'Seascapes', 'Agricultural Fields', 'Mountains'],
        travel: ['Cultural', 'Landmarks', 'Adventures', 'Local Life', 'Food'],
        black_and_white: ['Portraits', 'Landscapes', 'Street', 'Architecture', 'Abstract'],
        commercial: ['Billboards', 'Industrial', 'Automobile', 'Tourism', 'Motorcycles', 'Hotel and Resorts', 'Print Ads', 'Food and Beverages', 'Real State', 'Workplace'],
        fashion: ['Editorial', 'catalog', 'Acessories', 'Swimwear', 'suits', 'Street style', 'Fashion shows', 'Makeup'],
        lifestyle: ['Family', 'Couples', 'Fitness', 'Home', 'Hobbies', 'Food and Travel', 'Fashion', 'Social and Envireonmental']
    };
    return subcategories[category] || [];
}

function populateSubcategories(subcategories) {
    const subcategorySelect = document.getElementById('edit-subcategory');
    subcategories.forEach(function(subcat) {
        const option = document.createElement('option');
        option.value = subcat.toLowerCase().replace(/ /g, '_');
        option.textContent = subcat;
        subcategorySelect.appendChild(option);
    });
}
