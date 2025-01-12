document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", event => {
            const inputs = form.querySelectorAll("input[required], select[required], textarea[required]");
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = "red";
                } else {
                    input.style.borderColor = "#ddd";
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    });
});