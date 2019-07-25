$(document).ready(function(){
    console.log(json_data);
    var csrftoken = $.cookie("csrftoken");
	var app = new Vue({
        el : "#dataframe",
        data : {
            permission : json_data['permission'],
            session_id : json_data['session_id']
        }
	});
    $("#but").bind("click",function () {
        $.ajax({
            type: 'post',
            url: '/reg_investor/',
            data: $("#login").serialize(),
            dataType: 'json',
            success: function (res,state) {
                console.log(res);
                app.$data.session_id = res['session_id'];
                app.$data.permission = res['permission'];
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });
})