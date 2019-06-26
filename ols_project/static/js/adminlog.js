var csrftoken = $.cookie("csrftoken");
$(document).ready(function () {
    $(".log_But").bind("click",function () {
        $.ajax({
            type: 'post',
            url: '/ajax/',
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

    $("#but").button();
    $("#but").bind("click", function () {
        console.log('我是一个按钮');
        $("#dialog").dialog("open");

    });
    
    $("#dialog").dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        model: true,
        title: '温馨提示！',
        show: 'slide',
        hide: 'slide',

    });

});
