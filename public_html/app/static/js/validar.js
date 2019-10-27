function validarRegistro() { //Comprobar si las contraseñas coinciden
    var pass = document.forms["registro"]["password"].value;
    var conf_pass = document.forms["registro"]["conf_password"].value;
    if(pass != conf_pass){
        alert("¡Las contraseñas no coinciden!");
        return false;
    }
}