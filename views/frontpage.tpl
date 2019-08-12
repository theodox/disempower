% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')

<div class="card-body" id='loginform'>
	<div class="form-group-lg">
	<form method="POST" action="/login">
		<div class="input-group mb-2">
			<div class="input-group-prepend">
				<div class="input-group-text">
					Username
				</div>
			</div>
			<input type="text" class="form-control"  id="inlineFormInputGroup"placeholder="username" name="username">			
		</div>

		<div class="input-group mb-2">
			<div class="input-group-prepend">
				<div class="input-group-text">
					Password
				</div>
			</div>
			<input type="password" class="form-control" placeholder="password" name="password">
		</div>
		<input type="submit" value="Login" class="btn btn-primary btn-block login_btn">
	</form>
	</div>
</div>