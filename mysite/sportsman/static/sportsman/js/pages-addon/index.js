$(function () {
	var percentage_chart_options = {
        chart: {
            type: 'pie'
        },
		title: {
			text: '',
			style: {
				display: 'none'
			}
		},
		credits: {
			enabled: false
		},
        tooltip: {
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.y}</b>人'
                },
				showInLegend: true
            }
        }
    };
	
    $('#talent_frail_other_percentage_chart').highcharts($.extend({}, percentage_chart_options, {series: [{data: talent_frail_other_percentage_data}]}));
	$('#male_female_percentage_chart').highcharts($.extend({}, percentage_chart_options, {series: [{data: male_female_percentage_data}]}));
	
	$('#talent_local_global_percentage_chart').highcharts($.extend({}, percentage_chart_options, {series: [{data: talent_local_global_percentage_data}]}));
	$('#frail_local_global_percentage_chart').highcharts($.extend({}, percentage_chart_options, {series: [{data: frail_local_global_percentage_data}]}));
});