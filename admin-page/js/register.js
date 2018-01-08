function register() {
    var name = null;
    var email = null;
    var knock = null;
    var _pass = null;
    var uid = null;

    $.ajax({
        //door= None, user= None, num= None, loc = None, arg5


        url:'http://localhost:8080/generator?t=3&door='+name +
        '&user=' + email +
        '&num=' + knock +
        '&loc=' + _pass +
        '&arg5='+ uid,
        type: 'POST',
        success: function(json) {
            var obj = jQuery.parseJSON( json );
            //result: [res,message]
            alert(obj.result);
            //http redirect

        }
    });
}

function read() {

    $.get("/read_card", {})
        .done(function (uuid) {
            console.log(uuid);
        });


}

function measure() {

}

function stop_clock() {

}
