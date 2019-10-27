jQuery.fn.animateAuto = function(prop, speed, callback) {
    var elem, height, width;
    return this.each(function(i, el) {
        el = jQuery(el), elem = el.clone().css({ "height": "auto", "width": "auto" }).appendTo("body");
        height = elem.css("height"),
            width = elem.css("width"),
            elem.remove();

        if (prop === "height")
            el.animate({ "height": height }, speed, callback);
        else if (prop === "width")
            el.animate({ "width": width }, speed, callback);
        else if (prop === "both")
            el.animate({ "width": width, "height": height }, speed, callback);
    });
}
$(window).ready(function() {
    $('.plegablePedido').click(function() {
        if ($(this).next().hasClass('desplegado')) {
            $(this).next().removeClass('desplegado').animate({ height: 0 }, 700);
        } else {
            $(this).next().addClass('desplegado').animateAuto("height", 700);
        }
    })
})