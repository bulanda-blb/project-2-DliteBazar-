// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Admin panel scripts loaded');
// });
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Admin panel scripts loaded');
//     const sidebarLinks = document.querySelectorAll('.sidebar ul li');
//     sidebarLinks.forEach(link => {
//         link.addEventListener('click', function() {
//             sidebarLinks.forEach(l => l.classList.remove('active'));
//             this.classList.add('active');
//         });
//     });
// });



function searchUser() {
    const searchValue = document.getElementById('search').value;
    // Implement search functionality here
    console.log('Search for:', searchValue);
}

function editUser(userId) {
    // Implement edit functionality here
    console.log('Edit user with ID:', userId);
}

function deleteUser(userId) {
    // Implement delete functionality here
    console.log('Delete user with ID:', userId);
}



document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("emailModal");
    var closeBtn = document.getElementsByClassName("close")[0];

    document.querySelectorAll(".email-button").forEach(button => {
        button.onclick = function() {
            var email = this.getAttribute("data-email");
            var name = this.getAttribute("data-name");
            document.getElementById("contactEmail").value = email;
            document.getElementById("contactName").innerText = name;
            modal.style.display = "block";
        };
    });

    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});




