from PyPDF4 import PdfFileReader, PdfFileWriter
from xml.etree import ElementTree as ET
from tempfile import TemporaryFile
from io import BytesIO
from fitz import fitz
import qrcode
import re

class PdfDoc:
    def __init__(self, path, qr_code, qr_coords, error_correct='H'):
        self.path = path
        self.qr_code = qr_code
        self.qr_coords = qr_coords

        if error_correct.upper() == 'L':
            self.error_correct = qrcode.constants.ERROR_CORRECT_L
        elif error_correct.upper() == 'M':
            self.error_correct = qrcode.constants.ERROR_CORRECT_M
        elif error_correct.upper() == 'Q':
            self.error_correct = qrcode.constants.ERROR_CORRECT_Q
        elif error_correct.upper() == 'H':
            self.error_correct = qrcode.constants.ERROR_CORRECT_H
        else:
            self.error_correct = qrcode.constants.ERROR_CORRECT_H

        self.add_qrcode_to_pdf_information()
        self.add_qrcode_image()
        

    @property
    def xmp_metadata(self):
        with fitz.open(self.path) as pdf:
            xmp_metadata = pdf.get_xml_metadata()
        if not bool(xmp_metadata): return None
        return xmp_metadata
        
    @property
    def xmp_metadata_with_qrcode(self):
        ADOBE_NS = '{adobe:ns:meta/}'
        RDF_NS = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
        PDFX = '{http://ns.adobe.com/pdfx/1.3/}' 
        
        if self.xmp_metadata is None:
            root = None
        else:
            root = ET.fromstring(self.xmp_metadata)
        if root is None: root = ET.Element(ADOBE_NS+'xmpmeta')

        rdftree = root.find(RDF_NS+'RDF')
        if rdftree is None: rdftree = ET.SubElement(root, RDF_NS+'RDF')

        qr_elem = None
        for elem in rdftree:
            qr_elem = elem.find(PDFX+'QR')
            if qr_elem is not None:
                break

        if qr_elem is None:
            rdf_desc_elem = ET.SubElement(rdftree, RDF_NS+'Description')
            qr_elem = ET.SubElement(rdf_desc_elem, PDFX+'bx-QR')

        qr_elem.text = self.qr_code

        xml_meta_str = ET.tostring(root, encoding='utf-8').decode() 

        return xml_meta_str

    def add_qrcode_to_pdf_information(self):
        fin = open(self.path, 'rb')
        reader = PdfFileReader(fin, strict=False)
        writer = PdfFileWriter()
        writer.appendPagesFromReader(reader)
        metadata = reader.getDocumentInfo()
        writer.addMetadata(metadata)
        writer.addMetadata({
            '/bx-QR': self.qr_code
        })
        fout_temp = TemporaryFile('w+b')
        writer.write(fout_temp)
        fout_temp.seek(0)
        fin.close()
        pdf_source = fout_temp.read()
        fin = open(self.path, 'wb')
        fin.write(pdf_source)
        fin.close()
        fout_temp.close()

    def _qr(self, version=1, box_size=3, border=1):
        qr = qrcode.QRCode(
            version=version,
            error_correction=self.error_correct,
            box_size=box_size,
            border=border,
        )
        qr.add_data(self.qr_code)
        qr.make(fit=True)
        return qr
    
    def _qr_image(self, fill_color="black", back_color="white"):
        return self._qr().make_image(fill_color=fill_color, back_color=back_color)

    def add_qrcode_image(self):
        x = self.qr_coords[0]
        y = self.qr_coords[1]       
        w = h = float(self._qr_image().pixel_size)

        with fitz.open(self.path) as pdf:
            page = pdf[0]
            page.wrapContents()
            x_1 = float(x)
            y_1 = float(y)
            x_2 = x_1 + w
            y_2 = y_1 + h
            point_1 = fitz.Point(x_1, y_1)
            point_2 = fitz.Point(x_2, y_2)

            image = self._qr_image()
            imgByteArr = BytesIO()
            image.save(imgByteArr, format=image.format)
            imgByteArr = imgByteArr.getvalue()

            rect = fitz.Rect(point_1, point_2).transform(page.derotationMatrix)
            page.insertImage(rect, stream=imgByteArr)

            pdf.setXmlMetadata(self.xmp_metadata_with_qrcode)

            pdf.saveIncr()
            return pdf


    

