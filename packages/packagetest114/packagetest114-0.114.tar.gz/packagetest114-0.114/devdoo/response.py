#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


# --------------------------------
# Response
# --------------------------------
# A classe Response gerencia o retorno de consulta no servidor de configuração
class Response:
    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, service_id, data, status):
        self.__ready = False
        self.__data = None
        self.__id = service_id

        self.status = status
        self.__check(service_id, data)

    # --------------------------------
    # data
    # --------------------------------
    # Retorna os dados de configuração
    def data(self):
        return self.__data

    # --------------------------------
    # ready
    # --------------------------------
    # Status indica se os dados estão prontos
    def ready(self):
        return self.__ready

    # --------------------------------
    # show
    # --------------------------------
    # Imprime propriedade/valor do objeto
    def show(self, message=None):
        if message:
            print message, self.__id, ":::------->>>"
        pprint(self.__data)

    # --------------------------------
    # __check
    # --------------------------------
    # Verifica se os dados retornados são válidos
    '''
    :param service_id: Identificador do serviço
    :param data: Dados retornados do serviço de configuração
    :return: void
    '''

    def __check(self, service_id, data):
        # Verifica se os dados é do tipo lista ou dicionário e se possui valor atribuído
        if ((type(data) == list) and (len(data) > 0)) or ((type(data) == dict) and (len(data.keys()) > 0)):
            self.__data = data
            self.__ready = True
        else:
            self.status.error("RESPONSE", None, ["Configuracao de servico nao encontrada", service_id])

        #self.show("RESPONSE")
