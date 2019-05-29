<!-- Static navbar -->
<nav class="navbar navbar-expand-sm bg-light navbar-light">
  <ul class="nav navbar-nav">
    <li class="nav-item">
      <a href="/status">Status</a>
    </li>
    <li class="nav-item dropdown">
      <a class="dropdown-toggle" data-toggle="dropdown" href="/Status">Users
        <span class="caret"></span>
      </a>
      <ul class="dropdown-menu">
        % for item in users:
        <li><a href="/user/{{!item}}">{{!item.title()}}</a></li>
        % end
      </ul>
    </li> 

    <li class="nav-item">
      <a href="/newuser">Add User</a>
    </li>

    <li class="nav-item">
      <a href="/logout">Log Out</a>
    </li>

  </ul>

</nav>



