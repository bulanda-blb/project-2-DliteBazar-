document.getElementById('checkout-form').addEventListener('submit', function(event) {
    // Custom validation or additional JS functionality can be added here if needed.
    // For example, you can prevent form submission to simulate an error:
    // event.preventDefault();
});


function openTermsModal() {
    document.getElementById('terms-modal').style.display = 'block';
}

function closeTermsModal() {
    document.getElementById('terms-modal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('terms-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
