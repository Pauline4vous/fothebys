// JavaScript file for Fotheby's Auction System

// Example: Simple form validation
document.addEventListener("DOMContentLoaded", function () {
    // Get all forms
    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            let isValid = true;
            const inputs = form.querySelectorAll("input, textarea, select");

            inputs.forEach((input) => {
                if (input.hasAttribute("required") && input.value.trim() === "") {
                    isValid = false;
                    input.style.borderColor = "red";
                } else {
                    input.style.borderColor = "#ddd";
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert("Please fill in all required fields.");
            }
        });
    });
});

// Example: Highlight archived lots in admin table
function highlightArchivedRows() {
    const rows = document.querySelectorAll("tr[data-archived='true']");
    rows.forEach((row) => {
        row.style.backgroundColor = "#f8d7da";
    });
}

highlightArchivedRows();

// Example: Dynamic message for bid placement (if implemented)
function placeBid(lotId) {
    alert(`Bid successfully placed on Lot ${lotId}!`);
}