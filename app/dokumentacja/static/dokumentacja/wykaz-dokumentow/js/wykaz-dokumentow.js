function show_toast(text) {
    let container = $('.toast-container');
    let toast_el = document.querySelector('.toast.pattern').cloneNode(true);
    let toast_body = toast_el.querySelector('.toast-body');
    toast_body.innerHTML = text;  
    let el = new bootstrap.Toast(toast_el)
    container.append(toast_el)
    el.show()
}


$(document).ready(function(){
    $("#search").on("keyup", function() {
    var values = $(this).val().toLowerCase().split(' ');
        $("table.wykaz-dokumentow tbody tr").filter(function() {
            var mat = true
            var txt = $(this).text().toLowerCase()
            values.forEach(function(item, index) {
                mat *= txt.indexOf(item) > -1
            })
            $(this).toggle(Boolean(mat))
        });
    });
});

$(document).ready(function() {
    $('#filter-zastosuj').click(function() {
        req_get_string = '?';
        $('#filter-inwestycja, #filter-branza, #filter-status, #filter-nieaktualne, #filter-zarchiwizowane').each(function(index, element) {
            console.log($(element))
            let name = $(element).data('name');
            let values = [];
            $(element).find('input:checked').each(function() {
                values.push($(this).val())
            })
            req_get_string += name + '=' + values.join() + '&';
            console.log(values)
            console.log(req_get_string)
        });
        $('#filter-data_dodania, #filter-data_dokumentu').each(function(index, element) {
            let name = $(element).data('name');
            let values = [];
            let from = $(element).find('input[name="od"]').val().replace(/-/g,'');
            let to = $(element).find('input[name="do"]').val().replace(/-/g,'');
            req_get_string += name + '=' + from + "-" + to + "&";
        });
        window.location.href = req_get_string;
    });
})

$(document).ready(function() {
    $('#akcje input[type="submit"]').click(function() {
        let selected = $('#select-akcje option:selected');
        let action = selected.data('action');
        let url = selected.data('href');
        let val = selected.val();
        let pk = [];
        $('table.wykaz-dokumentow input[type=checkbox][name=action]:checked').each(function(index, item) {
            pk.push($(item).data('pk'));
        })
        pk = pk.join(',');

        if (action == 'update_status' || action == 'update_zarchiwizowany') {
            $.ajax({
                type: 'POST',
                url: url,
                headers: {'X-CSRFToken': csrftoken},
                data: { 'value': val,
                        'pk': pk,
                        'action': action},
            }).done(function(request) {
                if (request.info) {
                    show_toast(request.info);
                }
                if (request.errors) {
                    let msg = '<span class="text-danger">' + request.errors[0] + '</span>'
                    show_toast(msg);
                }
            }).fail(function(request) {
                let msg = '<span class="text-danger">Coś poszło nie tak</span>'
                show_toast(msg)
            })
        }

        if (action == 'download_files') {
            var form = document.createElement("form");
            form.style = 'display:none;';
            var el_pk = document.createElement("input");
            var el_action = document.createElement("input");
            var el_csrf = document.createElement("input");

            form.method = "POST";
            form.action = url; 
            
            el_csrf.value=csrftoken;
            el_csrf.name="csrfmiddlewaretoken";
            form.appendChild(el_csrf);  
        
            el_pk.value=pk;
            el_pk.name="pk";
            form.appendChild(el_pk);

            el_action.value=action;
            el_action.name="action";
            form.appendChild(el_action);
        
            document.body.appendChild(form);
            console.log(form)
        
            form.submit();
        }
    })
})


var last_check_action_click_index;
var shift_press = false;

$(document).ready(function() {
    $(window).keydown(function(e) {
        if (e.keyCode == 16) {
            shift_press = true
        }
    }).keyup(function(e) {
        if (e.keyCode == 16) {
            shift_press = false
        }
    })
    
    var $children = $('table.wykaz-dokumentow input[type=checkbox][name=action]').click(function() {
        
        let this_index = $children.index(this)

        if (shift_press) {
            if (last_check_action_click_index < this_index) {
                var elem = $children.slice(last_check_action_click_index, this_index+1);
            } else {
                var elem = $children.slice(this_index, last_check_action_click_index+1);
            }


            if ($(this).is(":checked")) {
                elem.prop( "checked", true)
            } else {
                elem.prop( "checked", false)
            }
        }

        $('table.wykaz-dokumentow tr:hidden').find('input[type=checkbox][name=action]').prop( "checked", false)
        
        last_check_action_click_index = this_index;
    })

    $('#table-select-all').change(function() {
        let all_val = $(this).is(":checked")
        $children.prop("checked", all_val)
        $('table.wykaz-dokumentow tr:hidden').find('input[type=checkbox][name=action]').prop( "checked", false)
    });

})

$(document).ready(function() {
    $('#filters-toggle-button').click(function() {
        $('#filters').slideToggle(duration=200);
    })
})