function makeTimer() {

	//var endTime = new Date("29 April 2018 9:56:00 GMT+01:00");
	var endTime = new Date("26 November 2021 19:00:00 GMT+05:30");
	endTime = (Date.parse(endTime) / 1000);

	var now = new Date();
	now = endTime;//(Date.parse(now) / 1000);

	var timeLeft = endTime - now;

	var days = Math.floor(timeLeft / 86400);
	var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
	var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
	var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

	if (hours < "10") { hours = "0" + hours; }
	if (minutes < "10") { minutes = "0" + minutes; }
	if (seconds < "10") { seconds = "0" + seconds; }
	if (days < "10") { days = "0" + days; }

	document.querySelector('.days-javascript').innerHTML = days;
	document.querySelector('.hours-javascript').innerHTML = hours;
	document.querySelector('.minutes-javascript').innerHTML = minutes;
	document.querySelector('.seconds-javascript').innerHTML = seconds;

	document.querySelector('.mobile-days-javascript').innerHTML = days;
	document.querySelector('.mobile-hours-javascript').innerHTML = hours;
	document.querySelector('.mobile-minutes-javascript').innerHTML = minutes;
	document.querySelector('.mobile-seconds-javascript').innerHTML = seconds;
}

setInterval(function () { makeTimer(); }, 1000);