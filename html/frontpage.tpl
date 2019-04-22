% rebase('base.tpl', title='Page Title')
% include('header.tpl', title='Page Title')

<div class="card-body">
	<form method="POST" action="/login">
		<div class="input-group form-group">
			<div class="input-group-prepend">
				<span class="input-group-text"><i class="fas fa-user"></i></span>
			</div>
			<input type="text" class="form-control" placeholder="username" name="username"'>
			
		</div>
		<div class="input-group form-group">
			<div class="input-group-prepend">
				<span class="input-group-text"><i class="fas fa-key"></i></span>
			</div>
			<input type="password" class="form-control" placeholder="password" name="password">
		</div>
		<div class="form-group">
			<input type="submit" value="Login" class="btn float-right login_btn">
		</div>
	</form>
</div>