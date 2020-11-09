/*let hourHand = document.querySelector('.hour');
// minute hand 
let minuteHand = document.querySelector('.minute');
// second hand
let secondHand = document.querySelector('.second');

// function that rotates the hands
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

// for every 1000 milliseconds(ie, 1 second) interval, activate the rotate() function.
setInterval(rotate, 1000);
*/
var canvas = document.getElementById("canvas");
		var ctx = canvas.getContext("2d");

		ctx.strokeStyle = '#00ffff';
		ctx.lineWidth = 17;
		//ctx.shadowBlur= 15;
		ctx.shadowColor = '#00ffff'

		function degToRad(degree){
			var factor = Math.PI/180;
			return degree*factor;
		}

		function renderTime(){
			var now = new Date();
			var today = now.toDateString();
			var time = now.toLocaleTimeString();
			var hrs = now.getHours();
			var min = now.getMinutes();
			var sec = now.getSeconds();
			var mil = now.getMilliseconds();
			var smoothsec = sec+(mil/1000);
      var smoothmin = min+(smoothsec/60);

			//Background
			//gradient = ctx.createRadialGradient(250, 250, 5, 250, 250, 300);

			
			ctx.fillStyle = "rgba(0, 0, 0, 0.2)";
			ctx.clearRect(-radius, -radius, canvas.width, canvas.height);
			//Hours
			ctx.beginPath();
			ctx.arc(250,250,200, degToRad(270), degToRad((hrs*30)-90));
			ctx.stroke();
			//Minutes
			ctx.beginPath();
			ctx.arc(250,250,170, degToRad(270), degToRad((smoothmin*6)-90));
			ctx.stroke();
			//Seconds
			ctx.beginPath();
			ctx.arc(250,250,140, degToRad(270), degToRad((smoothsec*6)-90));
			ctx.stroke();
			//Date
			ctx.font = "25px Helvetica";
			ctx.fillStyle = 'rgba(00, 255, 255, 1)'
			ctx.fillText(today, 175, 250);
			//Time
			ctx.font = "25px Helvetica Bold";
			ctx.fillStyle = 'rgba(00, 255, 255, 1)';
			ctx.fillText(time, 175, 280);

		}
		setInterval(renderTime, 40);