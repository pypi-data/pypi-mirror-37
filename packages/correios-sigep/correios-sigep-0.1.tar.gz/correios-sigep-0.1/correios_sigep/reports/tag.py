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

class Tag(Generator):
    TYPE_4P = '4p.html'
    TYPE_6P = '6p.html'
    def __init__(self, sender, postal_object, id_postcard, contract_id, volume={}, group = ''):
        super(Tag, self).__init__()
        self.str_datamatrix = ''
        self.logo = ''
        self.contract_id = contract_id
        self.id_postcard = id_postcard
        self.postal_object = postal_object
        self.sender = sender
        self.volume = volume

        if not isinstance(sender, Sender):
            raise Exception(
                'parameter sender is not valid. Must have be Sender instance')

        if not isinstance(postal_object, PostalObject):
            raise Exception(
                'parameter postal_object is not valid. Must have be PostalObject instance')

        self.str_datamatrix = self.generateDataMatrix(sender, postal_object, id_postcard)
        
        self.img_barcode_tag = b64encode(self.generate_barcode_128(postal_object.numero_etiqueta, 300, 66, 1))
        self.img_barcode_zipcode = b64encode(self.generate_barcode_128(postal_object.nacional.cep_destinatario, 220, 66))

    def mountStr(self, value):
        self.str_datamatrix += str (value)

    def generateDataMatrix(self, sender, postal_object, id_postcard):
        self.mountStr(postal_object.nacional.cep_destinatario)
        self.mountStr(postal_object.destinatario.numero_end_destinatario)
        self.mountStr(sender.cep_remetente)
        self.mountStr(sender.numero_remetente)
        self.mountStr(postal_object.nacional.cep_destinatario)
        self.mountStr('51')
        self.mountStr(postal_object.numero_etiqueta)
        self.mountStr(self.normalizeAdditionalServices(postal_object.servico_adicional))
        self.mountStr(id_postcard)
        self.mountStr(postal_object.codigo_servico_postagem)
        self.mountStr(postal_object.destinatario.numero_end_destinatario)
        self.mountStr(self.normalizeComplementAddress(postal_object.destinatario.complemento_destinatario))
        self.mountStr(self.normalizeDeclaredValue(postal_object.servico_adicional.valor_declarado))
        self.mountStr(self.normalizeTelephone(postal_object.destinatario.telefone_destinatario))
        self.mountStr('-00.000000')
        self.mountStr('-00.000000')
        self.mountStr('|')
        self.mountStr(''.ljust(30, ' '))

        byte_io = BytesIO()
        encoder = barcode('datamatrix', self.str_datamatrix, options = dict(), margin=0)
        encoder.save(byte_io, 'png')
        
        return b64encode(byte_io.getvalue())

    def generate_barcode_128(self, value, width=300, height=80, scale=1):
        cb128 = CandyBar128(value, width, height, scale)
        bs = cb128.generate_barcode()
        return bs
        
    def render(self, tag_type=TYPE_4P):
        params = {
            'datamatrix': self.str_datamatrix,
            'barcode_tag': self.img_barcode_tag,
            'barcode_cep': self.img_barcode_zipcode,
            'contract_id': self.contract_id,
            'recipient_name': self.postal_object.destinatario.nome_destinatario,
            'recipient_address': '{}, {}'.format(self.postal_object.destinatario.logradouro_destinatario, self.postal_object.destinatario.numero_end_destinatario),
            'recipient_comp': self.postal_object.destinatario.complemento_destinatario,
            'recipient_neighborhood': self.postal_object.nacional.bairro_destinatario,
            'recipient_city': self.postal_object.nacional.cidade_destinatario,
            'recipient_uf': self.postal_object.nacional.uf_destinatario,
            'recipient_zipcode': self.postal_object.nacional.cep_destinatario,
            'sender_address': '{}, {}'.format(self.sender.logradouro_remetente, self.sender.numero_remetente),
            'sender_comp': self.sender.complemento_remetente,
            'sender_name': self.sender.nome_remetente,
            'sender_neighborhood': self.sender.bairro_remetente,
            'sender_zipcode': self.sender.cep_remetente,
            'sender_city': '{}/{}'.format(self.sender.cidade_remetente, self.sender.uf_remetente),
            'total_volume': self.volume['total_volume'],
            'current_volume': self.volume['current_volume'],
            'weight': self.volume['weight'],
            'tag': self.normalizeTag(self.postal_object.numero_etiqueta)

        }

        return super(Tag, self).render(tag_type, **params)

    @staticmethod
    def normalizeTag(tag):
        prefix_tag = tag[:2]
        sufix_tag = tag[11:13]
        tag = tag[2:11]

        tag = '{} {} {} {} {}'.format(prefix_tag, tag[0:3], tag[3:6], tag[6:10], sufix_tag )
        return tag

    @staticmethod
    def normalizeAdditionalServices(additional_service):
        return ''.join(additional_service.codigo_servico_adicional).ljust(12, '0')

    @staticmethod
    def normalizeComplementNumber(number):
        return str(number).ljust(4, '0')
    
    @staticmethod
    def normalizeDeclaredValue(value):
        return re.sub('[^0-9]+', '', str(value)).ljust(5, '0')

    @staticmethod
    def normalizeTelephone(number=''):
        return number.ljust(12, '0')
    
    @staticmethod
    def normalizeComplementAddress(complement):
        return complement.ljust(20, ' ')