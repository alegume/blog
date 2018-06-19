// quando o document estiver ready
$(function() {
    $('#conteudo').hide();
    $('#id_input').focus();
    /// AJAX (Asynchronous JavaScript and XML)
    // Mas sem XML ;P
    $('form').submit(function(e) {
        e.preventDefault();
        let url = $('#url').attr('data-url').slice(0, -1);
        let id = $('#id_input').val();
        $.get(url + id, function(response) {
            console.log(response);
            if (!response.status) {
                $('#conteudo').fadeOut()
                return;
            }
            $('#id').text(response.id);
            $('#title').text(response.title);
            $('#text').text(response.text);
            $('#conteudo').fadeIn();
        });
    });

    $('#trash').click(function(e) {
        e.preventDefault();
        let url = $('#trash').attr('href').slice(0, -1);
        let id = $('#id_input').val();

        $.post(url + id, function(response) {
            console.log(response);
            if (response.status) {
                $('#conteudo').fadeOut()
            } else {
                console.log("Erro!");
            }

        });
    });
    

});