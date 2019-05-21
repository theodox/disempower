% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')
 
<div class="card-body">

<!--This works with the theme, so convert all the forms below-->

<div class="input-group mb-3 form-group-lg">
			  <div class="input-group-prepend">
			    <span class="input-group-text" id="inputGroup-sizing-default">Add Credits</span>
			  </div>
			  <input type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
	</div>

<div class="container-fluid" id='frame'>
	<h1> {{!username.title()}} </h1>
	<h3> {{!credits}} / {{!cap}} available </h3>
	<h4> ({{!daily}}/{{!weekly}})</h4>
 		<canvas id="calendar_canvas" width=128 height=400></canvas>
		<div id='creditdiv' class="input-group mb-3">
		<h3>credits</h3>

		
		<form method="POST" action="/credit/{{!username}}">

			

			<div class="input-group form-group-lg">
				<label for="credits">Add Credits</label>
				<input type="number" name="credits" min="-180" max="180" value=30 step=15>		
			</div>
			
			<input type="submit" value="Add" class="btn float-right login_btn">
		</form>

		<form method="POST" action="/daily/{{!username}}">
			<div class="input-group form-group-lg">
				<label for="daily_cred">Daily </label>
				<input type="number" name="daily_cred" min="0" max="180" value=60 step=15>		
			</div>
			
			<input type="submit" value="Set" class="btn float-right login_btn">
		</form>

		<form method="POST" action="/weekly/{{!username}}">
			<div class="input-group form-group-lg">
				<label for="weekly_cred">Weekly</label>
				<input type="numeric" name="weekly_cred" min="0" max="600" value="60" step="15">		
			</div>
			
			<input type="submit" value="Set" class="btn float-right login_btn">
		</form>
		</div>

		<form method="POST" action="/interval/{{!username}}">
			<div class="form-group">
				<div class="row form-inline">
					<div class="form-group">
					
						<label for="days">On</label>
						<select class="form-control selcls"  name="days">
							<option value="(0,)">Monday</option>
							<option value="(1,)">Tuesday</option>
							<option value="(2,)">Wedneday</option>
							<option value="(3,)">Thursday</option>
							<option value="(4,)">Friday</option>
							<option value="(5,)">Saturday</option>
							<option value="(6,)">Sunday</option>
							<option value="(0,1,2,3,4)">Weekdays</option>
							<option value="(5,6)">Weekends</option>
						</select>	
						<label for="start_time">From</label>
						<input type="time" class="form-control input-sm" name="start_time" value="07:30">

						<label for='end_time'>To</label>
						<input type="time" class="form-control input-sm" name="end_time" value="19:30">
						<input type="submit" name='action' value="add" class="btn btn-primary mb-2">
						<input type="submit" name='action' value="block" class="btn btn-primary mb-2">

					</div>
					<input type="submit" name='action' value="clear" class="btn btn-primary mb-2">
					<input type="submit" name='action' value="unblock" class="btn btn-primary mb-2">
				</div>
			</div>
			

		</form>

	<div>
	</div>
	<div id='names'></div>
 </div>

<script type="module">window.disempower.set_status({{!context}});</script>
<script type="module">window.disempower.draw_calendar()</script>
