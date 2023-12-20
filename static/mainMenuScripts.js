
function playWithAI(color) {
    // Implement the logic for playing with AI using the selected color
    window.location.href = `/playWithAI?color=${color}`;
}

function playOffline() {
    // Redirect to the index.html page
    window.location.href = "/playOffline";
}
// Add these functions to your playScripts.js
function openColorSelection() {
    const modal = document.getElementById('colorSelectionModal');
    modal.style.display = 'block';
}

function closeColorSelection(color) {
    const modal = document.getElementById('colorSelectionModal');
    modal.style.display = 'none';
    if (color) {
        playWithAI(color);
    } else {
        window.location.href = "/playWithAI";
    }

}

function selectColor(color) {
    // Handle the selected color (e.g., start the game with the chosen color)
    console.log(`Selected color: ${color}`);
    closeColorSelection(color);
    // Add logic to start the game with the selected color
    // For example, you can call a function like startGameWithAI(color);
}

// Close the modal if the user clicks outside the modal
window.onclick = function (event) {
    const modal = document.getElementById('colorSelectionModal');
    if (event.target === modal) {
        closeColorSelection();
    }
};
