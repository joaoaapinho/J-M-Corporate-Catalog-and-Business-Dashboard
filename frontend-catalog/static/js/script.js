// Selecting the menu icon and navbar elements.
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

// Toggling the navbar when the menu icon is clicked.
menu.onclick = () => {
  menu.classList.toggle('bx-x');
  navbar.classList.toggle('active');
};

// Listening for the Register button on DOMContentLoaded event.
document.addEventListener("DOMContentLoaded", function () {
  const registerBtn = document.querySelector("#register-btn");

  if (registerBtn) {
    const registrationUrl = registerBtn.getAttribute("data-url");
    // Adding click event listener for the Register button.
    registerBtn.addEventListener("click", function () {
      redirectToPage(registrationUrl);
    });
  }
});

// Executing when the document is ready.
$(document).ready(function() {
  // Handling the logout button click event.
  $("#logout-button").click(function(event) {
    // Preventing default link behavior - executing instead the AJAX logout request.
    event.preventDefault();

    // Sending a POST request to /logout route.
    $.ajax({
      url: "/logout",
      type: "POST",
      success: function(data) {
        // Redirecting to the login page.
        window.location.href = "/login";
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
      }
    });
  });
});

// Defining the redirectToPage function.
function redirectToPage(url) {
  window.location.href = url;
};