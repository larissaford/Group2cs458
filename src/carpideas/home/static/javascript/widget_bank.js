/* Variables for Widget Bank operation */

// Container for all widgets
var bankContainer = $("#widgetBank")
// State of Widget Bank
var isOpen = false

// Available Widgets in Bank
var widgets = [
    {
        name: "Spotify",
        html: $("#spotify_widget")
    },
    {
        name: "Analog Clock",
        html: $("#analog_clock")
    }
]

// JQuery function to call when document is ready
$(addWidgetsToList())

// Adds widgets to list
function addWidgetsToList() {
    var widgetList = $("#widgetList")

    for(var i = 0; i < widgets.length; i++) {
        var widget = widgets[i];
        console.log(widget)
    // for(var widget of widgets) {
        // Do we want to add an onclick function for each widget?
        widget["html"].hide()
        // var listItem = widgetList.append("<li draggable='true' ondragstart='drag(event)'>" + widget["name"] + "</li>");
        var listItem = widgetList.append("<li onclick='activateWidget("+i+")'>" + widget["name"] + "</li>")

    }
}

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
        // console.log("CLOSING");
        closeBank();
    } else {
        // console.log("OPENING");
        openBank();
    }
    isOpen = !isOpen;
}

function activateWidget(widgetId) {
    // Ternary operator to check if value is defined
    var widget = (widgets[widgetId]) ? widgets[widgetId]["html"] : undefined;
    if(widget) {
        if(widget.is(":visible")){
            widget.hide();
        } else {
            widget.show();
        }
    }
}