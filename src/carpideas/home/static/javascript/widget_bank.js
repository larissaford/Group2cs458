
var bankContainer = $("#widgetBank")
var isOpen = false

// Changes width of bank to open
function openBank() {
    bankContainer.width("25%");
}

// Changes width of bank to close
function closeBank() {
    bankContainer.width(0);
}

// Called by button event listener
function activateBank() {
    if(isOpen) {
        console.log("CLOSING");
        closeBank();
    } else {
        console.log("OPENING");
        openBank();
    }
    isOpen = !isOpen;
}