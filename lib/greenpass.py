from pyzbar.pyzbar import decode
from PIL import Image
from base45 import b45decode
from zlib import decompress
from flynn import decoder as flynn_decoder
from lib.datamapper import DataMapper as data_mapper
from lib.sigmapper import SigMapper as sig_mapper


class GreenPassDecoder(object):
    stream_data = None

    def __init__(self, stream_data):
        self.stream_data = decode(Image.open(stream_data))[0].data

    def decode(self, schema, key_url):
        qr_decoded = self.stream_data[4:]
        qrcode_data = decompress(b45decode(qr_decoded))
        (_, (header_1, header_2, cbor_payload, sign)) = flynn_decoder.loads(qrcode_data)
        data = flynn_decoder.loads(cbor_payload)
        dm = data_mapper(data, schema)
        sm = sig_mapper(flynn_decoder.loads(header_1), header_2, cbor_payload, sign, key_url)

        return {"vals": dm.convert_json(), "sig": sm.print_html()}
