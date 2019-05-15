% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')
 
<div class="card-body">

<div class="container-fluid" id='frame'>
	<h1> {{!username}}</h1>
 		<canvas id="calendar_canvas" width=128 height=400></canvas>
 		<div id='names'></div>

 		<form method="POST" action="/credit/{{!username}}">
		<div class="input-group form-group-lg">
			<label for="credits">Add Credits</label>
			<input type="range" name="credits" min="-180" max="180">		
		</div>
		
		<input type="submit" value="Add" class="btn float-right login_btn">
	</form>
 </div>
<script type="module">window.disempower.set_status({{!context}});</script>
<script type="module">window.disempower.draw_calendar()</script>
