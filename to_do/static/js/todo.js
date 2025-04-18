document.addEventListener("DOMContentLoaded", function () {
    const readMoreLinks = document.querySelectorAll(".read-more");
    const closeButtons = document.querySelectorAll(".close");
  
    readMoreLinks.forEach(link => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const id = this.getAttribute("data-id");
        document.getElementById(`modal-${id}`).style.display = "block";
      });
    });
  
    closeButtons.forEach(button => {
      button.addEventListener("click", function () {
        const id = this.getAttribute("data-id");
        document.getElementById(`modal-${id}`).style.display = "none";
      });
    });
  
    // Optional: Close modal when clicking outside
    window.addEventListener("click", function (event) {
      if (event.target.classList.contains("modal")) {
        event.target.style.display = "none";
      }
    });
  });
  