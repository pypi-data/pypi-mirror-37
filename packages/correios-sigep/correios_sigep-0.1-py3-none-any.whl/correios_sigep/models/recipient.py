class Recipient(object):
    
    def __init__(self, name, telephone, cellphone, email, address, number, 
                complement=''):
        self.nome_destinatario = name
        self.telefone_destinatario = telephone
        self.celular_destinatario = cellphone
        self.email_destinatario = email
        self.logradouro_destinatario = address
        self.complemento_destinatario = complement
        self.numero_end_destinatario = number