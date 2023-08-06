from collections import OrderedDict
from ..utils import dict as Dict
from ..utils.etree import parseDict
from lxml import etree
from ..models.plp import Plp
from ..models.sender import Sender
from ..models.postal_object import PostalObject

class CorreiosLog:
    def __init__(self, plp, sender_obj):
        
        if not isinstance(plp, Plp):
            raise Exception('parameter plp must have be an instance of Plp')

        if not isinstance(sender_obj, Sender):
            raise Exception('parameter sender_obj must have be an instance of Sender')

        self._correios_log = OrderedDict()
        self._correios_log['tipo_arquivo'] = 'Postagem'
        self._correios_log['versao_arquivo'] = '2.3'
        self._correios_log['plp'] = plp
        self._correios_log['remetente'] = sender_obj
        self._correios_log['objeto_postal'] = []

    @property
    def correios_log(self):
        return self._correios_log
    
    def addPostalObject(self, postal_object):
        if not isinstance(postal_object, PostalObject):
            raise Exception('postal_object must have be an instance of PostalObject')
            
        self._correios_log['objeto_postal'].append(postal_object)

    def getXml(self):
        # xml_dict = Dict.toRecursiveDict(self._correios_log)

        correios_log = etree.Element('correioslog')
        
        tipo_arquivo = etree.Element('tipo_arquivo')
        versao_arquivo = etree.Element('versao_arquivo')

        correios_log.append(tipo_arquivo)
        correios_log.append(versao_arquivo)
        # remetente = etree.Element('remetente')
        # objeto_postal = etree.Element('objeto_postal')
        
        tipo_arquivo.text = unicode(self._correios_log['tipo_arquivo'])
        versao_arquivo.text = unicode(self._correios_log['versao_arquivo'])

        # plp node
        etree_plp = etree.Element('plp')
        plpobj = self._correios_log['plp']

        etree_id_plp = etree.Element('id_plp')
        etree_valor_global = etree.Element('valor_global')
        etree_mcu_unidade_postagem = etree.Element('mcu_unidade_postagem')
        etree_nome_unidade_postagem = etree.Element('nome_unidade_postagem')
        etree_cartao_postagem = etree.Element('cartao_postagem')

        etree_id_plp.text = unicode(plpobj.id_plp)
        etree_valor_global.text = unicode(plpobj.valor_global)
        etree_mcu_unidade_postagem.text = unicode(plpobj.mcu_unidade_postagem)
        etree_nome_unidade_postagem.text = unicode(plpobj.nome_unidade_postagem)
        etree_cartao_postagem.text = unicode(plpobj.cartao_postagem)

    
        etree_plp.append(etree_id_plp)
        etree_plp.append(etree_valor_global)
        etree_plp.append(etree_mcu_unidade_postagem)
        etree_plp.append(etree_nome_unidade_postagem)
        etree_plp.append(etree_cartao_postagem)
        correios_log.append(etree_plp)

        # remetente node
        etree_remetente = etree.Element('remetente')

        etree_numero_contrato = etree.Element('numero_contrato')
        etree_numero_diretoria = etree.Element('numero_diretoria')
        etree_codigo_administrativo = etree.Element('codigo_administrativo')
        etree_nome_remetente = etree.Element('nome_remetente')
        etree_logradouro_remetente = etree.Element('logradouro_remetente')
        etree_numero_remetente = etree.Element('numero_remetente')
        etree_complemento_remetente = etree.Element('complemento_remetente')
        etree_bairro_remetente = etree.Element('bairro_remetente')
        etree_cep_remetente = etree.Element('cep_remetente')
        etree_cidade_remetente = etree.Element('cidade_remetente')
        etree_uf_remetente = etree.Element('uf_remetente')
        etree_telefone_remetente = etree.Element('telefone_remetente')
        etree_fax_remetente = etree.Element('fax_remetente')
        etree_email_remetente = etree.Element('email_remetente')

        remetenteobj = self._correios_log['remetente']
        etree_numero_contrato.text = unicode(remetenteobj.numero_contrato)
        etree_numero_diretoria.text = unicode(remetenteobj.numero_diretoria)
        etree_codigo_administrativo.text = unicode(remetenteobj.codigo_administrativo)
        etree_nome_remetente.text = etree.CDATA(unicode(remetenteobj.nome_remetente)) if remetenteobj.nome_remetente != '' else None
        etree_logradouro_remetente.text = etree.CDATA(unicode(remetenteobj.logradouro_remetente)) if remetenteobj.logradouro_remetente != '' else None
        etree_numero_remetente.text = etree.CDATA(unicode(remetenteobj.numero_remetente)) if remetenteobj.numero_remetente != '' else None
        etree_complemento_remetente.text = etree.CDATA(unicode(remetenteobj.complemento_remetente)) if remetenteobj.complemento_remetente != '' else None
        etree_bairro_remetente.text = etree.CDATA(unicode(remetenteobj.bairro_remetente)) if remetenteobj.bairro_remetente != '' else None
        etree_cep_remetente.text = etree.CDATA(unicode(remetenteobj.cep_remetente)) if remetenteobj.cep_remetente != '' else None
        etree_cidade_remetente.text = etree.CDATA(unicode(remetenteobj.cidade_remetente)) if remetenteobj.cidade_remetente != '' else None
        etree_uf_remetente.text = etree.CDATA(unicode(remetenteobj.uf_remetente)) if remetenteobj.uf_remetente != '' else None
        etree_telefone_remetente.text = etree.CDATA(unicode(remetenteobj.telefone_remetente)) if remetenteobj.telefone_remetente != '' else None
        etree_fax_remetente.text = etree.CDATA(unicode(remetenteobj.fax_remetente)) if remetenteobj.fax_remetente != '' else None
        etree_email_remetente.text = etree.CDATA(unicode(remetenteobj.email_remetente)) if remetenteobj.email_remetente != '' else None

        etree_remetente.append(etree_numero_contrato)
        etree_remetente.append(etree_numero_diretoria)
        etree_remetente.append(etree_codigo_administrativo)
        etree_remetente.append(etree_nome_remetente)
        etree_remetente.append(etree_logradouro_remetente)
        etree_remetente.append(etree_numero_remetente)
        etree_remetente.append(etree_complemento_remetente)
        etree_remetente.append(etree_bairro_remetente)
        etree_remetente.append(etree_cep_remetente)
        etree_remetente.append(etree_cidade_remetente)
        etree_remetente.append(etree_uf_remetente)
        etree_remetente.append(etree_telefone_remetente)
        etree_remetente.append(etree_fax_remetente)
        etree_remetente.append(etree_email_remetente)

        correios_log.append(etree_remetente)

        forma_pagamento = etree.Element('forma_pagamento')
        correios_log.append(forma_pagamento)

        # objeto_postal node list

        for objeto_postal_obj in self._correios_log['objeto_postal']:
            etree_objeto_postal = etree.Element('objeto_postal')

            etree_codigo_objeto_cliente = etree.Element('codigo_objeto_cliente')
            etree_data_postagem_sara = etree.Element('data_postagem_sara')
            etree_status_processamento = etree.Element('status_processamento')
            etree_numero_comprovante_postagem = etree.Element('numero_comprovante_postagem')
            etree_numero_etiqueta = etree.Element('numero_etiqueta')
            etree_codigo_servico_postagem = etree.Element('codigo_servico_postagem')
            etree_cubagem = etree.Element('cubagem')
            etree_peso = etree.Element('peso')
            etree_rt1 = etree.Element('rt1')
            etree_rt2 = etree.Element('rt2')
            etree_destinatario = etree.Element('destinatario')
            etree_nacional = etree.Element('nacional')
            etree_servico_adicional = etree.Element('servico_adicional')
            etree_dimensao_objeto = etree.Element('dimensao_objeto')
            etree_valor_cobrado = etree.Element('valor_cobrado')


            etree_status_processamento.text = unicode('0')
            etree_numero_etiqueta.text = unicode(objeto_postal_obj.numero_etiqueta)
            etree_codigo_servico_postagem.text = unicode(objeto_postal_obj.codigo_servico_postagem)
            etree_cubagem.text = unicode(objeto_postal_obj.cubagem)
            etree_peso.text = unicode(objeto_postal_obj.peso)
            etree_rt1.text = etree.CDATA(unicode(objeto_postal_obj.rt1)) if objeto_postal_obj.rt1 != '' else None
            etree_rt2.text = etree.CDATA(unicode(objeto_postal_obj.rt2)) if objeto_postal_obj.rt2 != '' else None

            #  objeto_postal.destinatario node
            destinatario_obj = objeto_postal_obj.destinatario
            
            etree_nome_destinatario = etree.Element('nome_destinatario')
            etree_telefone_destinatario = etree.Element('telefone_destinatario')
            etree_celular_destinatario = etree.Element('celular_destinatario')
            etree_email_destinatario = etree.Element('email_destinatario')
            etree_logradouro_destinatario = etree.Element('logradouro_destinatario')
            etree_complemento_destinatario = etree.Element('complemento_destinatario')
            etree_numero_end_destinatario = etree.Element('numero_end_destinatario')

            etree_nome_destinatario.text = etree.CDATA(unicode(destinatario_obj.nome_destinatario)) if destinatario_obj.nome_destinatario != '' else ''
            etree_telefone_destinatario.text = etree.CDATA(unicode(destinatario_obj.telefone_destinatario)) if destinatario_obj.telefone_destinatario != '' else ''
            etree_celular_destinatario.text = etree.CDATA(unicode(destinatario_obj.celular_destinatario)) if destinatario_obj.celular_destinatario != '' else ''
            etree_email_destinatario.text = etree.CDATA(unicode(destinatario_obj.email_destinatario)) if destinatario_obj.email_destinatario != '' else ''
            etree_logradouro_destinatario.text = etree.CDATA(unicode(destinatario_obj.logradouro_destinatario)) if destinatario_obj.logradouro_destinatario != '' else ''
            etree_complemento_destinatario.text = etree.CDATA(unicode(destinatario_obj.complemento_destinatario)) if destinatario_obj.complemento_destinatario != '' else ''
            etree_numero_end_destinatario.text = etree.CDATA(unicode(destinatario_obj.numero_end_destinatario)) if destinatario_obj.numero_end_destinatario != '' else ''

            etree_destinatario.append(etree_nome_destinatario)
            etree_destinatario.append(etree_telefone_destinatario)
            etree_destinatario.append(etree_celular_destinatario)
            etree_destinatario.append(etree_email_destinatario)
            etree_destinatario.append(etree_logradouro_destinatario)
            etree_destinatario.append(etree_complemento_destinatario)
            etree_destinatario.append(etree_numero_end_destinatario)

            #  objeto_postal.nacional node
            nacional_obj = objeto_postal_obj.nacional
            
            etree_bairro_destinatario = etree.Element('bairro_destinatario')
            etree_cidade_destinatario = etree.Element('cidade_destinatario')
            etree_uf_destinatario = etree.Element('uf_destinatario')
            etree_cep_destinatario = etree.Element('cep_destinatario')
            etree_numero_nota_fiscal = etree.Element('numero_nota_fiscal')
            etree_descricao_objeto = etree.Element('descricao_objeto')
            etree_valor_a_cobrar = etree.Element('valor_a_cobrar')
            etree_natureza_nota_fiscal = etree.Element('natureza_nota_fiscal')
            etree_codigo_usuario_postal = etree.Element('codigo_usuario_postal')
            etree_centro_custo_cliente = etree.Element('centro_custo_cliente')
            etree_serie_nota_fiscal = etree.Element('serie_nota_fiscal')
            etree_valor_nota_fiscal = etree.Element('valor_nota_fiscal')

            etree_bairro_destinatario.text = etree.CDATA(unicode(nacional_obj.bairro_destinatario)) if nacional_obj.bairro_destinatario != '' else ''
            etree_cidade_destinatario.text = etree.CDATA(unicode(nacional_obj.cidade_destinatario)) if nacional_obj.cidade_destinatario != '' else ''
            etree_uf_destinatario.text = etree.CDATA(unicode(nacional_obj.uf_destinatario)) if nacional_obj.uf_destinatario != '' else ''
            etree_cep_destinatario.text = etree.CDATA(unicode(nacional_obj.cep_destinatario)) if nacional_obj.cep_destinatario != '' else ''
            etree_numero_nota_fiscal.text = unicode(nacional_obj.numero_nota_fiscal) if nacional_obj.numero_nota_fiscal != '' else ''
            etree_descricao_objeto.text = etree.CDATA(unicode(nacional_obj.descricao_objeto)) if nacional_obj.descricao_objeto != '' else ''
            etree_valor_a_cobrar.text = unicode(nacional_obj.valor_a_cobrar) if nacional_obj.valor_a_cobrar != '' else ''
            etree_natureza_nota_fiscal.text = etree.CDATA(unicode(nacional_obj.natureza_nota_fiscal)) if nacional_obj.natureza_nota_fiscal != '' else ''
            etree_codigo_usuario_postal.text = etree.CDATA(unicode(nacional_obj.codigo_usuario_postal)) if nacional_obj.codigo_usuario_postal != '' else ''
            etree_centro_custo_cliente.text = etree.CDATA(unicode(nacional_obj.centro_custo_cliente)) if nacional_obj.centro_custo_cliente != '' else ''
            etree_serie_nota_fiscal.text = etree.CDATA(unicode(nacional_obj.serie_nota_fiscal)) if nacional_obj.serie_nota_fiscal != '' else ''
            etree_valor_nota_fiscal.text = unicode(nacional_obj.valor_nota_fiscal) if nacional_obj.valor_nota_fiscal !='' else ''

            etree_nacional.append(etree_bairro_destinatario)
            etree_nacional.append(etree_cidade_destinatario)
            etree_nacional.append(etree_uf_destinatario)
            etree_nacional.append(etree_cep_destinatario)
            etree_nacional.append(etree_codigo_usuario_postal)
            etree_nacional.append(etree_centro_custo_cliente)
            etree_nacional.append(etree_numero_nota_fiscal)
            etree_nacional.append(etree_serie_nota_fiscal)
            etree_nacional.append(etree_valor_nota_fiscal)
            etree_nacional.append(etree_natureza_nota_fiscal)
            etree_nacional.append(etree_descricao_objeto)
            etree_nacional.append(etree_valor_a_cobrar)

            #  objeto_postal.servico_adicional node
            servico_adicional_obj = objeto_postal_obj.servico_adicional

            for servico_adicional in servico_adicional_obj.codigo_servico_adicional:
                codigo_servico_adicional = etree.Element('codigo_servico_adicional')
                codigo_servico_adicional.text = unicode(servico_adicional)
                etree_servico_adicional.append(codigo_servico_adicional)

            etree_valor_declarado = etree.Element('valor_declarado')
            etree_valor_declarado.text = unicode(servico_adicional_obj.valor_declarado)
            etree_servico_adicional.append(etree_valor_declarado)

            #  objeto_postal.dimensao_objeto node
            
            etree_tipo_objeto = etree.Element('tipo_objeto')
            etree_dimensao_altura = etree.Element('dimensao_altura')
            etree_dimensao_largura = etree.Element('dimensao_largura')
            etree_dimensao_comprimento = etree.Element('dimensao_comprimento')
            etree_dimensao_diametro = etree.Element('dimensao_diametro')

            etree_tipo_objeto.text = unicode(objeto_postal_obj.dimensao_objeto.tipo_objeto)
            etree_dimensao_altura.text = unicode(objeto_postal_obj.dimensao_objeto.dimensao_altura) if objeto_postal_obj.dimensao_objeto.dimensao_altura != '' else ''
            etree_dimensao_largura.text = unicode(objeto_postal_obj.dimensao_objeto.dimensao_largura) if objeto_postal_obj.dimensao_objeto.dimensao_largura != '' else ''
            etree_dimensao_comprimento.text = unicode(objeto_postal_obj.dimensao_objeto.dimensao_comprimento) if objeto_postal_obj.dimensao_objeto.dimensao_comprimento != '' else ''
            etree_dimensao_diametro.text = unicode(objeto_postal_obj.dimensao_objeto.dimensao_diametro) if objeto_postal_obj.dimensao_objeto.dimensao_diametro != '' else ''
            
            etree_dimensao_objeto.append(etree_tipo_objeto)
            etree_dimensao_objeto.append(etree_dimensao_altura)
            etree_dimensao_objeto.append(etree_dimensao_largura)
            etree_dimensao_objeto.append(etree_dimensao_comprimento)
            etree_dimensao_objeto.append(etree_dimensao_diametro)

            etree_objeto_postal.append(etree_numero_etiqueta)
            etree_objeto_postal.append(etree_codigo_objeto_cliente)
            etree_objeto_postal.append(etree_codigo_servico_postagem)
            etree_objeto_postal.append(etree_cubagem)
            etree_objeto_postal.append(etree_peso)
            etree_objeto_postal.append(etree_rt1)
            etree_objeto_postal.append(etree_rt2)
            etree_objeto_postal.append(etree_destinatario)
            etree_objeto_postal.append(etree_nacional)
            etree_objeto_postal.append(etree_servico_adicional)
            etree_objeto_postal.append(etree_dimensao_objeto)
            etree_objeto_postal.append(etree_data_postagem_sara)
            etree_objeto_postal.append(etree_status_processamento)
            etree_objeto_postal.append(etree_numero_comprovante_postagem)
            etree_objeto_postal.append(etree_valor_cobrado)
            
            correios_log.append(etree_objeto_postal)

        # correios_log = parseDict(xml_dict, 'correioslog')
        soap_package = etree.tostring(correios_log, encoding='ISO-8859-1')
        return soap_package.replace('\n', '')