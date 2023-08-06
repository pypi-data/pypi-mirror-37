from zeep import Client as ZeepClient
from zeep.plugins import HistoryPlugin
from lxml import etree
class Client:

    CORREIOS_WEBSERVICES = {
        'sigep-production': (
            'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl',
            'AtendeCliente-production.wsdl',
        ),
        'sigep-test': (
            'https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl',
            'AtendeCliente-test.wsdl',
        ),
        'websro': (
            'https://webservice.correios.com.br/service/rastro/Rastro.wsdl',
            'Rastro.wsdl',
        ),
        'freight': (
            'http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL',
            'CalcPrecoPrazo.asmx',
        ),
    }

    def __init__(self, username, password, environment='sigep-test'):
        self.username = username
        self.password = password
        self.WS = self.CORREIOS_WEBSERVICES[environment]
        
    def _request(self, method, *args, **kwargs):
        history = HistoryPlugin()
        client = ZeepClient(self.WS[0], plugins=[history])
        kwargs['usuario'] = self.username
        kwargs['senha'] = self.password

        fn = getattr(client.service, method)
        
        # print envelope for debug purposes
        # node = client.create_message(client.service, method, **kwargs)
        # print etree.tostring(node, encoding='iso-8859-1'), 'NODE'
        result = fn(**kwargs)
        return result

    def get_available_service(self, *args, **kwargs):

        params = {
            'codAdministrativo': kwargs['codAdministrativo'],
            'numeroServico': kwargs['numeroServico'],
            'cepOrigem': kwargs['cepOrigem'],
            'cepDestino': kwargs['cepDestino']
        }
        return self._request('verificaDisponibilidadeServico', **params)

    def get_card_services(self, *args, **kwargs):
        params = {
            'idContrato': kwargs['contract_id'],
            'idCartaoPostagem': kwargs['id_postcard'],
        }

        return self._request('buscaCliente', **params)

    def get_postcard_status(self, *args, **kwargs):
        params = {
            'numeroCartaoPostagem': kwargs['postcard_number']
        }

        return self._request('getStatusCartaoPostagem', **params)

    def get_address(self, zipcode):
        params = {
            'cep': zipcode
        }

        return self._request('buscaCEP', **params)

    def get_range_tag(self, *args, **kwargs):
        params = {
            'tipoDestinatario': kwargs['recipient_type'],
            'identificador': kwargs['cnpj'],
            'idServico': kwargs['service'],
            'qtdEtiquetas': kwargs['qtd'],
        }
        
        list_tags = self._request('solicitaEtiquetas', **params).split(',')
        
        return list_tags if params['qtdEtiquetas'] > 1 else [list_tags[0]]

    def get_checker_digit(self, zipcodes):
        params = {
            'etiquetas': zipcodes
        }

        return self._request('geraDigitoVerificadorEtiquetas', **params)

    def close_pre_post_list(self, *args, **kwargs):
        params = {
            'idPlpCliente': kwargs['id_plp'],
            'cartaoPostagem': kwargs['id_postcard'],
            'listaEtiquetas': kwargs['list_tags'],
            'xml': kwargs['xml']
        }

        return self._request("fechaPlpVariosServicos", **params)

    def recover_xml_plp(self, id_plp):
        params = {
            'idPlpMaster': id_plp
        }

        return self._request("solicitaXmlPlp", **params)