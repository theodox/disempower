% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')
 
<div class="card-body">

<div class="container-fluid" id='frame'>
	<h1>Weekly times</h1>
 		<canvas id="calendar_canvas" width=128 height=400></canvas>
 		<div id='names'></div>
 </div>
<script type="module">window.disempower.set_status({{!context}});</script>
<script type="module">window.disempower.draw_calendar()</script>
<script type="module">window.disempower.show_times()</script>
