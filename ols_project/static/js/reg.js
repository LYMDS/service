$(document).ready(function(){

    var csrftoken = $.cookie("csrftoken");
	var app = new Vue({
        el : "#dataframe",
        data : {
            permission : json_data['permission'],
            session_id : json_data['session_id']
        }
	});
    $("#refush").bind("click",function () { //刷新
        $.ajax({
            type: 'post',
            url: '/reg_show/',
            data: null,
            dataType: 'json',
            success: function (res,state) {
                app.$data.session_id = res['session_id'];
                app.$data.permission = res['permission'];
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

    $("#submit").bind("click",function () {   //提交
        $.ajax({
            type: 'post',
            url: '/reg_investor/',
            data: $("#reg_form").serialize(),
            dataType: 'json',
            success: function (res,state) {
                if(res['status'] == true){window.location.href="/admin_login/";}
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

})