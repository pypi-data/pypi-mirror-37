#!/usr/bin/env python
# -*- coding: utf-8 -*-

from broker import Broker

# --------------------------------
# Brokers
# --------------------------------
'''
A classe Brokers gerencia a lista de brokers utilizada pelo serviço
'''


class Brokers:
    '''
    Inicializa a classe

    :param service_port: Porta do serviço
    :param brokers: Objeto de broker para registrar
    :param status: Gerenciador de erros
    :param has_connect_backend:  Status indica se deve configurar endpoind para conexão backend
    :param has_connect_frontend: Status indica se deve configurar endpoind para conexão frontend
    '''

    def __init__(self, service_port, brokers, status, has_connect_backend=False, has_connect_frontend=False):

        # Variaveis privadas
        self.__brokers = []

        # Variaveis parametros
        self.brokers = brokers
        self.has_connect_backend = has_connect_backend
        self.has_connect_frontend = has_connect_frontend
        self.status = status
        self.service_port = service_port

        self.__config()

    # --------------------------------
    # available
    # --------------------------------
    '''
    Recupera o broker disponível para atender o serviço
    '''

    def available(self):
        return self.__brokers[0]

    # --------------------------------
    # __config
    # --------------------------------
    # Registra brokers na lista de brokers
    def __config(self):
        if len(self.brokers) > 0:
            for broker_id in self.brokers:
                self.__brokers.append(
                    Broker(broker_id, self.status, self.service_port, self.has_connect_backend, self.has_connect_frontend))
        else:
            self.status.error("ERROR_BROKER_CONFIG", None, ["Nao recebeu lista de brokers para configurar no servico"])
