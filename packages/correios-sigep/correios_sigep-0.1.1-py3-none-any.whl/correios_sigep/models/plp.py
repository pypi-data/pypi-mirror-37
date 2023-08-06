class Plp(object):
    

    def __init__(self, postage_card):

        if not len(str(postage_card)) == 10:
            raise Exception('the postage card number should be have has 10 character length')

        if not str(postage_card).isdigit():
            raise Exception('postage card number has to be a string type digit')

        self.id_plp = ''
        self.valor_global = ''
        self.mcu_unidade_postagem = ''
        self.nome_unidade_postagem = ''
        self.cartao_postagem = postage_card