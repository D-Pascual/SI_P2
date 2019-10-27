$(document).ready(function(){
    $("#clave").keyup(function(){
        if($(this).val().length < 8){
            $("#mensaje").text("No segura").css("color", "red");
        }
        else{
            if (/\d/.test($(this).val()) && /[A-Z]/.test($(this).val()) && /[a-z]/.test($(this).val())) {
                $("#mensaje").text("Muy segura").css("color", "green"); // Contiene al menos una minuscula, mayuscula y numero
            }
            else if (/[A-Z]/.test($(this).val()) && /[a-z]/.test($(this).val())) {
                $("#mensaje").text("Medianamente segura").css("color", "orange"); // Contiene al menos una minuscula y mayuscula 
            }
            else if (/\d/.test($(this).val()) && /[a-z]/.test($(this).val())) {
                $("#mensaje").text("Medianamente segura").css("color", "orange"); // Contiene al menos una minuscula y numero
            }
            else if (/\d/.test($(this).val()) && /[A-Z]/.test($(this).val())) {
                $("#mensaje").text("Medianamente segura").css("color", "orange"); // Contiene al menos un numero y mayuscula 
            }
            else{
                $("#mensaje").text("Poco segura").css("color", "yellow"); // Contiene solo de un tipo
            }
        }
    });
});
