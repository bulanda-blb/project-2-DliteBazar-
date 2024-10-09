document.addEventListener('DOMContentLoaded', function () {
    const reportButton = document.querySelector('.open-report');
    const modal = document.getElementById('report-modal');
    const closeButton = document.querySelector('.close');
    const stars = document.querySelectorAll('.stars input[type="radio"]');
    const reportForm = document.getElementById('report-form');

    reportButton.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const clickedIndex = Array.from(stars).indexOf(star);
            for (let i = 0; i <= clickedIndex; i++) {
                stars[i].nextElementSibling.classList.add('selected');
            }
            for (let i = clickedIndex + 1; i < stars.length; i++) {
                stars[i].nextElementSibling.classList.remove('selected');
            }
        });
    });

    reportForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Simulate backend submission and response (replace with actual AJAX call in real application)
        const reportTitle = this.querySelector('input[name="report_title"]').value;
        const reportMessage = this.querySelector('textarea[name="report_message"]').value;

        // Simulated response handling
        const reportDetails = document.createElement('div');
        reportDetails.innerHTML = `
            <h2>Report Details</h2>
            <p><strong>Title:</strong> ${reportTitle}</p>
            <p><strong>Message:</strong> ${reportMessage}</p>
            <p><strong>Reported At:</strong> ${new Date().toLocaleString()}</p>
        `;
        
        const reportBox = document.querySelector('.report-box');
        reportBox.innerHTML = ''; // Clear form
        reportBox.appendChild(reportDetails);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.stars input[type="radio"]');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const clickedIndex = Array.from(stars).indexOf(star);
            for (let i = 0; i <= clickedIndex; i++) {
                stars[i].nextElementSibling.classList.add('selected');
            }
            for (let i = clickedIndex + 1; i < stars.length; i++) {
                stars[i].nextElementSibling.classList.remove('selected');
            }
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.stars input[type="radio"]');

    stars.forEach(star => {
        star.addEventListener('change', function () {
            const clickedIndex = Array.from(stars).indexOf(star);
            stars.forEach((star, index) => {
                if (index <= clickedIndex) {
                    star.nextElementSibling.classList.add('selected');
                } else {
                    star.nextElementSibling.classList.remove('selected');
                }
            });
        });
    });
});





document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.querySelector('.edit-review-button');
    const editModal = document.getElementById('edit-review-modal');
    const closeEditButton = editModal.querySelector('.close');
    const editStars = editModal.querySelectorAll('.edit-stars input[type="radio"]');

    editButton.addEventListener('click', function () {
        editModal.style.display = 'block';
    });

    closeEditButton.addEventListener('click', function () {
        editModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });

    editStars.forEach(star => {
        star.addEventListener('change', function () {
            const clickedIndex = Array.from(editStars).indexOf(star);
            editStars.forEach((star, index) => {
                if (index <= clickedIndex) {
                    star.nextElementSibling.classList.add('selected');
                } else {
                    star.nextElementSibling.classList.remove('selected');
                }
            });
        });
    });
});




