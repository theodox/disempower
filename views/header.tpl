<!-- Static navbar -->
<nav class="navbar navbar-expand-sm">
    <a class="navbar-brand" href="/" style="color: red;">Disempower</a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav">
      <li class="nav-item dropdown position-static">
        <a class="dropdown-toggle" data-toggle="dropdown" href="/Status">Users
          <span class="caret"></span>
        </a>
        <ul class="dropdown-menu">
          % for item in users:
          <li><a href="/user/{{!item}}">{{!item.title()}}</a></li>
          % end
          <li class="nav-item">
           <a href="/newuser">Add New...</a>
         </li>
       </ul>
     </li> 
    <li>|</li>
     <li>
       <a class="nav-item" href="/logout">Logout</a>
     </li>
  </ul>
</div>
</nav>



