/* Variables for Widget Bank operation */

// Container for all widgets
var bankContainer = $("#widgetBank")
// State of Widget Bank
var isOpen = false
var currentlyDraggedWidgetLocation = ""
var dragX, dragY;

// Available Widgets in Bank

// This is a stupid way of getting our widgets, but it works
// Doing it this way, so we have a jQuery object of each widget
// instead of just the HTML
// var widgets = $(".widgetContainer").map(x => $(".widgetContainer").eq(x));
var widgets = $(".widgetContainer").map(x => {
    // console.log(x)
    var container = $(".widgetContainer").eq(x);
    var widget = container.find(".widget");
    var icon = container.find(".icon")
    var iframe = container.find("iframe")
    if(iframe) {
        iframe.draggable = true
        console.log(iframe)
    }
    var widgetObject = {
        container: container,
        widget: widget,
        icon: icon
    }
    return widgetObject
});

$("")


// JQuery function to call when document is ready
$(addWidgetsToList())

// Adds widgets to the Widget List
function addWidgetsToList() {
    var widgetList = $("#widgetList")
    console.log(widgets.length)

    for(var i = 0; i < widgets.length; i++) {
        var widgetObject = widgets[i]; // get widget
        var widgetContainer = widgetObject["container"];
        var widget = widgetObject["widget"];
        // console.log(widget)
        var icon = widgetObject["icon"];

        widget.hide() // hide by default
        // create option in bank
        // var listItem = widgetList.append("<li onclick='activateWidget("+i+")'>" + widget + "</li>")
        // var listItem = widgetList.append("<li>" + widgetContainer + "</li>")
        var listItem = widgetList.append(widgetContainer)

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

document.addEventListener("dragstart", onDragStart)
function onDragStart(event) {
    // console.log(event.screenX)
    // console.log(event.screenY)
    // event.dataTransfer.setData("text/html", event.target.id)
    // console.log("DRAG START " + event.target.id)
    // console.log(event.target)
    // console.log(event.target.parentElement)
}

function allowDrop(event) {
    event.preventDefault()
}

// document.addEventListener("drag", function drag(event) {
//     event.preventDefault()
//     // event.
//     console.log("DRAG " + event.target.className)
//     console.log(event.target)
//     // event.dataTransfer.setData("text/html", event.target.id)
//     console.log(event.pointerX)
//     console.log(event.pointerY)
// })

// TODO: Fix when another div is in same "line" causing issues with dragging over body
// TODO: Highlight location when dragged over
// Event Listener to check where widget is being dragged
document.addEventListener("dragenter", function dragenter(event) {
    var location = ""
    var dragOverId = event.target.id
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

document.addEventListener("dragover", function(event) {
    dragX = event.pageX
    dragY = event.pageY
    // console.log("(X,Y) = ("+dragX+","+dragY+")")
})

// TODO: how to get main widget content from dragged item
// Called when releasing mouse button of a dragged widget
document.addEventListener("drop", function(event) {
    event.preventDefault()
    console.log("DROP")

    // console.log(event.touches[0].clientX)
    // console.log(event[0].clientY)
})

function drop(event) {
    event.preventDefault()

    var widgetContainerElement = getWidgetContainerElement(event.target)
    console.log(widgetContainerElement)
    if(currentlyDraggedWidgetLocation == "body") {
        activateWidget($(widgetContainerElement))
    }
    else if (currentlyDraggedWidgetLocation == "bank") {
        deactivateWidget($(widgetContainerElement))
    }
    // console.log("DROP: " + currentlyDraggedWidgetLocation)

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