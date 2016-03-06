$(function () {
	var helpers = Chart.helpers
	
    var talent_frail_other_percentage_options = {
        segmentShowStroke: true,
        segmentStrokeColor: "#fff",
        segmentStrokeWidth: 2,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
		tooltipTemplate : "<%if (label){%><%=label%>: <%}%><%= value %>"
    };

	var canvas = document.getElementById("talent_frail_other_percentage_chart")
    var chart_talent_frail_other_percentage = new Chart(canvas.getContext('2d')).Pie(talent_frail_other_percentage_data, talent_frail_other_percentage_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_talent_frail_other_percentage.generateLegend();
		// Include a html legend template after the module doughnut itself
		helpers.each(legendHolder.firstChild.childNodes, function(legendNode, index){
			helpers.addEvent(legendNode, 'mouseover', function(){
				var activeSegment = chart_talent_frail_other_percentage.segments[index];
				activeSegment.save();
				activeSegment.fillColor = activeSegment.highlightColor;
				chart_talent_frail_other_percentage.showTooltip([activeSegment]);
				activeSegment.restore();
			});
		});
		helpers.addEvent(legendHolder.firstChild, 'mouseout', function(){
			chart_talent_frail_other_percentage.draw();
		});
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);
	
    var male_female_percentage_options = {
        segmentShowStroke: true,
        segmentStrokeColor: "#fff",
        segmentStrokeWidth: 2,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
		tooltipTemplate : "<%if (label){%><%=label%>: <%}%><%= value %>"
    };

	var canvas = document.getElementById("male_female_percentage_chart")
    var chart_male_female_percentage = new Chart(canvas.getContext('2d')).Pie(male_female_percentage_data, male_female_percentage_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_male_female_percentage.generateLegend();
		// Include a html legend template after the module doughnut itself
		helpers.each(legendHolder.firstChild.childNodes, function(legendNode, index){
			helpers.addEvent(legendNode, 'mouseover', function(){
				var activeSegment = chart_male_female_percentage.segments[index];
				activeSegment.save();
				activeSegment.fillColor = activeSegment.highlightColor;
				chart_male_female_percentage.showTooltip([activeSegment]);
				activeSegment.restore();
			});
		});
		helpers.addEvent(legendHolder.firstChild, 'mouseout', function(){
			chart_male_female_percentage.draw();
		});
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);
	
	var talent_local_global_percentage_options = {
        segmentShowStroke: true,
        segmentStrokeColor: "#fff",
        segmentStrokeWidth: 2,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
		tooltipTemplate : "<%if (label){%><%=label%>: <%}%><%= value %>"
    };

	var canvas = document.getElementById("talent_local_global_percentage_chart")
    var chart_talent_local_global_percentage = new Chart(canvas.getContext('2d')).Pie(talent_local_global_percentage_data, talent_local_global_percentage_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_talent_local_global_percentage.generateLegend();
		// Include a html legend template after the module doughnut itself
		helpers.each(legendHolder.firstChild.childNodes, function(legendNode, index){
			helpers.addEvent(legendNode, 'mouseover', function(){
				var activeSegment = chart_talent_local_global_percentage.segments[index];
				activeSegment.save();
				activeSegment.fillColor = activeSegment.highlightColor;
				chart_talent_local_global_percentage.showTooltip([activeSegment]);
				activeSegment.restore();
			});
		});
		helpers.addEvent(legendHolder.firstChild, 'mouseout', function(){
			chart_talent_local_global_percentage.draw();
		});
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);
	
	var frail_local_global_percentage_options = {
        segmentShowStroke: true,
        segmentStrokeColor: "#fff",
        segmentStrokeWidth: 2,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
		tooltipTemplate : "<%if (label){%><%=label%>: <%}%><%= value %>"
    };

	var canvas = document.getElementById("frail_local_global_percentage_chart")
    var chart_frail_local_global_percentage = new Chart(canvas.getContext('2d')).Pie(frail_local_global_percentage_data, frail_local_global_percentage_options);
	
	var legendHolder = document.createElement('div');
	legendHolder.innerHTML = chart_frail_local_global_percentage.generateLegend();
		// Include a html legend template after the module doughnut itself
		helpers.each(legendHolder.firstChild.childNodes, function(legendNode, index){
			helpers.addEvent(legendNode, 'mouseover', function(){
				var activeSegment = chart_frail_local_global_percentage.segments[index];
				activeSegment.save();
				activeSegment.fillColor = activeSegment.highlightColor;
				chart_frail_local_global_percentage.showTooltip([activeSegment]);
				activeSegment.restore();
			});
		});
		helpers.addEvent(legendHolder.firstChild, 'mouseout', function(){
			chart_frail_local_global_percentage.draw();
		});
	canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);
});