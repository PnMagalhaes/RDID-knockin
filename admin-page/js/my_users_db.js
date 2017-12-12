var table;
$(document).ready(
    function() {
        console.log("not empty");
        table = $("#dataTable").DataTable({
            ajax: {
                url: 'http://localhost:8080/generator?t=4',
                dataSrc: 'data'

            }
        });

    });

var model_user = null;

function edit_user(door) {
    //show values
    //$('#txt_num').val();
    //$('#txt_loc').val("");

    //Display modal
    $('#myModal').modal('show');
    //update global variable
    model_user = door;
}

function update_user() {
    /*try{
        var num = parseInt($('#text_num').val());
    }catch(err){
        alert("ERROR: Number not integer!");
        return;
    }
    var loc = $('#text_loc').val();


    $.ajax({
        url:'http://localhost:8080/generator?_id=' +  model_door+ '&num=' + num + '&loc='+ loc,
        type: 'PUT',
        success: function(json) {
            var obj = jQuery.parseJSON( json );
            //result: [res,message]
            alert(obj.result[1]);
            if (obj.result[0]){
                //close modal
                $('#text_num').val("");
                $('#text_loc').val("");
                $('#myModal').modal('hide');
                t_doors.ajax.reload();
            }

        }
    });*/

    $('#myModal').modal('hide');
}