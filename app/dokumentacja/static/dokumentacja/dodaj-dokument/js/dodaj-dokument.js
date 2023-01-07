// Przesuwanie kodu QR

var qr_img = $("#sample_qr")
var pdf_wrapper = $("#pdf_wrapper")
var pdf_render = $('#pdf_render')
var qr_input_x = $('input#qr_x')
var qr_input_y = $('input#qr_y')

var moving = false;

function set_qr_coords() {
    qr_coords = {
        x : qr_img.offset().left - pdf_render.offset().left,
        y : qr_img.offset().top - pdf_render.offset().top
    }
    qr_input_x.val(qr_coords.x);
    qr_input_y.val(qr_coords.y);
}

qr_img.click(function(e) {
    moving = !moving;
    set_qr_coords();
})

pdf_wrapper.mousemove(function(e) {

  if (moving) {
    var newX = e.pageX - 30;
    var newY = e.pageY - 30;

    qr_img.css("left", newX + "px");
    qr_img.css("top", newY + "px");
  }
})

pdf_wrapper.bind('scroll', function() {
    set_qr_coords();
})
set_qr_coords();

// --------------------------------------------------------
// Renderowanie pliku pdf

function render_draw() {
    var myState = {
        pdf: null,
        currentPage: 1,
        zoom: 1
    }
    var file = document.getElementById('id_file').files[0];
    var fileReader = new FileReader();
    fileReader.onload = function() {
        var typedarray = new Uint8Array(this.result);
        pdfjsLib.getDocument(typedarray).promise.then((pdf) => {
            myState.pdf = pdf;
            console.log(pdf)
            render();
        });
    };
    fileReader.readAsArrayBuffer(file);


    function render() {
        myState.pdf.getPage(myState.currentPage).then((page) => {
            console.log(page)
            var canvas = document.getElementById("pdf_render");
            var ctx = canvas.getContext('2d');
            var viewport = page.getViewport({scale: myState.zoom});
            console.log(viewport.viewBox)

            canvas.width = viewport.width;
            canvas.height = viewport.height;

            pdf_wrapper.css('max-width', viewport.width + "px")

            page.render({
                canvasContext: ctx,
                viewport: viewport
            });
            set_qr_coords();
            load_gif.css("display", "none")
        });
    };
};

var file_input = $('#id_file')
var load_gif = $('#id_load_gif')
file_input.on('change', function() {
    load_gif.css("display", "block")
    render_draw();
})