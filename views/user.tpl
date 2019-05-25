% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')

<div class="card-body">


	<div class="container-fluid" id='frame'>
		<h1> {{!username.title()}} </h1>

		<canvas id="calendar_canvas" width=128 height=400></canvas>

		<div id="creditdiv" class="col-md-8">

			
			<div class="form-group row row-top-buffer row-bottom-buffer form-horizontal">
				<form method="POST" action="/interval/{{!username}}">
					<div class="form-group form-inline">

						<div class="input-group-prepend">
							<span class="input-group-text" id="inputGroup-sizing-default">On</span>
						</div>
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
						</select class='input-group'>	
						<div class="input-group">
							<span class="input-group-text" id="inputGroup-sizing-default">From </span>
						</div>
						<input type="time" class="form-control" name="start_time" value="07:30">

						<div class="input-group">
							<span class="input-group-text" id="inputGroup-sizing-default">To </span>
						</div>
						<input type="time" class="form-control" name="end_time" value="19:30">
						<input type="submit" name='action' value="add" class="btn btn-outline-primary">
						<input type="submit" name='action' value="block" class="btn btn-outline-secondary">
						<input type="submit" name='action' value="clear" class="btn btn-outline-primary">
						<input type="submit" name='action' value="unblock" class="btn btn-outline-secondary">
					</div>

				</form>

			</div>



			<div class="form-group row row-top-buffer row-bottom-buffer form-horizontal">
				<form method="POST" action="/credit/{{!username}}">
					<div class="form-inline">
						<div class="input-group-prepend">
							<span class="input-group-text" id="inputGroup-sizing-default">Minutes</span>
						</div>
						<input type="number" name="credits"  class="form-control" aria-describedby="inputGroup-sizing-default" min="0"  value={{!credits}} >		
						<div class="form-group">
							<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
						</div>
					</div>
				</form>
			</div>

			<div class="form-group row row-top-buffer row-bottom-buffer form-horizontal">
				<form method="POST" action="/cap/{{!username}}">
					<div class="form-inline">
						<div class="input-group-prepend">
							<span class="input-group-text" id="inputGroup-sizing-default">Cap</span>
						</div>
						<input type="number" name="cap"  class="form-control" aria-describedby="inputGroup-sizing-default" min="0"  value={{!cap}} >		
						<div class="form-group">
							<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
						</div>
					</div>
				</form>
			</div>

			<div class="form-group">
				<form method="POST" action="/daily/{{!username}}">
					<div class="form-inline">
						<div class="input-group-prepend">
							<span class="input-group-text" id="inputGroup-sizing-default">Daily</span>
						</div>
						<input type="number" name="daily_cred"  class="form-control" aria-describedby="inputGroup-sizing-default" min=0 max=300 value={{!daily}} step=15>				
						<div class="form-group">
							<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
						</div>
					</div>
				</form>
			</div>
			<div class="form-group">
				<form method="POST" action="/weekly/{{!username}}">
					<div class="form-inline">
						<div class="input-group-prepend">
							<span class="input-group-text" id="inputGroup-sizing-default">Weekly</span>
						</div>
						<input type="number" name="weekly_cred"  class="form-control" aria-describedby="inputGroup-sizing-default" min=0 max=600  value={{!weekly}} step=15>		
						<div class="form-group">
							<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>

	

	<div>
	</div>
	<div id='names'></div>
</div>

<script type="module">window.disempower.set_status({{!context}});</script>
<script type="module">window.disempower.draw_calendar()</script>
