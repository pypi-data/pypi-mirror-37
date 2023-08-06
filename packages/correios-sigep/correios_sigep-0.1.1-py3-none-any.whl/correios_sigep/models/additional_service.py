from ..utils.number import number_format

class AdditionalService(object):
    def __init__(self, added_value=0.00):
        self.codigo_servico_adicional = []
        self.valor_declarado = number_format(added_value)

        self.addCode('025')
    
    def addCode(self, code):
        # todo check availables codes
        self.codigo_servico_adicional.append(str(code))