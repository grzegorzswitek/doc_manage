var document_source_video = $("#document-source-video")
var document_source_file = $("#document-source-file")

var result_container = $('#result-container')
var result_help = $('#result-help');

var video_js = document.querySelector("#v");
var video_jq = $("#v")
var video_help = $('#video-help');

var vCanvas = document.getElementById("video-canvas");
var vCanvasCtx;

var render_spinner = $('#render-spinner');
var select_file_label = $('#select-file-label');

var camSetInterval;

// przechwytuje obraz z kamery i decoduje kod qr

function initCanvas(canvas, w, h)
{
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    canvas.width = w;
    canvas.height = h;
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, w, h);
    return ctx
}

function captureToCanvas() {
  vCanvasCtx.drawImage(video_js,0,0);
  QCodeDecoder().decodeFromImage(vCanvas.toDataURL(), function (er, res) {
    if (res) {
      clearInterval(camSetInterval);
      if (res.length == 5) {
        // TODO
        search_draw_in_database(res);
        video_js.pause();
        video_help.show();
        vCanvasCtx = null;
      } else {
        video_js.pause()
        video_help.show();
        result_help.append('<p class="alert alert-danger">Niepoprawny kod.</p>')
      }
    };
  });
};

function show_spinner() {
  select_file_label.hide();
  render_spinner.show();
  clearResult();
}

function hide_spinner() {
  render_spinner.hide();
  select_file_label.show();
}

function clearResult() {
  result_help.html('');
  result_container.find('table td:nth-child(2)').html('');
}

function cam_refresh() {
  clearResult();
  video_help.hide();
  video_js.play()
  vCanvasCtx = initCanvas(vCanvas, 800, 600);
  camSetInterval = setInterval(captureToCanvas, 500);
}

function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}

function drop(e) {
  clearResult();
  find_count=0;
  e.stopPropagation();
  e.preventDefault();

    var files = e.originalEvent.dataTransfer.files;
    var fd = new FormData();

    fd.append('files', files[0]);

  if(files.length>0)
  {
    show_spinner();
    search_qrcode_in_document(files)
  }
}

function setfile() {
  clearResult();
  clearInterval(camSetInterval);
  document_source_video.hide();
  document_source_file.show();

  document_source_file.on("dragenter", dragenter);
  document_source_file.on("dragover", dragover);
  document_source_file.on("drop", drop);
}

function setcam() {
  clearResult();
  cam_refresh();
  document_source_file.hide();
  document_source_video.show();
}

setfile();



function search_qrcode_in_metadata(file){
  return new Promise((resolve, reject) => {
    var reader = new FileReader();
    reader.onload = function(progressEvent){
      var patt = /\/bx-QR\s{0,1}\(([a-z0-9]{5})\)|<.*:bx-QR>\s{0,1}([a-z0-9]{5})\s{0,1}<\/.*:bx-QR>/i
        if (patt.test(this.result)) {
          qr_matches = this.result.match(patt)
          var kod = qr_matches.slice(1).filter(match => match !== undefined)[0]
          resolve(kod);
        } else {
          reject('Nie znaleziono kodu w metadanych')
        }
      }
    reader.readAsText(file);
  });
};

function search_qrcode_by_image(file) {
  return new Promise((resolve, reject) => {
    var fd = new FormData();    
    fd.append('file', file);
    $.ajax({
      type: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      url: url_ajax_search_qrcode_by_image,
      data: fd,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.kod) {
          resolve(response.kod)
        } else if (response.error) {
          reject(response.error)
        }
      }
  })
  })
}

function search_qrcode_in_document(files) {
  if (files.length > 1) {
    result_help.append('<p class="alert alert-danger">Należy wybrać jeden plik.</p>')
  }
  file = files[0];
  console.log(file.type)
  if (file.type !== 'application/pdf') {
    result_help.append('<p class="alert alert-danger">Niepoprawny format pliku (wybierz plik *.pdf).</p>')
    hide_spinner();
    return false;
  }
  search_qrcode_in_metadata(file).then((kod) => {
    console.log(`Znaleziono w metadanych kod ${kod}`);
    search_draw_in_database(kod);
  }).catch((error) => {
    console.log(error);
    search_qrcode_by_image(file).then((kod) => {
      console.log(`Znaleziono w pliku kod ${kod} (by image)`);
      search_draw_in_database(kod);
    }).catch((error) => {
      console.log(error);
      result_help.append('<p class="alert alert-danger">W pliku nie znaleziono identyfikatora.</p>')
    });
  }).finally(hide_spinner);
}

$(document).ready(function() {
  $('#set-video').change(setcam);
  $('#set-file').change(setfile);

  $('#select-file-btn').change(function(){
    if (this.files) {
      show_spinner();
      search_qrcode_in_document(this.files);
    }
  })

  $('#video-help').click(function() {
    clearResult();
    cam_refresh();
  });

})



// TODO: przycisk do sprawdzania QR po ustawieniu rysunku w widocznym obszarze
// TODO: inicjować canvas przy przełączeniu pomiędzy camerą a select_file
// TODO: dorobić przycisk odśwież i inicjować przy nim canvas (czyścić)
// TODO: wyłączyć automatyczne czytanie plików pdf po drop'ie
// TODO: czyszczenie canvas po drop'ie (coś już jest, wrzucamy nowy plik i trzeba wyczyścić)
