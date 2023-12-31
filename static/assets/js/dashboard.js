document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll(".nav li a");
    const contentSections = document.querySelectorAll(".content-section");

    navLinks.forEach((link, index) => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            
            contentSections.forEach(section => {
                section.style.display = "none";
            });

            contentSections[index].style.display = "block";
        });
    });
});












