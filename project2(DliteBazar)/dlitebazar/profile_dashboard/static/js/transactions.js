document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodSelect = document.getElementById('payment_method');
    const bankDetailsDiv = document.getElementById('bankDetails');

    paymentMethodSelect.addEventListener('change', function() {
        if (paymentMethodSelect.value === 'bank') {
            bankDetailsDiv.style.display = 'block';
        } else {
            bankDetailsDiv.style.display = 'none';
        }
    });

    if (paymentMethodSelect.value !== 'bank') {
        bankDetailsDiv.style.display = 'none';
    }
});
