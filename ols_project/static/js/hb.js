/**
 * Created by lym_d on 2020/5/11.
 */
var csrftoken = $.cookie("csrftoken");
$(document).ready(function(){
	var app = new Vue({
        el : "#dataframe",
        data : {
            hardwarelist: []
        }
	});
	var t1=window.setInterval(refreshCount, 1000);
    function refreshCount() {
        $.ajax({
            type: 'get',
            url: '/hb/data/',
            data: null,
            dataType: 'json',
            success: function (res,state) {
                app.$data.hardwarelist = res['data'];
                console.log(res['data']);
            },
            beforeSend: function (XmlHttpRequest) {
                XmlHttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    }
});