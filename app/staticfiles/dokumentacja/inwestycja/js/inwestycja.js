$(document).ready(function() {
    $('#select-inwestycja').change(function() {
        if ($(this).val() == "dodaj") {
            let specs = "width=600,height=300,left=200,top=200"
            var dodaj_inwestycje_window = window.open(url_inwestycja_create, "MsgWindow", specs );
        } else if ($(this).val() != "") {
            url = $(this).find('option:selected').data('href')
            window.location.href = url;
        }
    })
})

function add_inwestycja_option(value, text) {
    let option = new Option(text, value, selected=true)
    let last_option = document.querySelector('#select-inwestycja option:last-child')
    select = document.querySelector('#select-inwestycja')
    select.insertBefore(option, last_option)
    select.value = value
}