$(document).ready(function() {
    $('#uprawnienia-form').submit(function(e) {

    })
    $('#uprawnienia-form input[type=checkbox]').change(function() {
        let value = $(this).is(':checked');
        let target = $(this).data('target');
        console.log(value)
        console.log($(this).parent().find('input[type=hidden]').val(value))
    })
})

$(document).ready(function() {

    $('#add-row-uprawnienia').click(function() {
        let row = document.querySelector('.sample-row-uprawnienia').cloneNode(true);
        row.classList.remove('hidden');
        document.querySelector('table.uprawnienia tbody').append(row);
        $('#uprawnienia-form input[type=checkbox]').change(function() {
            let value = $(this).is(':checked');
            let target = $(this).data('target');
            console.log(value)
            console.log($(this).parent().find('input[type=hidden]').val(value))
        })
    })
    $('#del-row-uprawnienia').click(function() {
        document.querySelector('table.uprawnienia tbody tr.sample-row-uprawnienia:last-child').remove()
    })
})