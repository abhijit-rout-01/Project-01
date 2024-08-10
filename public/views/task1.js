var inputField = document.getElementById("videoURL");

inputField.addEventListener('focus', () => {
    // Add class to stop placeholder animation on focus
    inputField.classList.add('stop-animation');
});

inputField.addEventListener('blur', () => {
    // Remove class to restart placeholder animation when input loses focus
    inputField.classList.remove('stop-animation');
});