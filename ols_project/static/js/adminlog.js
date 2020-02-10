var csrftoken = $.cookie("csrftoken");
$(document).ready(function () {
    $("#but").button();
    $("#but").bind("click",function () {
        $.ajax({
            type: 'post',
            url: '/ajax/',
            data: $("#reg_form").serialize(),
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
        height: "auto",
        width: "auto",
        modal: true,
        title: '温馨提示！',
        show: 'slide',
        hide: 'slide',
    });
});
