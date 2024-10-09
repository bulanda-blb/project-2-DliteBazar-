




// Function to toggle password visibility
function togglePassword() {
    let passwordField = document.getElementById('password');
    let toggleButton = document.getElementById('toggle-password');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleButton.textContent = '👁️';
    } else {
        passwordField.type = 'password';
        toggleButton.textContent = '👁️';
    }
}

// Function to open edit form
function openEditForm() {
    document.getElementById('editPopup').style.display = 'block';
}


// Function to close edit form
function closeEditForm() {
    document.getElementById('editPopup').style.display = 'none';
}

// // Function to save edited details
// function saveEdit() {
//     let fieldName = document.getElementById('editFieldName').textContent.trim();
//     let newValue = document.getElementById('editFieldInput').value.trim();
    
//     // Update the displayed value
//     document.getElementById(fieldName).textContent = newValue;

//     // Close the edit form
//     closeEditForm();
// }
