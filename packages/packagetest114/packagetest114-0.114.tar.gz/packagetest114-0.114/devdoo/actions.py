#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datarest import DataRest
from check import Check
from validate import Validate
from status import Status

# TODO:: Fazer revisão completa da classe para fechar
# TODO:: Mover todas as mensagens de erros para a classe status
# TODO:: Remover todos os prints
class Actions(object):
    def __init__(self, message, service):
        self.service = service
        self.status = Status()
        self.endpoint = None

        self.database = service.database
        self.datarest = DataRest(message, self.database.id, self.status)
        self.validate = Validate(self.status)

        self.__config()
        self.status.to_print()

    # --------------------------------
    # action
    # --------------------------------
    def __config(self):
        print "DATAREST_READY", self.datarest.ready()
        print "SERVICE_READY", self.service.ready()

        if self.datarest.ready() and self.service.ready() and self.database.ready():
            source = self.datarest.source()
            method = self.datarest.method()

            self.endpoint = self.database.endpoint(method, source, self.status)

            # Verifica se o endereço da api existe
            if self.endpoint.ready():
                # Registra o tipo de retorno de dados deve executar
                self.datarest.result_type(self.endpoint.type)

                # if hasattr(self, self.endpoint.action) and self.datarest.validate_service(self.name, self.id):
                if hasattr(self, self.endpoint.action):
                    action = getattr(self, self.endpoint.action)
                    action(self.endpoint)
                else:
                    self.status.error("INVALID_ACTION", None, [source, self.service.name, self.endpoint.action, method])

            else:
                self.status.error("INVALID_ENDPOINT", None, [source, self.service.name, method])

        else:
            self.status.error("INVALID_SERVICE", None, ["NAO ESTA PRONTO PARA EXECUTAR SERVICO", "PARAMETROS FALTANDO"])

    # --------------------------------
    # find
    # --------------------------------
    def find(self, endpoint):
        # Define o tipo de ação que será executada no servidor de base de dados
        self.datarest.action("find")

        # Recupera o identificador da coleção
        self.datarest.collection(endpoint.collection)

        # Registra campos que devem ser retornados
        self.datarest.fields(endpoint.fields(self.datarest.public_access()))
        self.datarest.limit(endpoint.max_limit)

    # --------------------------------
    # insert
    # --------------------------------
    # Prepara documento para ser inserido base de dados
    def insert(self, endpoint):
        list_insert_data = []

        # Define o tipo de ação que será executada no servidor de base de dados
        self.datarest.action("insert")

        # Recupera o identificador da coleção
        self.datarest.collection(endpoint.collection)


        #self.database.show()

        # Prepara a lista de campos válidos que poderão ser inseridos na base de dados
        # Recebe a lista de erros em campos recebidos no body
        # Recebe a lista de erros em campos definido pelo desenvolvedor de microserviço
        list_scheme_clean = self.database.fields_insert(self.datarest.body(), endpoint)

        # Processa todos os campos registrados no schema para validar os valores e formatar
        for item_scheme_name in list_scheme_clean:
            # Recupera o esquema para validar e formatar
            item_scheme = list_scheme_clean[item_scheme_name]

            # Recupera o valor que deverá ser validado e formatado
            field_value = item_scheme["value"]

            # Valida o campo e valor
            # Recebe o nome do campo que será inserido na base de dados e depois retornado
            # Recebe o valor que deverá ser insrido na base de dados
            field_name, field_value = self.validate.field_insert(item_scheme_name, item_scheme, field_value, "custom_insert")

            # Verifica se o campo não está com erro de validação
            if field_value != '__error__' and field_value != '__ERROR__':
                # Registra o campo na lista de dados que deverá ser enviada para o servidor de base de dados
                if field_name != "id":
                    list_insert_data.append({"field": field_name, "value": field_value})

        # Prepara s lista de campos que será enviada para o servidor de base de dados
        # Prepara a lista de campos que devrá ser retornada do servidor depois de salvar na base de dados
        list_insert_data = self.__prepare_insert_data_fields(list_insert_data)

        # Registra os dados do documento
        self.datarest.data(list_insert_data)

        # Verificar se tem algo para gravar no banco, caso contrário, registra mensagem de error
        if len(list_insert_data) <= 0:
            self.status.error("NO_DATA_TO_INSERT", None, ['insert'])

    # --------------------------------
    # prepare_update_data
    # --------------------------------
    # Prepara lista de campos que podem ser atualizados no documento
    @staticmethod
    def prepare_update_data(list_data):
        result = dict()
        for item in list_data:
            # Registra o campo e valor na lista de campos válida do documento
            result[(item["field"])] = item["value"]
        return result

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # remove
    # --------------------------------
    def remove(self, endpoint):
        # Define o tipo de ação que será executada no servidor de base de dados
        self.datarest.action("remove")

        # Recupera o identificador da coleção
        self.datarest.collection(endpoint.collection)

    # --------------------------------
    # send_database
    # --------------------------------
    def send_database(self):
        return self.datarest.send_database()

    # --------------------------------
    # send_error
    # --------------------------------
    def send_error(self):
        return self.datarest.send_service_error()

    # --------------------------------
    # update
    # --------------------------------
    def update(self, endpoint):
        # Validar configuração de schema para update, erro developer
        if Check.is_scheme(endpoint.scheme):
            # Define o tipo de ação que será executada no servidor de base de dados
            self.datarest.action("update")

            # Recupera o identificador da coleção
            self.datarest.collection(endpoint.collection)

            update_data = dict()
            fields = ["_id"]
            for item_scheme in endpoint.scheme:
                obj_item_scheme = self.update_config(endpoint.scheme[item_scheme], endpoint.fields(self.datarest.public_access()))

                if len(obj_item_scheme.keys()) > 0:
                    fields = fields + obj_item_scheme.keys()
                    update_data[item_scheme] = obj_item_scheme

            # Registra os dados do documento
            self.datarest.data(update_data)

            # Registra campos que devem ser retornados
            self.datarest.fields(fields)

        else:
            self.status.error("INVALID_SCHEME_UPDATE", None, [])

    # --------------------------------
    # update_config
    # --------------------------------
    def update_config(self, scheme, fields_default):

        list_update_data = []

        # Prepara a lista de campos válidos que poderão ser inseridos na base de dados
        # Recebe a lista de erros em campos recebidos no body
        # Recebe a lista de erros em campos definido pelo desenvolvedor de microserviço
        list_scheme_clean = self.database.fields_update(self.datarest.body(), scheme, fields_default)

        print "LIST_SCHEME_CLEAN", list_scheme_clean

        # Processa todos os campos registrados no schema para validar os valores e formatar
        for item_scheme_name in list_scheme_clean:
            # Recupera o equema para validar e formatar
            item_scheme = list_scheme_clean[item_scheme_name]

            # Recupera o valor que deverá ser validado e formatado
            field_value = item_scheme["value"]

            # Valida o campo e valor
            # Recebe o nome do campo que será inserido na base de dados e depois retornado
            # Recebe o valor que deverá ser inserido na base de dados
            field_name, field_value = self.validate.field_update(item_scheme_name, item_scheme, field_value, "custom_update")

            # Verifica se o campo não está com erro de validação
            if field_value != '__error__' and field_value != '__ERROR__':
                # Registra o campo na lista de dados que deverá ser enviada para o servidor de base de dados
                if field_name != "id":
                    list_update_data.append({"field": field_name, "value": field_value})

        # Prepara a lista de campos que será enviada para o servidor de base de dados
        # Prepara a lista de campos que devrá ser retornada do servidor depois de salvar na base de dados
        list_update_data = self.prepare_update_data(list_update_data)

        # Verificar se tem algo para gravar no banco, caso contrário, registra mensagem de error
        if len(list_update_data) <= 0:
            self.status.error("NO_DATA_TO_UPDATE", None, [])

        return list_update_data

    # --------------------------------
    # __insert_data_join
    # --------------------------------
    # Função recursiva utilizada para tratar conflito de elementos filho no momento de gravar na base de dados
    #
    # data - Objeto contento dados existentes do mesmo grupo ou um objeto vazio para receber novos elementos
    # value - Dados que deverão ser inseridos no objeto
    def __insert_data_join(self, data, value):

        # Pega cada elemento do objeto valor
        for item in value:
            # Verifica se valor é um objeto
            # Verifica se o elemento filho valor é um objeto
            # Verifica se o elemento filho existe no objeto de dados
            if type(value) == dict and type(value[item]) == dict and type(data) == dict and item in data.keys():
                # Adiciona novo elemento no objeto de dados com o resultado da interação nos objetos filhos do objeto valor
                data[item] = self.__insert_data_join(data[item], value[item])

            # Verifica se valor é um objeto
            # Verifica se o elemento filho valor é um objeto
            elif type(value) == dict and type(data) == dict:
                # Adiciona o objeto valor como novo elemento no objeto de dados
                data[item] = value[item]

            # Verifica se o objeto dados é um objeto
            elif type(data) == dict:
                # Adiciona o valor como novo elemento no objeto de dados
                data[item] = value
        return data

    # --------------------------------
    # __prepare_insert_data_fields
    # --------------------------------
    # Prepara lista de campos que podem ser incluidos no documento
    # Prepara e registra a lista de campos que deverá ser retornada do servidor após a inclusão do documento na base de dados
    def __prepare_insert_data_fields(self, list_data):
        result = dict()
        fields = dict()

        for item in list_data:
            # Verifica se o nome do campo existe na lista que será incluida no documento
            if (item["field"]) in result.keys():
                # Caso não esteja na lista então o campo é incluido
                # Prepara objetos filhos no padrão permitido paraga registrar na base de dados
                result[(item["field"])] = self.__insert_data_join(result[(item["field"])], item["value"])
            else:
                # Registra o campo e valor na lista de campos válida do documento
                result[(item["field"])] = item["value"]

            # Adiciona o campo na lista de campos que devem ser retornados do servidor
            fields[(item["field"])] = True

        # Registra campos que devem ser retornados
        self.datarest.fields(fields)

        return result
