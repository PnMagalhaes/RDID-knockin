$(document).ready(
    function() {



    });


function register() {
    var name = $("#exampleInputName").val() + " "+ $("#exampleInputLastName").val();
    var email = $("#exampleInputEmail1").val();
    var knock = k_list;
    var _pass = $("#exampleInputPassword1").val();
    var uid = $("#feedback").val();

    $.get("/post", {"t":3, "name": name, "email": email, "knock": "[" + knock + "]" , "_pass": _pass, "uid": uid})
    .done(function(json) {

        console.log(json);
        var obj = jQuery.parseJSON(json);
        //result: [res,message]
        alert(obj.result);
        //http redirect


    });
}

var old_measure = null;
var k_list = []; //knock list

function read() {
    $.get("http://localhost:8080/read_card", {})
        .done(function (uuid) {
            console.log(uuid);
            var obj = jQuery.parseJSON(uuid);
            $("#feedback").text(obj.result);

        });


}

function measure() {
    if (old_measure == null){
        //time
        old_measure = new Date().getTime() ;
        console.log(old_measure);
    }
    else{

        var tmp = new Date().getTime() ; //time
        //calculate difference
        var difference = tmp - old_measure;
        var secondsDifference = Math.floor(difference/1000);
        var miliDiff = Math.floor(difference);
        console.log(miliDiff);
        k_list.push(miliDiff);
        //update old_me...
        old_measure = tmp;
    }

}

function stop_clock() {

    console.log(k_list);
    $("#feedback2").text(k_list);
}

