from ..utils.number import number_format
class National(object):
    def __init__(self, neighboorhood, city, state, zipcode, invoice_number='', object_description='', value_charged=0.00):
        self.bairro_destinatario = neighboorhood
        self.cidade_destinatario = city
        self.uf_destinatario = state
        self.cep_destinatario = zipcode
        self.numero_nota_fiscal = invoice_number
        self.descricao_objeto = object_description
        self.valor_a_cobrar = number_format(value_charged)
        self.natureza_nota_fiscal = ''
        self.codigo_usuario_postal = ''
        self.centro_custo_cliente  = ''
        self.serie_nota_fiscal = ''
        self.valor_nota_fiscal = ''