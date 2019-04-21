function change_payload(){
	var dom = document.getElementById("payload");
	var hide = document.querySelectorAll(".hide");
	if (dom.value[1]=='c'){
		dom.value = "Sqa0000000000000000T";
		for (i=0;i<16;i+=1){
		hide[i].style.display="inline";}
		alert("已改为取车命令，请按您的需要稍加修改");
	}
	else{
		dom.value = "Sc00000000000000000T";
		for (i=0;i<16;i+=1){
		hide[i].style.display="none";}
		alert("已改为查询命令，请按您的需要稍加修改");
	}
}
function refresh(){location.reload()}

function T(str){
	var dom = document.getElementById("payload");
	var a = dom.value.split("");
	a.splice(2,1,str);
	dom.value = a.join("");
	}


function C(i){
	var dom = document.getElementById("payload");
	var a = dom.value.split("");
	if(a[i]=="0"){
		a.splice(i,1,"b");
	}
	else{
	a.splice(i,1,"0");
	}
	dom.value = a.join("");
}




