// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// -- Bar Chart Example
var ctx = document.getElementById("myAreaChart");
var year_chart;
var table;
$(document).ready(
    function() {
        table = $("#dataTable").DataTable({
            ajax: {
                url: 'http://localhost:8080/generator?t=9',
                dataSrc: 'data'

            }
        });

        setInterval(function() {
            table.ajax.reload();
        }, 5000 );

    });
var x_label, y_label;
$.get("/generator", {"t": 6, "d1":  2017 }) .done(function(json) {
    var obj = jQuery.parseJSON( json );
    //result: [<db id user>]
    var tmp = obj.result;
    x_label = tmp.x;
    y_label = tmp.y;

    year_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x_label,
            datasets: [{
                label: "2017",
                lineTension: 0.3,
                backgroundColor: "rgba(2,117,216,0.2)",
                borderColor: "rgba(2,117,216,1)",
                pointRadius: 5,
                pointBackgroundColor: "rgba(2,117,216,1)",
                pointBorderColor: "rgba(255,255,255,0.8)",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(2,117,216,1)",
                pointHitRadius: 20,
                pointBorderWidth: 2,
                data: y_label,
            }],
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,

                    }
                }]
            }
        }
    });
});


function draw() {
    var label = "";
    var parameters = {};
    if($("#user_opt").is(':checked') && $("#door_opt").is(':checked') ){
        users = $("#user_id").val();
        doors = $("#door_id").val();
        parameters = {"user": users, "doorId": doors} ;
        label = " User: " + users + ", Door: " + doors;
    }
    else if($("#user_opt").is(':checked')) {
        users = $("#user_id").val();
        parameters = {"user": users} ;
        label = " User: " + users ;
    }
    else if($("#door_opt").is(':checked') ){
        doors = $("#door_id").val();
        parameters = {"doorId": doors} ;
        label = " Door: " + doors;
    }


    if( $("#years_opt").is(':checked') ){
        parameters["d1"] = $("#begin_year").val();
        parameters["d2"] = $("#end_year").val();
        label = "From " + parameters["d1"] + " to " + parameters["d2"] + label ;
        parameters["t"] = 5;
    }
    else if($("#year_opt").is(':checked')){
        parameters["d1"] =  $("#year").val();
        label = "Year " + parameters["d1"] + label ;
        parameters["t"] = 6;
    }
    else if( $("#month_opt").is(':checked') ){
        parameters["d1"] =  $("#month").val();
        label = "Date  " + parameters["d1"] + label ;
        parameters["t"] = 7;
    }
    else if( $("#day_opt").is(':checked') ){
        parameters["d1"] =  $("#day").val();
        parameters["t"] = 8;
        label = "Date  " + parameters["d1"] + label ;
    }

    console.log(parameters);
    $.get("/generator", parameters) .done(function(json) {
        var obj = jQuery.parseJSON( json );
        //result: [<db id user>]
        var tmp = obj.result;
        x_label = tmp.x;
        y_label = tmp.y;
        year_chart.destroy();
        year_chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: x_label,
                datasets: [{
                    label: label,
                    lineTension: 0.3,
                    backgroundColor: "rgba(2,117,216,0.2)",
                    borderColor: "rgba(2,117,216,1)",
                    pointRadius: 5,
                    pointBackgroundColor: "rgba(2,117,216,1)",
                    pointBorderColor: "rgba(255,255,255,0.8)",
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(2,117,216,1)",
                    pointHitRadius: 20,
                    pointBorderWidth: 2,
                    data: y_label,
                }],
            },
            options: {
                responsive: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0,

                        }
                    }]
                }
            }
        });
    });


}