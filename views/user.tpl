% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')

<div class="card-body">


	<div class="container-fluid" id='frame'>
		<h1> {{!username.title()}} </h1>

		<canvas id="calendar_canvas" width=128 height=400></canvas>

		<div id="creditdiv" class="container">

			<div class="row row-top-buffer">
				&nbsp;
			</div>
			<div class="row row-top-buffer">
				<h3>Intervals</h3>
			</div>
			
			<div class="row row-top-buffer ">
				<div class="col-md-12">

					<form method="POST" action="/interval/{{!username}}" >
						
						<div class="form-row">
							<div class="form-group col-md-2">
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
								</select class='input-group'>	
							</div>

							<div class="col-sm"></div>
							<div class="form-group col-md-2">
								<label for="start_time">From</label>
								<input type="time" class="form-control" name="start_time" value="07:30">
							</div>

							<div class="col-sm"></div>
							<div class="form-group col-md-2">
								<label for="end_time">To</label>
								<input type="time" class="form-control" name="end_time" value="19:30">
							</div>

							<div class="col-sm"></div>
							<div class="form-group col-md-2">
								<label for="action_type"> Do...</label>
								<select class="form-control selcls"  name="action_type">
									<option value="add">Add</option>
									<option value="block">Block</option>
								</select>
							</div>
							<div class="col-sm"></div>
							<input type="submit" class="btn btn-outline-primary" id="set" name="set"/></input>

						</div>
					</form>
				</div>
			</div>

			<div class="row row-top-buffer">
				<div class="col-sm"></div>
				<div class="col-md-4">
					<form method="POST" action="/clear_intervals/{{!username}}">
						<button type="submit" class="btn btn-outline-primary" id="set" name="set"/>Clear all intervals</button>
					</form>
				</div>
					<div class="col-sm"></div>
				<div class="col-md-4">
					<form method="POST" action="/clear_blackouts/{{!username}}">
						<button type="submit" class="btn btn-outline-primary" id="set" name="set"/>Clear all blackouts</button>
					</form>
				</div>
					<div class="col-sm"></div>
			</div>



			<div class="row">
				<h3>Credits</h3>
			</div>
			<div class="row row-top-buffer">
				<div class="col-md-6">
					<form method="POST" action="/credit/{{!username}}" >

						<div class="form-group">
							<label for='credits'>Available</label>
							<div class="form-inline">
								<input type="number" name="credits"  class="form-control" aria-describedby="inputGroup-sizing-default" min="0"  value={{!credits}} max=720>		
								<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
							</div>
						</div>
					</form>
				</div>
				<div class="col-md-6">
					<form method="POST" action="/cap/{{!username}}" >
						<div class="form-group">

							<label for='cap'>Maximum</label>
							<div class="form-inline">
								<input type="number" name="cap"  class="form-control" aria-describedby="inputGroup-sizing-default" min="0"  value={{!cap}} max=720>		
								<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
							</div>
						</div>
					</form>
				</div>
			</div>


			<div class="row">
				<h3>Allowance</h3>
			</div>
			<div class="row row-bottom-buffer row-top-buffer">
				<div class="col-md-6">
					<form method="POST" action="/daily/{{!username}}">
						<div class="form-group">
							<label for='daily_cred'>Daily</label>
							<div class='form-inline'>
								<input type="number" name="daily_cred"  class="form-control" aria-describedby="inputGroup-sizing-default" min=0 max=300 value={{!daily}} step=15>				
								<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
							</div>
						</div>
					</form>
				</div>
				<div class="col-md-6">
					<form method="POST" action="/weekly/{{!username}}">
						<div class="	">
							<label for="weekly_cred">Weekly</label>
							<div class="form-inline"> 
								<input type="number" name="weekly_cred"  class="form-control" aria-describedby="inputGroup-sizing-default" min=0 max=600  value={{!weekly}} step=15>		
								<button type="submit" class="btn btn-outline-primary" id="submit" name="submit"/>Set</button>
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>



	<div>
	</div>
	<div id='names'></div>
</div>

<script type="module">window.disempower.set_status({{!context}});</script>
<script type="module">window.disempower.draw_calendar()</script>
