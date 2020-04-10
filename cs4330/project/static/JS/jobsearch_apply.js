
function goto_or_apply(s){
    document.getElementById("id_job_id").value = s;
    document.getElementById("applyform").submit();
}

function success_message(flag){
    if(flag == 'True'){
        document.getElementById("success").style.display='block';
        setTimeout(function(){document.getElementById("success").style.display='none';}, 3000);
    } else {
        document.getElementById("success").style.display="none";
    }
}