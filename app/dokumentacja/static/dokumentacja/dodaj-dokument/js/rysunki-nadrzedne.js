select_inwestycja = $('#id_inwestycja')
select_branza = $('#id_branza')
select_dokument_nadrzedny = $('#id_dokument_nadrzedny')

function change_form_select_rysunek_nadrzedny() {
    $.ajax({
        type: 'POST',
        url: url_ajax_rysunki_branzy,
        headers: {'X-CSRFToken': csrftoken},
        data: {'pk_inwestycja': select_inwestycja.val(), 'pk_branza': select_branza.val()},
        success: function(response) {
            var rysunki_json = JSON.parse(response["dokumenty_nadrzedne"]);
            select_dokument_nadrzedny.children().remove();
            select_dokument_nadrzedny.append(new Option("---------", ''));
            rysunki_json.forEach(function(item, index) {
                select_dokument_nadrzedny.append(new Option(item['fields']['nazwa'], item['pk']));
            })
        }   
    })
}

select_inwestycja.change(function() {
    if (Boolean(select_branza.val()) && Boolean(select_inwestycja.val())) {
        change_form_select_rysunek_nadrzedny()
    }
})
select_branza.change(function() {
    if (Boolean(select_branza.val()) && Boolean(select_inwestycja.val())) {
        change_form_select_rysunek_nadrzedny()
    }
})

