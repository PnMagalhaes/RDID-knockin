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

        $('#dataTable tbody').on( 'click', 'input.btn', function () {
            console.log("in");
            var d = table.row($(this).parents('tr')).data();
            $("#exampleInputName").val(d[2]) ;
            $("#exampleInputEmail1").val(d[0]);
            $("#exampleInputPassword1").val(d[5]);

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
    $.ajax({
        url:'http://localhost:8080/generator?t=2&_id=' +  model_door+ '&num=' + $("#exampleInputName").val()
        + '&loc='+ $("#exampleInputEmail1").val()+ '&arg1='+ $("#exampleInputPassword1").val(),
        type: 'PUT',
        success: function(json) {
            var obj = jQuery.parseJSON( json );
            //result: [res,message]
            alert(obj.result[1]);
            if (obj.result[0]){
                //close modal
                $('#myModal').modal('hide');
                table.ajax.reload();
            }

        }
    });

    //$('#myModal').modal('hide');
}