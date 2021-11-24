import json
import ssl
from base64 import b64decode
from urllib.request import urlopen

import certifi
from Crypto.PublicKey import ECC
from cose.algorithms import Es256
from cose.headers import KID
from cose.keys import CoseKey
from cose.keys.curves import P256
from cose.keys.keyparam import KpKty, EC2KpCurve, KpAlg, EC2KpX, EC2KpY
from cose.keys.keytype import KtyEC2
from cose.messages.sign1message import Sign1Message


class SigMapperError(Exception):
    pass


class SigMapper:
    header_prot = None
    header = None
    payload = None
    signature = None

    html = ''
    keys = []

    countries = {"BE": "Belgium", "EL": "Greece", "LT": "Lithuania", "PT": "Portugal", "BG": "Bulgaria", "ES": "Spain",
                 "LU": "Luxembourg", "RO": "Romania", "CZ": "Czechia", "FR": "France", "HU": "Hungary",
                 "SI": "Slovenia", "DK": "Denmark", "HR": "Croatia", "MT": "Malta", "SK": "Slovakia", "DE": "Germany",
                 "IT": "Italy", "NL": "Netherlands", "FI": "Finland", "EE": "Estonia", "CY": "Cyprus", "AT": "Austria",
                 "SE": "Sweden", "IE": "Ireland", "LV": "Latvia", "PL": "Poland"}

    def _check_keys(self):
        c = Sign1Message(self.header_prot, self.header, self.payload)
        key_id = c.phdr[KID]
        pk = None
        for pk_ in self.keys:
            if key_id == b64decode(pk_['kid']):
                pk = pk_
                break

        ec = ECC.import_key(b64decode(pk['subjectPk']))

        c.key = CoseKey.from_dict(
            {
                KpKty: KtyEC2,
                EC2KpCurve: P256,
                KpAlg: Es256,
                EC2KpX: ec.pointQ.x.to_bytes(),
                EC2KpY: ec.pointQ.y.to_bytes()
            }
        )

        c._signature = self.signature  # please tell me a way to set the signature

        if pk is not None:
            verified = False

            try:
                verified = c.verify_signature()
            except Exception as e:
                print("Signature could not be computed: " + str(e))

            if verified:
                self.html += "<p>Signature validated the key with ID \"" + \
                             pk['kid'] + "\" issued by " + self.countries[pk['ian']] + \
                             (" - " + pk['san'] if pk['san'] != "" else "") + "</p>"
            else:
                self.html += "<p>Signature validation failed! (" + pk['kid'] + ")</p>"
        else:
            self.html += "<p>No key found to validate signature!</p>"

    def _retrieve_keys(self, key_url):
        raw = urlopen(key_url, context=ssl.create_default_context(cafile=certifi.where()))
        json_ = json.loads(raw.read())
        payload = b64decode(json_['payload'])
        list_ = json.loads(payload)
        eu_list = list_['eu_keys']
        for kid in eu_list:
            self.keys.append(eu_list[kid][0] | {"kid": kid})

    def __init__(self, header_prot, header, payload, signature, key_url):
        self.header_prot = header_prot
        self.header = header
        self.payload = payload
        self.signature = signature

        self._retrieve_keys(key_url)

    def print_html(self):
        if len(self.keys) == 0:
            raise SigMapperError("RETRIEVING_KEYS_FAILED")
        self._check_keys()
        return self.html
