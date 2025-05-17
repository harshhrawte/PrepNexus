document.addEventListener("DOMContentLoaded", function () {
    /* --- IMAGE SLIDER --- */
    let currentSlide = 0;
    const slides = document.querySelectorAll(".slider-image");

    if (slides.length) {
        slides[0].style.display = "block";
    }

    window.changeSlide = function (n) {
        slides[currentSlide].style.display = "none";
        currentSlide = (currentSlide + n + slides.length) % slides.length;
        slides[currentSlide].style.display = "block";
    };

    /* --- FILE UPLOAD HANDLING --- */
    let fileInput = document.getElementById("fileInput");
    let fileList = document.getElementById("fileList");
    let dragAndDropArea = document.querySelector(".drag-and-drop");

    // Allowed file extensions
    const allowedFileTypes = ['.pdf', '.docx', '.txt'];

    // Click to open file dialog
    dragAndDropArea.addEventListener("click", () => {
        fileInput.value = ""; // 🔥 Reset value to allow reselecting the same file
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener("change", handleFileUpload);

    function handleFileUpload(event) {
        let files = event.target.files;

        // Allow only 1 file
        if (files.length > 1) {
            alert("You can upload only one resume.");
            fileInput.value = "";
            return;
        }

        let file = files[0];

        // Check file type
        let fileExt = file.name.split('.').pop().toLowerCase();
        if (!allowedFileTypes.includes('.' + fileExt)) {
            alert("Invalid file type. Only PDF, DOCX, or TXT files are allowed.");
            fileInput.value = "";
            return;
        }

        // Display selected file with cancel button
        fileList.innerHTML = `
            <p>${file.name} <button class="cancel-btn" onclick="removeFile()">Cancel</button></p>
        `;
    }

    // Remove uploaded file
    window.removeFile = function () {
        fileList.innerHTML = "";
        fileInput.value = "";
    };

    /* --- DRAG & DROP HANDLING --- */
    dragAndDropArea.addEventListener("dragover", function (e) {
        e.preventDefault();
        dragAndDropArea.style.backgroundColor = "#f1c40f"; // Highlight area
    });

    dragAndDropArea.addEventListener("dragleave", function () {
        dragAndDropArea.style.backgroundColor = "transparent"; // Reset background
    });

    dragAndDropArea.addEventListener("drop", function (e) {
        e.preventDefault();
        dragAndDropArea.style.backgroundColor = "transparent";

        let files = e.dataTransfer.files;

        if (files.length > 1) {
            alert("Only one resume is allowed.");
            return;
        }

        // Check file type
        let file = files[0];
        let fileExt = file.name.split('.').pop().toLowerCase();
        if (!allowedFileTypes.includes('.' + fileExt)) {
            alert("Invalid file type. Only PDF, DOCX, or TXT files are allowed.");
            return;
        }

        fileInput.files = files; // Set files to input
        handleFileUpload({ target: fileInput }); // Trigger file upload function
    });

    /* --- SKILLS INPUT HANDLING --- */
    window.addSkill = function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            const skillInput = document.getElementById("skillInput");
            const skillsList = document.getElementById("skillsList");

            if (skillInput.value.trim()) {
                let skillItem = document.createElement("li");
                skillItem.textContent = skillInput.value;
                skillsList.appendChild(skillItem);
                skillInput.value = "";
            }
        }
    };
});