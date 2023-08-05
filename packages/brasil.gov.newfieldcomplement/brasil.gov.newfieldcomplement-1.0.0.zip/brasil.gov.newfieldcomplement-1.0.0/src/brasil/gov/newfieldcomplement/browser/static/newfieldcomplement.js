$(document).ready(function(){

    // tratamento da coluna direita vazia
    if (!$.trim($('div#faceted-right-column').html())) {
        $('div#center-content-area').addClass('no-right-margin')
    }

});
