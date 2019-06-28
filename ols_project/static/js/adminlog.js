var csrftoken = $.cookie("csrftoken");
$(document).ready(function () {
    $("#but").button();
    $("#but").bind("click",function () {
        $.ajax({
            type: 'post',
            url: '/ajax/',//测试的视图
            data: $("#login").serialize(),
            dataType: 'json',
            success: function (res,state) {
                console.log(res);
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

    $("#dialog").dialog({
        //对话框设置
        autoOpen: false,
        height: 300,
        width: 350,
        model: true,
        title: '温馨提示！',
        show: 'slide',
        hide: 'slide',
    });
});
