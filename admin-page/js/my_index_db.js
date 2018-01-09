$(document).ready(    function() {

    $.get("/generator", {"t": 10})
        .done(function (json) {
            console.log(json);
            var obj = jQuery.parseJSON(json);
            //result: [<db id user>]
            result = obj.result;
            $("#icon1").text(result["users"]);
            $("#icon2").text(result["active_u"]);
            $("#icon3").text(result["doors"]);
            $("#icon4").text(result["active_d"]);

        });

    var table = $("#dataTable").DataTable({
        ajax: {
            url: 'http://localhost:8080/generator?t=11',
            dataSrc: 'data'

        }
    });

    setInterval(function() {
        table.ajax.reload();
    }, 3000 );



})

function add_door() {
    //Display modal
    $('#myModal').modal('show');

}

function update_door() {
    try{
        var num = parseInt($('#text_num').val());
    }catch(err){
        alert("ERROR: Number not integer!");
        return;
    }
    var loc = $('#text_loc').val();


    $.ajax({
        url:'http://localhost:8080/generator?t=2&num=' + num + '&loc='+ loc,
        type: 'POST',
        success: function(json) {
            var obj = jQuery.parseJSON( json );
            //result: [res,message]
            alert(obj.result);
            $('#myModal').modal('hide');

        }
    });
}