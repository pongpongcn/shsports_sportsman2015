$(function () {
	var helpers = Chart.helpers
	
    var percentage_chart_options = {
        segmentShowStroke: true,
        segmentStrokeColor: "#fff",
        segmentStrokeWidth: 2,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
		tooltipTemplate : "<%= value %>人",
		onAnimationComplete: function () {
			this.showTooltip(this.segments, true);
		},
		tooltipFillColor: "rgba(0,0,0,0.1)",
		tooltipEvents: [],
		showTooltips: true
    };

	var canvas = document.getElementById("talent_frail_other_percentage_chart")
    var chart_talent_frail_other_percentage = new Chart(canvas.getContext('2d')).Pie(talent_frail_other_percentage_data, percentage_chart_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_talent_frail_other_percentage.generateLegend();
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);


	var canvas = document.getElementById("male_female_percentage_chart")
    var chart_male_female_percentage = new Chart(canvas.getContext('2d')).Pie(male_female_percentage_data, percentage_chart_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_male_female_percentage.generateLegend();
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);


	var canvas = document.getElementById("talent_local_global_percentage_chart")
    var chart_talent_local_global_percentage = new Chart(canvas.getContext('2d')).Pie(talent_local_global_percentage_data, percentage_chart_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_talent_local_global_percentage.generateLegend();
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);


	var canvas = document.getElementById("frail_local_global_percentage_chart")
    var chart_frail_local_global_percentage = new Chart(canvas.getContext('2d')).Pie(frail_local_global_percentage_data, percentage_chart_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_frail_local_global_percentage.generateLegend();
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);
});