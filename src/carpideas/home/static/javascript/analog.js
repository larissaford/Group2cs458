//sets the roation of the tick marks on the clock face
var numberElements = document.querySelectorAll(".clock__numbers > div");
var radius = 360;
var pegs = numberElements.length;
var pegsI = radius / pegs;
var i = 0;

// Hands of the clock
var hourHand;
var minuteHand;
var secondHand;

/**
 * jQuery function to get hands of clock when document is ready.
 * Starts interval for running function to update hand positions.
 */
$(function () {
    // Using vanilla JS to prevent needing to parse jQuery object
    hourHand = document.querySelector('.hour');
    minuteHand = document.querySelector('.minute');
    secondHand = document.querySelector('.second');
    // for every 1000 milliseconds(ie, 1 second) interval, activate the rotate() function.
    setInterval(rotate, 1000);
})

for( let number of numberElements ){
    if( i > 0 ){
        number.style.transform = "rotate(" + pegsI * i + "deg)";
    }
    i++;
}

/**
 * Function that updates the hands of the clock
 */
function rotate() {
  // get the current Date object from which we can obtain the current hour, minute and second
  const currentDate = new Date();

  // get the hours, minutes and seconds
  const hours = currentDate.getHours();
  const minutes = currentDate.getMinutes();
  const seconds = currentDate.getSeconds();

  // rotating fraction --> how many fraction to rotate for each hand.
  const secondsFraction = seconds / 60;
  const minutesFraction = (secondsFraction + minutes) / 60;
  const hoursFraction = (minutesFraction + hours) / 12;

  // actual deg to rotate
  const secondsRotate = secondsFraction * 360;
  const minutesRotate = minutesFraction * 360;
  const hoursRotate = hoursFraction * 360;

  // apply the rotate style to each element
  // use backtick `` instead of single quotes ''
  secondHand.style.transform = `rotate(${secondsRotate}deg)`;
  minuteHand.style.transform = `rotate(${minutesRotate}deg)`;
  hourHand.style.transform = `rotate(${hoursRotate}deg)`;
}


