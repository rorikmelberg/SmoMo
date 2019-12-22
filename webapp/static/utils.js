'use strict';

window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

function Padder(len, pad) {
	if (len === undefined) {
	  len = 1;
	} else if (pad === undefined) {
	  pad = '0';
	}
  
	var pads = '';
	while (pads.length < len) {
	  pads += pad;
	}
  
	this.pad = function (what) {
	  var s = what.toString();
	  return pads.substring(0, pads.length - s.length) + s;
	};
  }