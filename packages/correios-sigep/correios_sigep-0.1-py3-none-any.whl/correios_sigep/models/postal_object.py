from ..utils.number import number_format
class PostalObject(object):

    def __init__(self, tag, service_code, weight, recipient, national,
                 additional_service, object_dimension, rt1='', rt2='', cubing=0.00):

        self.codigo_objeto_cliente = ''
        self.data_postagem_sara = ''
        self.status_processamento = 0
        self.numero_comprovante_postagem = ''
        
        self.numero_etiqueta = tag.tag_w_digit
        self.codigo_servico_postagem = service_code
        self.cubagem = number_format(cubing)
        self.peso = int(weight)
        self.rt1 = rt1
        self.rt2 = rt2
        self.destinatario = recipient
        self.nacional = national
        self.servico_adicional = additional_service
        self.dimensao_objeto = object_dimension
        self.valor_cobrado = ''

# 2018361049166