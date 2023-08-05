#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

# --------------------------------
# DataResponse
# --------------------------------
'''
A classe Response gerencia o retorno de consulta no servidor de configuração
'''


class DataResponse:
    # --------------------------------
    # __init__
    # --------------------------------
    '''
    Inicializa a classe

    :param data: Documento retornado do serviço de API
    :param status: Gerenciador de erros
    '''

    def __init__(self, data, status):
        # Variaveis privadas
        self.__values = None

        # Variaveis parametros
        self.status = status

        self.__config(data)

    # --------------------------------
    # ready
    # --------------------------------
    '''
    Status indica se está pronto
    
    :return: void
    '''

    def ready(self):
        return self.status.ready()

    # --------------------------------
    # show
    # --------------------------------
    '''
    Imprime propriedade/valor do objeto
    
    :param title: Título identificador
    :return: void
    '''

    def show(self, title=None):
        if title is not None:
            print title, ":::------->>>"
        pprint(self.__values)

    # --------------------------------
    # values
    # --------------------------------
    '''
    Retorna os valores obtidos no servidor de serviços API
    
    :return: void
    '''

    def values(self):
        return self.__values

    # --------------------------------
    # __config
    # --------------------------------
    '''
    Verifica se os dados retornados são válidos
    
    :param data: Dados retornados do servidor de serviços API
    :return: void
    '''

    def __config(self, data):
        # Verifica se os dados é do tipo lista ou dicionário e se possui valor atribuído
        if ((type(data) == list) and (len(data) > 0)) or ((type(data) == dict) and (len(data.keys()) > 0)):
            self.__values = data
        else:
            self.status.error("DATA_RESPONSE", None,
                              ["Falha da configuracao de dados retornados do servidor de servicos API"])
