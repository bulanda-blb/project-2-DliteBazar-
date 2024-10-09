// scripts.js

// Function to toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleBtn = document.getElementById('toggle-btn');

    if (sidebar.classList.contains('expanded')) {
        sidebar.classList.remove('expanded');
        mainContent.style.marginLeft = '60px'; 
        toggleBtn.style.top = '20px'; 
        toggleBtn.style.left = '50%';
        toggleBtn.style.transform = 'translateX(-50%)';
    } else {
        sidebar.classList.add('expanded');
        mainContent.style.marginLeft = '60px'; 
        toggleBtn.style.top = '10px';
        toggleBtn.style.right = '10px';
        toggleBtn.style.left = 'auto';
        toggleBtn.style.transform = 'none';
    }
}

// Function to highlight selected option in sidebar
function highlightOption(selectedElement) {
    const sidebarItems = document.querySelectorAll('.sidebar ul li');
    sidebarItems.forEach(item => {
        item.classList.remove('active');
    });
    selectedElement.classList.add('active');
}

// Function to open upload form
function openUploadForm() {
    document.getElementById('upload-form').style.display = 'flex';
}

// Function to close upload form
function closeUploadForm() {
    document.getElementById('upload-form').style.display = 'none';
}

// Function to open edit form based on section (phone or address)
function openEditForm(section) {
    if (section === 'phone') {
        document.getElementById('edit-phone-form').style.display = 'flex';
    } else if (section === 'address') {
        document.getElementById('edit-address-form').style.display = 'flex';
    }
}

function closeEditForm(section) {
    if (section === 'phone') {
        document.getElementById('edit-phone-form').style.display = 'none';
    } else if (section === 'address') {
        document.getElementById('edit-address-form').style.display = 'none';
    }
}

// Function to show content section based on sectionId
function showContent(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

// Function to handle "View All Notifications" button click
function viewAllNotifications() {
    console.log('View All Notifications clicked.');
    // Implement your logic here
}

// Function to toggle email notification status
function toggleEmailNotification() {
    const emailToggle = document.getElementById('email-notification');
    const notificationStatus = emailToggle.checked ? 'on' : 'off';

    console.log(`Email notification toggled ${notificationStatus}.`);
    // Simulate backend update or perform necessary actions
}
function submitNotificationForm() {
    const form = document.getElementById('notification-form');
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


// Function to open the form popup
function openForm() {
    document.getElementById("form-popup").style.display = "block";
}

// Function to close the form popup
function closeForm() {
    document.getElementById("form-popup").style.display = "none";
}

// Event listener for category selection
document.getElementById("category").addEventListener("change", function() {
    const category = this.value;
    const subcategory = document.getElementById("subcategory");
    
    // Clear existing options
    subcategory.innerHTML = "";
    
    // Enable or disable subcategory based on category selection
    if (category === "category") {
        subcategory.disabled = true; // Disable subcategory select
    } else {
        subcategory.disabled = false; // Enable subcategory select

        // Populate subcategory options based on selected category
        if (category === "nature") {
            populateSubcategories(['Mountains', 'Deserts', 'Sunsets', 'Stars and galaxies', 'Trees', 'Rivers', 'Flowers', 'Forests', 'Beaches', 'Rainbows', 'Lightning', 'Cloud and sky', 'night sky']);
        } else if (category === "wildlife") {
            populateSubcategories(['Birds', 'Mammals', 'Reptiles', 'Insects', 'Marine Life']);
        } else if (category === "urban") {
            populateSubcategories(['Architecture', 'Street Life', 'Nightlife', 'Markets', 'Urban Landscapes']);
        } else if (category === "portraits") {
            populateSubcategories(['Candid', 'Studio', 'Fashion', 'Lifestyle', 'Environmental']);
        } else if (category === "abstract") {
            populateSubcategories(['Patterns', 'Colors', 'Textures', 'Shapes', 'Reflections']);
        } else if (category === "events") {
            populateSubcategories(['Weddings', 'Concerts', 'Religious events', 'Holiday', 'Birthday', 'Sports', 'Festivals', 'Conferences']);
        } else if (category === "macro") {
            populateSubcategories(['Flowers', 'Insects', 'Textures', 'Water Drops', 'Miniatures']);
        } else if (category === "aerial") {
            populateSubcategories(['Landscapes', 'Urban Areas', 'Seascapes', 'Agricultural Fields', 'Mountains']);
        } else if (category === "travel") {
            populateSubcategories(['Cultural', 'Landmarks', 'Adventures', 'Local Life', 'Food']);
        } else if (category === "black_and_white") {
            populateSubcategories(['Portraits', 'Landscapes', 'Street', 'Architecture', 'Abstract']);
        } else if (category === "commercial") {
            populateSubcategories(['Billboards', 'Industrial', 'Automobile', 'Tourism', 'Motorcycles', 'Hotel and Resorts', 'Print Ads', 'Food and Beverages', 'Real State', 'Workplace']);
        } else if (category === "fashion") {
            populateSubcategories(['Editorial', 'catalog', 'Acessories', 'Swimwear', 'suits', 'Street style', 'Fashion shows', 'Makeup']);
        } else if (category === "lifestyle") {
            populateSubcategories(['Family', 'Couples', 'Fitness', 'Home', 'Hobbies', 'Food and Travel', 'Fashion', 'Social and Envireonmental']);
        }
    }
});

// Function to populate subcategory options
function populateSubcategories(options) {
    const subcategory = document.getElementById("subcategory");
    options.forEach(option => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.text = option;
        subcategory.add(opt);
    });
}



// Function to handle showing categories and sections for Uploaded Products
function showCategory(category) {
    const sections = document.querySelectorAll("#products .category-section");
    const categories = document.querySelectorAll("#products .product-category");

    // Hide all sections and remove active class from categories
    sections.forEach(section => {
        section.style.display = "none";
    });
    categories.forEach(category => {
        category.classList.remove("active");
    });

    // Show the selected category section
    document.getElementById(`${category}-section`).style.display = "block";

    // Add active class to the clicked category
    document.querySelector(`#products .product-category[data-category="${category}"]`).classList.add("active");
}

// Function to handle showing categories and sections for Purchased Products
function showCategoryPurchased(category) {
    const sections = document.querySelectorAll("#purchased-products .category-section");
    const categories = document.querySelectorAll("#purchased-products .product-category");

    // Hide all sections and remove active class from categories
    sections.forEach(section => {
        section.style.display = "none";
    });
    categories.forEach(category => {
        category.classList.remove("active");
    });

    // Show the selected category section
    document.getElementById(`${category}Purchased-section`).style.display = "block";

    // Add active class to the clicked category
    document.querySelector(`#purchased-products .product-category[data-category="${category}"]`).classList.add("active");
}

// Function to handle showing categories and sections for Purchased Products
function showCategoryPurchased1(category) {
    const sections = document.querySelectorAll("#purchased-products1 .category-section");
    const categories = document.querySelectorAll("#purchased-products1 .product-category");

    // Hide all sections and remove active class from categories
    sections.forEach(section => {
        section.style.display = "none";
    });
    categories.forEach(category => {
        category.classList.remove("active");
    });

    // Show the selected category section
    document.getElementById(`${category}Purchased1-section`).style.display = "block";

    // Add active class to the clicked category
    document.querySelector(`#purchased-products1 .product-category[data-category="${category}"]`).classList.add("active");
}



// Show Uploaded Images section by default when page loads
document.addEventListener('DOMContentLoaded', function() {
    showCategory('images');
});

// Show Purchased Images section by default when page loads
document.addEventListener('DOMContentLoaded', function() {
    showCategoryPurchased('images');
});

document.addEventListener('DOMContentLoaded', function() {
    showCategoryPurchased1('images');
});






// scripts.js

// Function to open the chat popup with specific person name
function openPopup(personName) {
    const popupChat = document.getElementById('popup-chat');
    const popupMessages = document.getElementById('popup-messages');
    const popupPersonName = document.getElementById('popup-person-name');

    // Replace this with AJAX call to fetch messages for the selected person
    // Dummy messages for demonstration
    const dummyMessages = [
        { type: 'received', message: 'Hello!', time: '10:00 AM' },
        { type: 'sent', message: 'Hi there!', time: '10:01 AM' },
        { type: 'received', message: 'How are you?', time: '10:02 AM' }
    ];

    // Clear previous messages
    popupMessages.innerHTML = '';

    // Display messages
    dummyMessages.forEach(message => {
        const chatDiv = document.createElement('div');
        chatDiv.classList.add('chat-message');
        chatDiv.classList.add(message.type);

        chatDiv.innerHTML = `
            <div class="chat-content">
                <p>${message.message}</p>
                <span class="chat-time">${message.time}</span>
            </div>
        `;

        popupMessages.appendChild(chatDiv);
    });

    // Display the popup chat
    popupPersonName.textContent = personName;
    popupChat.style.display = 'block';
}

// Function to close the chat popup
function closePopup() {
    const popupChat = document.getElementById('popup-chat');
    const popupMessages = document.getElementById('popup-messages');

    popupChat.style.display = 'none';
    popupMessages.innerHTML = ''; // Clear messages when closing popup
}

// Event listener to initialize chat popup when a person is clicked
document.addEventListener('DOMContentLoaded', function() {
    const chatPersons = document.querySelectorAll('.chat-person');

    chatPersons.forEach(person => {
        person.addEventListener('click', function() {
            const personName = this.querySelector('h3').textContent.trim();
            openPopup(personName);
        });
    });
});

// Event listener for chat form submission (send message)
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = messageInput.value.trim();

        if (message !== '') {
            // Replace with AJAX to send message to backend
            const sentMessage = {
                type: 'sent',
                message: message,
                time: getCurrentTime() // Function to get current time
            };

            const chatDiv = document.createElement('div');
            chatDiv.classList.add('chat-message');
            chatDiv.classList.add('sent');

            chatDiv.innerHTML = `
                <div class="chat-content">
                    <p>${sentMessage.message}</p>
                    <span class="chat-time">${sentMessage.time}</span>
                </div>
            `;

            document.getElementById('popup-messages').appendChild(chatDiv);
            messageInput.value = ''; // Clear input after sending message
            // Scroll to bottom of messages
            document.getElementById('popup-messages').scrollTop = document.getElementById('popup-messages').scrollHeight;
        }
    });

    // Function to get current time (for demonstration)
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
});







// Function to open details popup
function openDetailsPopup(issueTitle, issueDescription, participants, status) {
    const popup = document.getElementById('details-popup');
    const popupContent = popup.querySelector('.popup-content');

    
    popup.style.display = 'block';
}

// Function to close details popup
function closePopup() {
    const popup = document.getElementById('details-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}

// Event listener to open details popup when clicking on view details button
document.addEventListener('DOMContentLoaded', function() {
    const viewDetailsBtns = document.querySelectorAll('.complaint-item .view-details-btn');
    viewDetailsBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const issueTitle = this.parentNode.querySelector('h3').textContent;
            const issueDescription = this.parentNode.querySelector('p').textContent;
            const participants = Array.from(this.parentNode.querySelectorAll('.participant')).map(participant => participant.textContent);
            const status = this.parentNode.querySelector('.status-indicator').classList.contains('pending') ? 'pending' : 'solved';
            openDetailsPopup(issueTitle, issueDescription, participants, status);
        });
    });
});






document.addEventListener('DOMContentLoaded', function() {

    // Request live chat button functionality
    const requestChatBtn = document.getElementById('requestChatBtn');
    const chatBox = document.getElementById('chatBox');
    const overlay = document.getElementById('overlay');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    let chatInterval;

    requestChatBtn.addEventListener('click', function() {
        overlay.style.display = 'block';
        chatBox.style.display = 'block';
        startChatRequest();
    });

    closeChatBtn.addEventListener('click', function() {
        overlay.style.display = 'none';
        chatBox.style.display = 'none';
        clearInterval(chatInterval);
        resetChat();
    });

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            appendMessage('You', message);
            messageInput.value = '';
            // Simulate admin response
            setTimeout(function() {
                appendMessage('Admin', 'Thank you for your message. We will get back to you shortly.');
            }, 1000);
        }
    });

    // Function to start the chat request countdown
    function startChatRequest() {
        let countdown = 5 * 60; // 5 minutes countdown (in seconds)
        const timerDisplay = document.getElementById('countdownTimer');
        timerDisplay.classList.remove('hidden');

        chatInterval = setInterval(function() {
            const minutes = Math.floor(countdown / 60);
            let seconds = countdown % 60;
            seconds = seconds < 10 ? '0' + seconds : seconds;
            timerDisplay.textContent = `Requesting live chat... ${minutes}:${seconds}`;
            countdown--;

            if (countdown < 0) {
                clearInterval(chatInterval);
                timerDisplay.textContent = 'Request timed out.';
                setTimeout(function() {
                    overlay.style.display = 'none';
                    chatBox.style.display = 'none';
                    resetChat();
                }, 2000); // Hide after 2 seconds
            }
        }, 1000); // Update every second
    }

    // Function to append messages to the chat box
    function appendMessage(sender, message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        if (sender === 'You') {
            messageDiv.classList.add('user-message');
        } else {
            messageDiv.classList.add('admin-message');
        }
        messageDiv.textContent = `${sender}: ${message}`;
        chatMessages.appendChild(messageDiv);
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to reset chat state
    function resetChat() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = ''; // Clear chat messages
        const timerDisplay = document.getElementById('countdownTimer');
        timerDisplay.textContent = ''; // Clear countdown timer display
    }
});
