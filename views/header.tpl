<!-- Static navbar -->
<nav class="navbar navbar-default">
<div class="container-fluid">
  <div class="navbar-header">
    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
      <span class="sr-only">Toggle navigation</span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    <a class="navbar-brand" href="#">Disempower</a>
  </div>

  <div id="navbar" class="navbar-collapse collapse">
    <ul class="nav navbar-nav">
      <li>
        <a href="/status">Status</a>
      </li>
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="/Status">Users
            <span class="caret"></span>
          </a>
        <ul class="dropdown-menu">
          % for item in users:
            <li><a href="/user/{{!item}}">{{!item.title()}}</a></li>
          % end
        </ul>
      </li> 

      <li>
        <a href="/logout">Log Out</a>
      </li>

    </ul>
  </div><!--/.nav-collapse -->
</div><!--/.container-fluid -->
</nav>
