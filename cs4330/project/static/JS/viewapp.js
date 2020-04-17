    function accept_or_reject(id, status){
        document.getElementById("id_app_id").value = id;
        document.getElementById("id_status").value = status;
        document.getElementById("applyform").submit();
    };

    function accept(id){
        accept_or_reject(id, "ACCEPTED");
    };
    function reject(id){
        accept_or_reject(id, "REJECTED");
    };