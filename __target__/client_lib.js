// Transcrypt'ed from Python, 2019-05-18 19:39:38
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var STATUS = dict ({});
export var set_status = function (blob) {
	STATUS = blob;
};
export var get_status = function () {
	return STATUS;
};
export var DAY_HRS = tuple (range (8, 22));
export var DAY_E = 'hsl(46, 18%, 96%)';
export var DAY_O = 'hsl(151, 20%, 92%)';
export var NIGHT_E = 'hsl(46, 20%, 87%)';
export var NIGHT_O = 'hsl(151, 30%, 85%)';
export var DIVIDER = 'hsl(180, 0%, 100%, 0.33)';
export var BACKGROUND = '#FFFFFF';
export var MARGIN = 30;
export var HOUR_OFFSET = 4;
export var HR_FONT = '12px Arial';
export var HR_LABEL = 'hsl(180,0%,45%)';
export var DAY_FONT = '18px Arial Black';
export var DAY_LABEL = 'hsl(180,0%,10%)';
export var USER_COLORS = tuple (['hsl(0,50%,50%, 0.25', 'hsl(90,50%,50%, 0.25', 'hsl(180,50%,50%, 0.25', 'hsl(270,50%,50%, 0.25']);
export var BLACKOUT_COLOR = 'hsl(0, 33%, 33%, 0.33)';
export var NOW_COLOR = 'hsl(0, 50%, 60%, 0.75)';
export var hour_color = function (hour, day) {
	var evenodd = __mod__ (day, 2) == 0;
	if (__in__ (hour, DAY_HRS)) {
		if (evenodd) {
			return DAY_E;
		}
		else {
			return DAY_O;
		}
	}
	else if (evenodd) {
		return NIGHT_E;
	}
	else {
		return NIGHT_O;
	}
};
export var draw_calendar = function () {
	var canvas = document.getElementById ('calendar_canvas');
	var w = canvas.scrollWidth;
	var h = canvas.scrollHeight;
	var ctx = canvas.getContext ('2d');
	var draw_rect = function (rect, fillStyle) {
		var left = rect [0] * (w - 2 * MARGIN) + MARGIN;
		var right = rect [2] * (w - 2 * MARGIN) + MARGIN;
		var top = rect [1] * h;
		var bottom = rect [3] * h;
		ctx.fillStyle = fillStyle;
		ctx.fillRect (left, top, right - left, bottom - top);
	};
	draw_rect (tuple ([0, 0, 1, 1]), BACKGROUND);
	for (var day = 0; day < 7; day++) {
		var lf = day / 7;
		var r = (day + 1) / 7;
		for (var hour = 1; hour < 25; hour++) {
			var top = hour / 25;
			var bottom = (hour + 1) / 25;
			draw_rect (tuple ([lf, top, r, bottom]), hour_color (hour, day));
		}
	}
	ctx.font = HR_FONT;
	ctx.fillStyle = HR_LABEL;
	for (var i = 1; i < 24; i++) {
		if (__mod__ (i, 2) == 0) {
			var divider = ((i + 1) / 25) * h + HOUR_OFFSET;
			var hr = __mod__ (i, 12) || 'Noon';
			if (__mod__ (i, 12) < 10 && hr != 'Noon') {
				var hr = str (' {}').format (hr);
			}
			if (i > 12) {
				hr += ' p';
			}
			else if (i < 12) {
				hr += ' a';
			}
			ctx.fillText (hr, 2, divider);
		}
	}
	if (w < 512) {
		var names = tuple (['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']);
	}
	else {
		var names = tuple (['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
	}
	ctx.font = DAY_FONT;
	ctx.fillStyle = DAY_LABEL;
	for (var [i, t] of enumerate (names)) {
		var lf = int (((i + 0.5) / 7) * (w - 2 * MARGIN) + MARGIN);
		var size = int (ctx.measureText (t).width / 2);
		ctx.fillText (t, lf - size, 18, int (w / 7));
	}
	var status = dict (get_status ());
	var user_count = len (status.py_keys ());
	for (var [idx, user] of enumerate (status.py_keys ())) {
		var intervals = status [user] ['intervals'];
		for (var i of intervals) {
			var __left0__ = i [0];
			var day1 = __left0__ [0];
			var hr1 = __left0__ [1];
			var min1 = __left0__ [2];
			var __left0__ = i [1];
			var day2 = __left0__ [0];
			var hr2 = __left0__ [1];
			var min2 = __left0__ [2];
			var offset = idx / user_count;
			var left = (day1 + offset) / 7;
			var right = ((day2 + offset) + 1 / user_count) / 7;
			var top = ((1 + hr1) + min1 / 60) / 25;
			var bottom = ((1 + hr2) + min2 / 60) / 25;
			draw_rect (tuple ([left, top, right, bottom]), USER_COLORS [__mod__ (idx, 4)]);
		}
		var blackouts = status [user] ['blackouts'];
		for (var i of blackouts) {
			var __left0__ = i [0];
			var day1 = __left0__ [0];
			var hr1 = __left0__ [1];
			var min1 = __left0__ [2];
			var __left0__ = i [1];
			var day2 = __left0__ [0];
			var hr2 = __left0__ [1];
			var min2 = __left0__ [2];
			var offset = idx / user_count;
			var left = (day1 + offset) / 7;
			var right = ((day2 + offset) + 1 / user_count) / 7;
			var top = ((1 + hr1) + min1 / 60) / 25;
			var bottom = ((1 + hr2) + min2 / 60) / 25;
			draw_rect (tuple ([left, top, right, bottom]), BLACKOUT_COLOR);
		}
	}
	ctx.strokeStyle = DIVIDER;
	for (var i = 1; i < 25; i++) {
		var divider = (i / 25) * h;
		ctx.beginPath ();
		ctx.moveTo (0, divider);
		ctx.lineTo (w, divider);
		ctx.moveTo (w, divider + 1);
		ctx.lineTo (0, divider + 1);
		ctx.stroke ();
	}
	var now = new Date ();
	var hour = now.getHours () + now.getMinutes () / 60;
	var divider = (hour + 1) / 25;
	draw_rect (tuple ([0, divider - 0.005, 1, divider + 0.005]), NOW_COLOR);
};
export var resize_handler = function () {
	var frame = document.getElementById ('frame');
	var canvas = document.getElementById ('calendar_canvas');
	var w = frame.scrollWidth;
	canvas.width = w - 32;
	canvas.height = 25 * 20;
	draw_calendar ();
	print ('resized');
};
export var show_times = function () {
	var names = document.getElementById ('names');
	while (names.firstChild) {
		names.removeChild (names.firstChild);
	}
	var status = get_status ();
	for (var [idx, u] of enumerate (status.py_keys ())) {
		var sp = document.createElement ('BUTTON');
		sp.innerHTML = (u + ':') + status [u] ['credits'];
		sp.style.backgroundColor = USER_COLORS [idx];
		sp.style.border = 'None';
		sp.style.color = 'White';
		sp.style.textAlign = 'left';
		sp.style.margin = '0px 8px';
		sp.style.font = '14px Arial';
		sp.style.width = '24%';
		names.appendChild (sp);
	}
};
if (__name__ == '__main__') {
	resize_handler ();
	window.onresize = resize_handler;
	show_times ();
	print ('LOADED');
}

//# sourceMappingURL=client_lib.map