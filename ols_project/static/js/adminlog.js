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


});
