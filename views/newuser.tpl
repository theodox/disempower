% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')

<div class="card-body" id='loginform'>
	<form method="POST" action="/adduser">
		<div class="input-group form-group-lg">
			<label for="username">User Name</label>
			<input type="text" class="form-control" placeholder="username" name="username">			
		</div>
		<input type="submit" value="Login" class="btn float-right login_btn">
	</form>
</div>