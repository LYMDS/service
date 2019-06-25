$(document).ready(function () {
    $(".log_But").bind("click",function () {
        $.ajax({
            type: 'get',
            url: '/ajax/',
            dataType: 'json',
            success: function (res,state) {
                console.log(res);
            }
        });
    });
});
