function draw_calendar(arg)
{
		var canvas = document.getElementById("fred");
		canvas.addEventListener('click', function() { 
			canvas.style.width ='100%';
			canvas.style.height='100%';
			// ...then set the internal size to match
			canvas.width  = canvas.offsetWidth;
			canvas.height = canvas.offsetHeight;
			var ctx = canvas.getContext("2d");
			ctx.fillStyle = "#FF0000";
			ctx.fillRect(0, 0, 150, 75);
			console.log(canvas.width)
		}, false);
}