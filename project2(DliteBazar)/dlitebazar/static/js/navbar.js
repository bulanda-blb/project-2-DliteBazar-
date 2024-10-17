document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('liked-photos').addEventListener('click', () => {
        openModal('liked-modal');
    });

    document.getElementById('cart').addEventListener('click', () => {
        openModal('cart-modal');
    });

    document.querySelectorAll('.select-item').forEach(checkbox => {
        checkbox.addEventListener('change', updateCartSummary);
    });

    document.querySelector('.buy-now').addEventListener('click', () => {
        // Handle buy now action
        alert('Proceeding to checkout');
    });
});

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}
// cart summary
function updateCartSummary() {
    const selectedItems = document.querySelectorAll('.select-item:checked');
    let totalAmount = 0;
    let selectedCount = 0;

    selectedItems.forEach(item => {
        totalAmount += parseFloat(item.dataset.price);
        selectedCount++;
    });

    document.getElementById('selected-count').textContent = selectedCount;
    document.getElementById('total-amount').textContent = totalAmount.toFixed(2);
}

function toggleGems() {
    const gemsSwitch = document.getElementById('gems-switch');
    if (gemsSwitch.checked) {
        // Gems ON logic (if needed)
        console.log('Gems ON');
    } else {
        // Gems OFF logic (if needed)
        console.log('Gems OFF');
    }
}
