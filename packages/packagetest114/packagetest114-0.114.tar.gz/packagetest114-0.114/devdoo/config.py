#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check import Check
from pprint import pprint

#TODO:: Remover classe Config

class Config(object):
    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, params, status):
        self.__ready = False

        self.id = None
        self.database = None
        self.brokers = None
        self.endpoint = None
        self.name = None
        self.type = None
        self.services = None

        self.status = status

        self.__init(params)

    # --------------------------------
    # __init
    # --------------------------------
    def __init(self, params):

        print "PARAMS", params.network

        if (params is not None) and params.ready():
            # Identificador do serviço
            self.id = Check.value_string("id", params.id, self.status)
            # Identificador do tipo de serviço (devdoo-broker|devdoo-database|devdoo-service)
            self.type = Check.value_string("type", params.type, self.status)

            if self.type == "devdoo-broker":
                self.services = Check.value_list("services", params.services, self.status)
                if Check.is_object(params.network):
                    self.network = params.network
                    self.endpoint = "tcp://*:" + str(self.network["port"])

            elif (self.type == "devdoo-service"):
                # Nome do serviço
                self.name = Check.value_string("name", params.name, self.status)
                #self.mongodb = Check.value_dict("mongodb", params.mongodb, self.status)
                #self.endpoint = Check.value_dict("endpoint", params.database, self.status)

            elif (self.type == "devdoo-database"):
                # Nome do serviço
                self.mongodb = Check.value_dict("mongodb", params.mongodb, self.status)
                self.collections = Check.value_dict("collections", params.mongodb, self.status)
                self.actions = Check.value_dict("actions", params.mongodb, self.status)
        else:
            self.status.error("INVALID_CONFIG", None, ["Falha na leitura de arquivo de configuracao"])

        return self.status.ready()

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        if self.status.ready() is False:
            pprint(self.status.to_list())
        return self.status.ready()

    def show(self):
        pprint(self.__dict__)
