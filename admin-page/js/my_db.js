var table, t_doors;
$(document).ready(
    function() {
        console.log("not empty");
        t_doors = $("#dataTable").DataTable({
            ajax: {
                url: 'http://localhost:8080/generator?t=1',
                dataSrc: 'data'

            }
        });
        table = $('#users_per_door').DataTable();
    });
var selected_door = 0;
function selectDoor(door_db_id) {
    console.log(door_db_id);

    //update to use as a global value
    selected_door = door_db_id;

    //destroy old table
    table.destroy();

    table = $('#users_per_door').DataTable({
        ajax: {
            url: 'http://localhost:8080/generator?t=2&doorId='+ door_db_id,
            dataSrc: 'data'

        }
    });

    $('#users_table').css("visibility","visible");

    $('#users_per_door tbody').on( 'click', 'button.btn', function () {
        var d = table.row($(this).parents('tr')).data();
        var user_id_db = d[0];
        console.log(d);
        table
            .row( $(this).parents('tr') )
            .remove()
            .draw();

        $.ajax({
            url:'http://localhost:8080/generator?door='+selected_door +'&user='+ user_id_db,
            type: 'DELETE',
            success: function(json) {
                var obj = jQuery.parseJSON( json );
                //result: message
                alert(obj.result);
                t_doors.ajax.reload();

            }
        });

    } );
    /*$.get("/generator", {"doors": true})
        .done(function(json) {

            var obj = jQuery.parseJSON( json );
            var list = obj.result;
            var string = "";
            var i;
            for (i = 0; i < list.length; i++){
                var row = list[i];

                string += "<tr><td>" + row[0] +
                    "</td><td>" + row[1] +
                    "</td><td>" + row[2] +
                    "</td><td>" + row[3] +
                    "</td><td>" + row[4] +
                    "</td><td>" + "del" +
                    "</td></tr>";
            }
            $("#all_doors").html(string);

            console.log(list);

        });*/
}

function add_user(db_door_id) {
    var db_user_id;
    var person = prompt("Email:", "example@ua.pt");

    $.get("/generator", {"t": 3, "email":  person })
        .done(function(json) {
            var obj = jQuery.parseJSON( json );
            //result: [<db id user>]
            db_user_id = obj.result;
            console.log(db_user_id);

            if(db_user_id== []){
                alert("No user found with this email!");
            }
            else{
                //retrive ID
                db_user_id = db_user_id[0];
                $.post("/generator", {"door": db_door_id, "user": db_user_id})
                    .done(function(json) {
                        var obj = jQuery.parseJSON( json );
                        //result: message
                        alert(obj.result);
                        t_doors.ajax.reload();
                        table.ajax.reload();

                    });
            }
        });


}

var model_door = null;

function edit_door(door) {
    //show values
    //$('#txt_num').val();
    //$('#txt_loc').val("");

    //Display modal
    $('#myModal').modal('show');
    //update global variable
    model_door = door;
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
    });
}