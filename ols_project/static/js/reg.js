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
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

});

function submit_form(){
    var per = $("#reg_form").serialize();
    //密码强度正则，最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
    // var pPattern = /^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/;
    // 输出 true
    // console.log("=="+pPattern.test("iFat3#"));

    // 最短8位，最长16位 {6,16}
    // 可以包含小写大母 [a-z] 和大写字母 [A-Z]
    // 可以包含数字 [0-9]
    // 可以包含下划线 [ _ ] 和减号 [ - ]
    var pPattern = /^[\w_-]{8,16}$/;
    var uPattern = /^[a-zA-Z0-9_-]{4,16}$/;     //用户名正则，4到16位（字母，数字，下划线，减号）
    var Uallow = uPattern.test(per['username']);
    var Pallow = pPattern.test(per['password']);
    if(Uallow == true && Pallow == true){
        $.ajax({  //提交
            type: 'post',
            url: '/reg_investor/',
            data: per,
            dataType: 'json',
            success: function (res,state) {
                switch (res["status"]){
                    case "200" : window.location.href="/admin_login/";break;
                    case "404" : alert("404");break;
                    case "500" : alert("500");
                    // 404 : 未经管理员授权
                    // 500 : 账号名已存在
                    // 200 : 完成注册动作
                }
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    }
    else{
        alert("用户名与密码不符合！");
    }

                    
}
