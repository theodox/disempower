% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')
 
<div class="card-body">

<div class="container-fluid">
<div class="cal-row row">
	<div class="cal-cell col-xs-1"></div>
	<div class="cal-cell col-xs-1"><span class="clockday">M</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">T</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">W</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">Th</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">Fr</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">Sa</span></div>
	<div class="cal-cell col-xs-1"><span class="clockday">Su</span></div>

</div>
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock"></span></div>
% setdefault('M0','')
<div class="cal-cell col-xs-1">{{!M0}}</div>
% setdefault('T0','')
<div class="cal-cell col-xs-1">{{!T0}}</div>
% setdefault('W0','')
<div class="cal-cell col-xs-1">{{!W0}}</div>
% setdefault('TH0','')
<div class="cal-cell col-xs-1">{{!TH0}}</div>
% setdefault('FR0','')
<div class="cal-cell col-xs-1">{{!FR0}}</div>
% setdefault('SA0','')
<div class="cal-cell col-xs-1">{{!SA0}}</div>
% setdefault('SU0','')
<div class="cal-cell col-xs-1">{{!SU0}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">6 am</span></div>
% setdefault('M6','')
<div class="cal-cell col-xs-1">{{!M6}}</div>
% setdefault('T6','')
<div class="cal-cell col-xs-1">{{!T6}}</div>
% setdefault('W6','')
<div class="cal-cell col-xs-1">{{!W6}}</div>
% setdefault('TH6','')
<div class="cal-cell col-xs-1">{{!TH6}}</div>
% setdefault('FR6','')
<div class="cal-cell col-xs-1">{{!FR6}}</div>
% setdefault('SA6','')
<div class="cal-cell col-xs-1">{{!SA6}}</div>
% setdefault('SU6','')
<div class="cal-cell col-xs-1">{{!SU6}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">7 am</span></div>
% setdefault('M7','')
<div class="cal-cell col-xs-1">{{!M7}}</div>
% setdefault('T7','')
<div class="cal-cell col-xs-1">{{!T7}}</div>
% setdefault('W7','')
<div class="cal-cell col-xs-1">{{!W7}}</div>
% setdefault('TH7','')
<div class="cal-cell col-xs-1">{{!TH7}}</div>
% setdefault('FR7','')
<div class="cal-cell col-xs-1">{{!FR7}}</div>
% setdefault('SA7','')
<div class="cal-cell col-xs-1">{{!SA7}}</div>
% setdefault('SU7','')
<div class="cal-cell col-xs-1">{{!SU7}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">8 am</span></div>
% setdefault('M8','')
<div class="cal-cell col-xs-1">{{!M8}}</div>
% setdefault('T8','')
<div class="cal-cell col-xs-1">{{!T8}}</div>
% setdefault('W8','')
<div class="cal-cell col-xs-1">{{!W8}}</div>
% setdefault('TH8','')
<div class="cal-cell col-xs-1">{{!TH8}}</div>
% setdefault('FR8','')
<div class="cal-cell col-xs-1">{{!FR8}}</div>
% setdefault('SA8','')
<div class="cal-cell col-xs-1">{{!SA8}}</div>
% setdefault('SU8','')
<div class="cal-cell col-xs-1">{{!SU8}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">9 am</span></div>
% setdefault('M9','')
<div class="cal-cell col-xs-1">{{!M9}}</div>
% setdefault('T9','')
<div class="cal-cell col-xs-1">{{!T9}}</div>
% setdefault('W9','')
<div class="cal-cell col-xs-1">{{!W9}}</div>
% setdefault('TH9','')
<div class="cal-cell col-xs-1">{{!TH9}}</div>
% setdefault('FR9','')
<div class="cal-cell col-xs-1">{{!FR9}}</div>
% setdefault('SA9','')
<div class="cal-cell col-xs-1">{{!SA9}}</div>
% setdefault('SU9','')
<div class="cal-cell col-xs-1">{{!SU9}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">10 am</span></div>
% setdefault('M10','')
<div class="cal-cell col-xs-1">{{!M10}}</div>
% setdefault('T10','')
<div class="cal-cell col-xs-1">{{!T10}}</div>
% setdefault('W10','')
<div class="cal-cell col-xs-1">{{!W10}}</div>
% setdefault('TH10','')
<div class="cal-cell col-xs-1">{{!TH10}}</div>
% setdefault('FR10','')
<div class="cal-cell col-xs-1">{{!FR10}}</div>
% setdefault('SA10','')
<div class="cal-cell col-xs-1">{{!SA10}}</div>
% setdefault('SU10','')
<div class="cal-cell col-xs-1">{{!SU10}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">11 am</span></div>
% setdefault('M11',[])
<div class="cal-cell col-xs-1"><ul>{{
	% for u in M11:
		<li>{{u}}</li>
	% end
}}</ul></div>
% setdefault('T11','')
<div class="cal-cell col-xs-1">{{!T11}}</div>
% setdefault('W11','')
<div class="cal-cell col-xs-1">{{!W11}}</div>
% setdefault('TH11','')
<div class="cal-cell col-xs-1">{{!TH11}}</div>
% setdefault('FR11','')
<div class="cal-cell col-xs-1">{{!FR11}}</div>
% setdefault('SA11','')
<div class="cal-cell col-xs-1">{{!SA11}}</div>
% setdefault('SU11','')
<div class="cal-cell col-xs-1">{{!SU11}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">12 pm</span></div>
% setdefault('M12','')
<div class="cal-cell col-xs-1">{{!M12}}</div>
% setdefault('T12','')
<div class="cal-cell col-xs-1">{{!T12}}</div>
% setdefault('W12','')
<div class="cal-cell col-xs-1">{{!W12}}</div>
% setdefault('TH12','')
<div class="cal-cell col-xs-1">{{!TH12}}</div>
% setdefault('FR12','')
<div class="cal-cell col-xs-1">{{!FR12}}</div>
% setdefault('SA12','')
<div class="cal-cell col-xs-1">{{!SA12}}</div>
% setdefault('SU12','')
<div class="cal-cell col-xs-1">{{!SU12}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">1 pm</span></div>
% setdefault('M13','')
<div class="cal-cell col-xs-1">{{!M13}}</div>
% setdefault('T13','')
<div class="cal-cell col-xs-1">{{!T13}}</div>
% setdefault('W13','')
<div class="cal-cell col-xs-1">{{!W13}}</div>
% setdefault('TH13','')
<div class="cal-cell col-xs-1">{{!TH13}}</div>
% setdefault('FR13','')
<div class="cal-cell col-xs-1">{{!FR13}}</div>
% setdefault('SA13','')
<div class="cal-cell col-xs-1">{{!SA13}}</div>
% setdefault('SU13','')
<div class="cal-cell col-xs-1">{{!SU13}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">2 pm</span></div>
% setdefault('M14','')
<div class="cal-cell col-xs-1">{{!M14}}</div>
% setdefault('W14','')
<div class="cal-cell col-xs-1">{{!W14}}</div>
% setdefault('TH14','')
<div class="cal-cell col-xs-1">{{!TH14}}</div>
% setdefault('FR14','')
<div class="cal-cell col-xs-1">{{!FR14}}</div>
% setdefault('SA14','')
<div class="cal-cell col-xs-1">{{!SA14}}</div>
% setdefault('SU14','')
<div class="cal-cell col-xs-1">{{!SU14}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">3 pm</span></div>
% setdefault('M15','')
<div class="cal-cell col-xs-1">{{!M15}}</div>
% setdefault('T15','')
<div class="cal-cell col-xs-1">{{!T15}}</div>
% setdefault('W15','')
<div class="cal-cell col-xs-1">{{!W15}}</div>
% setdefault('TH15','')
<div class="cal-cell col-xs-1">{{!TH15}}</div>
% setdefault('FR15','')
<div class="cal-cell col-xs-1">{{!FR15}}</div>
% setdefault('SA15','')
<div class="cal-cell col-xs-1">{{!SA15}}</div>
% setdefault('SU15','')
<div class="cal-cell col-xs-1">{{!SU15}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">4 pm</span></div>
% setdefault('M16','')
<div class="cal-cell col-xs-1">{{!M16}}</div>
% setdefault('T16','')
<div class="cal-cell col-xs-1">{{!T16}}</div>
% setdefault('W16','')
<div class="cal-cell col-xs-1">{{!W16}}</div>
% setdefault('TH16','')
<div class="cal-cell col-xs-1">{{!TH16}}</div>
% setdefault('FR16','')
<div class="cal-cell col-xs-1">{{!FR16}}</div>
% setdefault('SA16','')
<div class="cal-cell col-xs-1">{{!SA16}}</div>
% setdefault('SU16','')
<div class="cal-cell col-xs-1">{{!SU16}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">5 pm</span></div>
% setdefault('M17','')
<div class="cal-cell col-xs-1">{{!M17}}</div>
% setdefault('T17','')
<div class="cal-cell col-xs-1">{{!T17}}</div>
% setdefault('W17','')
<div class="cal-cell col-xs-1">{{!W17}}</div>
% setdefault('TH17','')
<div class="cal-cell col-xs-1">{{!TH17}}</div>
% setdefault('FR17','')
<div class="cal-cell col-xs-1">{{!FR17}}</div>
% setdefault('SA17','')
<div class="cal-cell col-xs-1">{{!SA17}}</div>
% setdefault('SU17','')
<div class="cal-cell col-xs-1">{{!SU17}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">6 pm</span></div>
% setdefault('M18','')
<div class="cal-cell col-xs-1">{{!M18}}</div>
% setdefault('T18','')
<div class="cal-cell col-xs-1">{{!T18}}</div>
% setdefault('W18','')
<div class="cal-cell col-xs-1">{{!W18}}</div>
% setdefault('TH18','')
<div class="cal-cell col-xs-1">{{!TH18}}</div>
% setdefault('FR18','')
<div class="cal-cell col-xs-1">{{!FR18}}</div>
% setdefault('SA18','')
<div class="cal-cell col-xs-1">{{!SA18}}</div>
% setdefault('SU18','')
<div class="cal-cell col-xs-1">{{!SU18}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">7 pm</span></div>
% setdefault('M19','')
<div class="cal-cell col-xs-1">{{!M19}}</div>
% setdefault('T19','')
<div class="cal-cell col-xs-1">{{!T19}}</div>
% setdefault('W19','')
<div class="cal-cell col-xs-1">{{!W19}}</div>
% setdefault('TH19','')
<div class="cal-cell col-xs-1">{{!TH19}}</div>
% setdefault('FR19','')
<div class="cal-cell col-xs-1">{{!FR19}}</div>
% setdefault('SA19','')
<div class="cal-cell col-xs-1">{{!SA19}}</div>
% setdefault('SU19','')
<div class="cal-cell col-xs-1">{{!SU19}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">8 pm</span></div>
% setdefault('M20','')
<div class="cal-cell col-xs-1">{{!M20}}</div>
% setdefault('T20','')
<div class="cal-cell col-xs-1">{{!T20}}</div>
% setdefault('W20','')
<div class="cal-cell col-xs-1">{{!W20}}</div>
% setdefault('TH20','')
<div class="cal-cell col-xs-1">{{!TH20}}</div>
% setdefault('FR20','')
<div class="cal-cell col-xs-1">{{!FR20}}</div>
% setdefault('SA20','')
<div class="cal-cell col-xs-1">{{!SA20}}</div>
% setdefault('SU20','')
<div class="cal-cell col-xs-1">{{!SU20}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">9 pm</span></div>
% setdefault('M21','')
<div class="cal-cell col-xs-1">{{!M21}}</div>
% setdefault('T21','')
<div class="cal-cell col-xs-1">{{!T21}}</div>
% setdefault('W21','')
<div class="cal-cell col-xs-1">{{!W21}}</div>
% setdefault('TH21','')
<div class="cal-cell col-xs-1">{{!TH21}}</div>
% setdefault('FR21','')
<div class="cal-cell col-xs-1">{{!FR21}}</div>
% setdefault('SA21','')
<div class="cal-cell col-xs-1">{{!SA21}}</div>
% setdefault('SU21','')
<div class="cal-cell col-xs-1">{{!SU21}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">10 pm</span></div>
% setdefault('M22','')
<div class="cal-cell col-xs-1">{{!M22}}</div>
% setdefault('T22','')
<div class="cal-cell col-xs-1">{{!T22}}</div>
% setdefault('W22','')
<div class="cal-cell col-xs-1">{{!W22}}</div>
% setdefault('TH22','')
<div class="cal-cell col-xs-1">{{!TH22}}</div>
% setdefault('FR22','')
<div class="cal-cell col-xs-1">{{!FR22}}</div>
% setdefault('SA22','')
<div class="cal-cell col-xs-1">{{!SA22}}</div>
% setdefault('SU22','')
<div class="cal-cell col-xs-1">{{!SU22}}</div>
 </div >
<div class="cal-row row">
<div class="cal-cell col-xs-2"><span class="clock">11 pm</span></div>
% setdefault('M23','')
<div class="cal-cell col-xs-1">{{!M23}}</div>
% setdefault('T23','')
<div class="cal-cell col-xs-1">{{!T23}}</div>
% setdefault('W23','')
<div class="cal-cell col-xs-1">{{!W23}}</div>
% setdefault('TH23','')
<div class="cal-cell col-xs-1">{{!TH23}}</div>
% setdefault('FR23','')
<div class="cal-cell col-xs-1">{{!FR23}}</div>
% setdefault('SA23','')
<div class="cal-cell col-xs-1">{{!SA23}}</div>
% setdefault('SU23','')
<div class="cal-cell col-xs-1">{{!SU23}}</div>
 </div >
 <div height = 256px width=100%><canvas id="fred" width=100% height=100%></canvas></div>

 <script type="module">import * as hello from '/static/dummy.js'; window.hello = hello;</script>


 </div>