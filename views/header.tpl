<!-- Static navbar -->
<nav class="navbar navbar-expand-lg">
  <a class="navbar-brand" href="/" style="color: red;">Disempower</a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav">
     <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Users
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
          % for item in users:
          <a  class="dropdown-item" href="/user/{{!item}}">{{!item.title()}}</a>
          % end
          <a class="dropdown-item" href="/newuser">New...</a>
        </div>
      </li>

     

     <li>
       <a class="nav-item nav-link" href="/logout">Logout</a>
     </li>
   </ul>
 </div>
</nav>



