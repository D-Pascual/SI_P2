function conectados() {
    $(document).ready(function(){
        $.getJSON($SCRIPT_ROOT + '/connectedUsers', function(data){
            $("#numUsers").text(data.result);
        });
    });
}
conectados();
setInterval(conectados, 3000);