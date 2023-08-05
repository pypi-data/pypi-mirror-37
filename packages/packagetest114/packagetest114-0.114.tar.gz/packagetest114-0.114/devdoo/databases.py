#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Databases:
    def __init__(self, databases, status):
        # Status indica se o serviço está pronto
        self.ready = False
        self.status = status

        self.__databases = []
        self.__config(databases)

    # --------------------------------
    # __config
    # --------------------------------
    # Registra serviços na lista de serviços
    def __config(self, databases):
        if len(databases)>0:
            from database import Database
            for item in databases:
                self.__databases.append(Database(item, self.status))
        else:
            self.status.error("ERROR_DATABASE_CONFIG", None, ["Nao recebeu lista de database para configurar no serviço"])
