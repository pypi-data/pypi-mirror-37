#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..models.postal_object import PostalObject
from ..models.sender import Sender
from ..models.additional_service import AdditionalService
from elaphe import barcode
from hubarcode.datamatrix import DataMatrixEncoder
from candybar.CandyBarCode128 import CandyBar128
from base64 import b64encode
from ..reports.generator import Generator
import qrcode
import re
from io import BytesIO


class Plp(Generator):
    def __init__(self, id_plp, id_contract, services):
        super(Plp, self).__init__()

        cb128 = CandyBar128(id_plp, 180, 50, 1)
        bs = cb128.generate_barcode()
        self.id_contract = id_contract
        self.id_plp = id_plp
        self.id_plp_barcode = b64encode(bs) 
        self.services = services
        self.total = 0
        for service in services:
            self.total += int(services[service]['qty'])
    def render(self):

        params = {
            'barcode': self.id_plp_barcode,
            'id_contract': self.id_contract,
            'id_plp': self.id_plp,
            'services': self.services,
            'total': self.total
        }

        return super(Plp, self).render('plp_summary.html', **params)
