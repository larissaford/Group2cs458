/* Variables for Widget Bank operation */
var bankContainer = $("#widgetBank") // Container for all widgets
var isOpen = false // State of Widget Bank
var currentlyDraggedWidgetLocation = "" // location of widget being dragged
var dragX, dragY; // coordinates of widget being dragged

// Available Widgets in Bank
// Collects all Widget containers and makes it
// easier to reference when first setting up the page
var widgets = $(".widgetContainer").map(x => {
    // console.log(x)
    var container = $(".widgetContainer").eq(x);
    var widget = container.find(".widget");
    var icon = container.find(".icon")
    var widgetObject = {
        container: container,
        widget: widget,
        icon: icon
    }
    return widgetObject
});

/**
 * jQuery method to run a function when document is ready.
 */
$(addWidgetsToList())

/**
 * Sets up widgets for first time in the page.
 * Places any widgets in the Widget Bank, hides the widget itself
 * and shows an icon to represent the widget
 */
function addWidgetsToList() {
    // Reference to List inside the Bank
    var widgetList = $("#widgetList")

    for(var i = 0; i < widgets.length; i++) {
        var widgetObject = widgets[i]; // get widget
        var widgetContainer = widgetObject["container"];
        var widget = widgetObject["widget"];
        var icon = widgetObject["icon"];

        widget.hide() // hide by default
        icon.show() // show icon by default
        widgetList.append(widgetContainer)
    }
}

/**
 * Function that opens the widget bank by changing width
 */
function openBank() {
    bankContainer.width("20%");
}

/**
 * Function that closes the widget bank by changing width
 */
function closeBank() {
    bankContainer.width(0);
}

/**
 * Function that will open/close widget bank based on global state variable
 */
function activateBank() {
    isOpen ? closeBank() : openBank();
    isOpen = !isOpen;
}


function allowDrop(event) {
    event.preventDefault()
}

// TODO: Fix when another div is in same "line" causing issues with dragging over body
// TODO: Highlight location when dragged over
/**
 * Event listener that checks where widget is being dragged and updates
 * global state variable of the drag location.
 */
document.addEventListener("dragenter", function dragenter(event) {
    var location = ""
    var dragOverId = event.target.id
    console.log(dragOverId)
    console.log(event.target)
    // location of the main area of page
    if(dragOverId == "image") {
        location = "body"
    }
    // location of the Widget Bank
    else if(dragOverId == "widgetBank") {
        location = "bank"
    }
    // We are somewhere else
    else {
        location = ""
    }
    console.log("DRAG ENTER " + location)
    currentlyDraggedWidgetLocation = location
})

/**
 * Event listener for tracking drag location
 * and updates a global state varaibles.
 */
document.addEventListener("dragover", function(event) {
    event.preventDefault()
    dragX = event.pageX
    dragY = event.pageY
    console.log("(" + dragX + "," + dragY + ")")
})


/**
 * Event listener  for when user stops dragging
 */
document.addEventListener("drop", function(event) {
    event.preventDefault()
    console.log("DROP")
})

function drop(event) {
    event.preventDefault()

    var widgetContainerElement = getWidgetContainerElement(event.target)
    if(currentlyDraggedWidgetLocation == "body") {
        activateWidget($(widgetContainerElement))
    }
    else if (currentlyDraggedWidgetLocation == "bank") {
        deactivateWidget($(widgetContainerElement))
    }
    // reset the currently dragged location
    currentlyDraggedWidgetLocation = ""
    // reset drag coordinates after done
    dragX = 0; dragY = 0;
}

/**
 * Checks if dragged element has the parent node with the 'widgetContainer' class
 * Iterates over the parent elements till found and returns it.
 * @param draggableElement element that has been successfully dragged
 * @returns widgetContainer of widget that was dragged, undefined if
 */
function getWidgetContainerElement(draggableElement) {
    var widgetContainer = draggableElement
    while (!(widgetContainer.classList.contains("widgetContainer"))) {
        widgetContainer = widgetContainer.parentElement
    }
    return widgetContainer
}

/**
 * Makes widget available to be used.  Shows the widget on the main page,
 * hides the icon, and adds the widget to the location of end drag location
 * @param widgetContainer the widget that was dragged
 */
function activateWidget(widgetContainer) {
    // undefined check
    if (widgetContainer) {
        // check if it is a widgetContainer
        if (widgetContainer.hasClass("widgetContainer")) {
            // Get pieces of widget
            var widget = widgetContainer.find(".widget");
            var icon = widgetContainer.find(".icon")
            // undefined check for pieces
            if (widget && icon) {
                $("body").append(widgetContainer)
                // hide icon and show widget if needed
                if (icon.is(":visible")) icon.hide()
                if (widget.is(":hidden")) widget.show();

                // calculate offset to center widget to location of drag
                offsetX = dragX - (widget.width() / 2)
                offsetY = dragY - (widget.height() / 2)
                // move widget to location of drag
                widget.css("left", offsetX + "px")
                widget.css("top", offsetY + "px")
            }
        }
    }
}

/**
 * Removes widget from page to be put in bank. Removes widget from main page,
 * shows the icon in bank, and adds the widget to the Widget Bank
 * @param widgetContainer the widget that was dragged
 */
function deactivateWidget(widgetContainer) {
    // undefined check
    if (widgetContainer) {
        // check if it is a widgetContainer
        if (widgetContainer.hasClass("widgetContainer")) {
            // Get pieces of widget
            var widget = widgetContainer.find(".widget");
            var icon = widgetContainer.find(".icon")
            // undefined check for pieces
            if (widget && icon) {
                // show icon and hide widget
                if (icon.is(":hidden")) icon.show()
                if (widget.is(":visible")) widget.hide()
                // move to widget bank
                bankContainer.append(widgetContainer)
            }
        }
    }
}