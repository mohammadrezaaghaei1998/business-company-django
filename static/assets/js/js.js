document.addEventListener("DOMContentLoaded", function() {
  var servicesList = document.getElementById("servicesList");
  var serviceDescription = document.getElementById("serviceDescription");

  servicesList.addEventListener("click", function(event) {
      if (event.target.tagName === "LI" && event.target.hasAttribute("data-service")) {
          var selectedService = event.target.getAttribute("data-service");

          var allDescriptions = document.querySelectorAll(".description");
          allDescriptions.forEach(function(description) {
              description.style.display = "none";
          });

          var selectedDescription = document.querySelector(".description[data-service='" + selectedService + "']");
          if (selectedDescription) {
              selectedDescription.style.display = "block";
              document.querySelector(".default-description").style.display = "none"; // Hide default description
          }

          event.preventDefault();
      }
  });
});







  document.addEventListener('DOMContentLoaded', function () {
    var backToTopBtn = document.getElementById('backToTopBtn');

    window.addEventListener('scroll', function () {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    backToTopBtn.addEventListener('click', function (event) {
        event.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});









function shareInvestment(name, description) {
  var currentPageUrl = window.location.href;
  var productDetails = "Product Name: " + name + "\nDescription: " + description;
  $("#share-content").text(currentPageUrl);
  $("#shareModal").show();
}

function closeModal() {
  $("#shareModal").hide();
}

function copyLink() {
  var shareContent = document.getElementById("share-content");
  var range = document.createRange();
  range.selectNode(shareContent);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  alert("Link copied!");

  closeModal();
}









//Ajax for add to favorite
$(document).ready(function() {
  $(".addToFavoriteBtn").on("click", function() {
      var investmentId = $(this).data("investment-id");
      var formData = new FormData($("#addToFavoriteForm" + investmentId)[0]);
      
      $.ajax({
          type: "POST",
          url: $("#addToFavoriteForm" + investmentId).attr("action"),
          data: formData,
          processData: false,
          contentType: false,
          dataType: "json",
          success: function(response) {
              if (response.status === 'added_to_favorite') {
                  alert('Added to favorites!');
                  // You can update the UI or perform other actions here
              } else if (response.status === 'already_favorite') {
                  alert('Already in favorites!');
                  // You can handle the case where the item is already in favorites
              } else {
                  alert('Error occurred!');
                  // Handle other errors if needed
              }
          },
          error: function() {
              alert('Oops! An error occurred. Please log in to add this to your favorites.');
              // Handle AJAX error
          }
      });
  });
});








//remove from favorite
$(document).ready(function() {
    $('.removeFromFavoriteBtn').on('click', function() {
        var investmentId = $(this).data('investment-id');
        var url = $(this).closest('form').attr('action');
        var container = $(this).closest('.investment-container');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'investment_id': investmentId,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {
                if (data.status === 'removed_from_favorite') {
                    var userWantsToReload = confirm('Removed from favorite successfully. Do you want to reload the page to see the change?');
                    if (userWantsToReload) {
                        location.reload(); // Reload the page
                    } else {
                        container.remove(); // Remove the entire container from the DOM
                        // You can add more logic here if needed
                    }
                } else if (data.status === 'not_in_favorite') {
                    alert('This investment is not in your favorites.');
                } else {
                    alert('Unexpected response from the server.');
                }
            },
            error: function() {
                alert('An error occurred while processing your request.');
            }
        });
    });
});