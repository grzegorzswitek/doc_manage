function handle_drawing_data(response) {
    if (response) {
      if ("error" in response) {
        console.log(response["error"]);
        result_help.append('<p class="alert alert-danger">Nie znaleziono dokumentu w bazie danych.</p>')
        $('#render-spinner').hide();
        $('#help-select-file').show();
        return;
      }
      console.log(response)
      var dokument = JSON.parse(response["dokument"])[0];
      var url_change = JSON.parse(response["url_change"])[0];
      var url_detail = JSON.parse(response["url_detail"])[0];
      var fields = dokument.fields
      console.log(fields)
      console.log(dokument)
      $("#inwestycja-val").html(fields.inwestycja)
      $("#branza-val").html(fields.branza)
      $("#oznaczenie-val").html(fields.oznaczenie)
      $("#nazwa-val").html(fields.nazwa)
      $("#result-button-edit").attr('href', url_change)
      $("#result-button-details").attr('href', url_detail)
      $('#render-spinner').hide();
      $('#help-select-file').show();

      var status = fields.status
      if (status == "Aktualny") {
        $("#status-val").html('<span class="text-success">' + status + '</span>');
      } else if (status == "Nieaktualny") {
        $("#status-val").html('<span class="text-danger">' + status + '</span>');
      } else {
        $("#status-val").html('<span class="text-warning">' + status + '</span>');
      }
    }
    else {

    }
}

function search_draw_in_database(kod) {
  console.log('kod', kod)
  $.ajax({
      type: 'GET',
      url: url_ajax_get_document_by_code,
      data: {'kod': kod},
      success: function(response) {
        handle_drawing_data(response);
      }
  })
}