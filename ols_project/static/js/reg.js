var csrftoken = $.cookie("csrftoken");
$(document).ready(function(){   
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
                if(res['permission'] == true){
                    
                }
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

});

function submit_form(){
      //提交
                        $.ajax({
                            type: 'post',
                            url: '/reg_investor/',
                            data: $("#reg_form").serialize(),
                            dataType: 'json',
                            success: function (res,state) {
                                console.log(res);
                            },
                            beforeSend: function (XmlHttpRequest) {
                                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        });
                    
}
