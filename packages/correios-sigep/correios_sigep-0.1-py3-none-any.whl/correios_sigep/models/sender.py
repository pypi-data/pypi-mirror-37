class Sender(object):
    def __init__(self, contract_number, director_number, administrative_code, sender_name,
                 address, number, complement, neighborhood, zipcode, city, state, telephone='', fax='', email=''):

        self.numero_contrato = contract_number
        self.numero_diretoria = director_number
        self.codigo_administrativo = administrative_code
        self.nome_remetente = sender_name
        self.logradouro_remetente = address
        self.numero_remetente = number
        self.complemento_remetente = complement
        self.bairro_remetente = neighborhood
        self.cep_remetente = zipcode
        self.cidade_remetente = city
        self.uf_remetente = state
        self.telefone_remetente = telephone
        self.fax_remetente = ''
        self.email_remetente = email

    @property
    def numero_contrato(self):
        return self._numero_contrato

    @numero_contrato.setter
    def numero_contrato(self, value):
        if not len(str(value)) == 10:
            raise Exception('invalid contract number length. Must be 10 string digit length')
        self._numero_contrato = value

    @property
    def numero_diretoria(self):
        return self._numero_diretoria
    
    @numero_diretoria.setter
    def numero_diretoria(self, value):
        if not len(str(value)) == 2:
            raise Exception('invalid direction number length. Must be 2 string digit length')
        self._numero_diretoria = value

    @property
    def codigo_administrativo(self):
        return self._codigo_administrativo

    @codigo_administrativo.setter
    def codigo_administrativo(self, value):
        if not len(str(value)) == 8:
            raise Exception('invalid administrative number length. Must be 8 string digit length')
        self._codigo_administrativo = value

    @property
    def nome_remetente(self):
        return self._nome_remetente

    @nome_remetente.setter
    def nome_remetente(self, value):
        if len(str(value)) > 50:
            raise Exception('invalid sender name length. max length is 50 characters')
        self._nome_remetente = value

    @property
    def logradouro_remetente(self):
        return self._logradouro_remetente

    @logradouro_remetente.setter
    def logradouro_remetente(self, value):
        if len(str(value)) > 50:
            raise Exception('invalid address length. max length is 50 characters')
        self._logradouro_remetente = value

    @property
    def numero_remetente(self):
        return self._numero_remetente

    @numero_remetente.setter
    def numero_remetente(self, value):
        if len(str(value)) > 5:
            raise Exception('invalid address number length. max length is 5 characters')
        self._numero_remetente = value

    @property
    def complemento_remetente(self):
        return self._complemento_remetente

    @complemento_remetente.setter
    def complemento_remetente(self, value):
        if len(str(value)) > 30:
            raise Exception('invalid complement length. max length is 30 characters')
        self._complemento_remetente = value

    @property
    def bairro_remetente(self):
        return self._bairro_remetente
    
    @bairro_remetente.setter
    def bairro_remetente(self, value):
        if len(str(value)) > 30:
            raise Exception('invalid neighboorhood length. max length is 30 characters')
        self._bairro_remetente = value
    
    @property
    def cep_remetente(self):
        return self._cep_remetente

    @cep_remetente.setter
    def cep_remetente(self, value):
        import re
        if len(str(value)) < 8 or len(str(value)) > 9:
            raise Exception('invalid zipcode length')
        self._cep_remetente = re.sub('[^0-9]', '', value)

    @property
    def cidade_remetente(self):
        return self._cidade_remetente

    @cidade_remetente.setter
    def cidade_remetente(self, value):
        if len(str(value)) > 30:
            raise Exception('invalid city length. max length is 30 characters')
        self._cidade_remetente = value

    @property
    def uf_remetente(self):
        return self._uf_remetente

    @uf_remetente.setter
    def uf_remetente(self, value):
        if len(str(value)) > 30:
            raise Exception('invalid state length. max length is 2 characters')
        self._uf_remetente = value

    @property
    def telefone_remetente(self):
        return self._telefone_remetente

    @telefone_remetente.setter
    def telefone_remetente(self, value):
        if len(str(value)) < 11 or len(str(value)) > 12 :
            raise Exception('invalid telephone length')
        self._telefone_remetente = value

    @property
    def fax_remetente(self):
        return self._fax_remetente
    
    @fax_remetente.setter
    def fax_remetente(self, value):
        if len(str(value)) > 12:
            raise Exception('invalid fax length')
        self._fax_remetente = value

    @property
    def email_remetente(self):
        return self._email_remetente

    @email_remetente.setter
    def email_remetente(self, value):
        import re
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise Exception('invalid email')
        
        self._email_remetente = value