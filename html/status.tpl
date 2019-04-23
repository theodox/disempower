% rebase('base.tpl', title='Disempower Login')
% include('header.tpl', title='Disempower Login')

<div class="card-body">
%for key in context:
    %try:
    	<div>
        {{ key }} :  {{ context[key] }}
        </div>
    %except KeyError:
        %continue
    %end
%end
</div>