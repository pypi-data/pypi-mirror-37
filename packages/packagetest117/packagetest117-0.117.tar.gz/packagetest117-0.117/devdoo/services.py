#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class Services:

    def __init__(self, services, status, use_database=False):
        # Status indica se o servico está pronto
        self.ready = False
        self.status = status
        self.use_database = use_database

        self.__services = dict()
        self.__config(services)

    # --------------------------------
    # __config
    # --------------------------------
    # Registra servicos na lista de servicos
    def __config(self, services):
        if len(services) > 0:
            from service import Service
            for item in services:
                service = Service(item, self.status, False, self.use_database)
                # Verifica se a configuracao é válida
                if (service is not None) and service.ready():
                    # Registra o servico no stack de servicos
                    self.__services[service.id] = service
                else:
                    self.status.error("INVALID_SERVICE", None, ["FALHA NA INICIALIZACAO DO SERVICO", service.id])
        else:
            self.status.error("ERROR_SERVICE_CONFIG", None, ["Nao recebeu lista de servico para configurar no broker"])

    # --------------------------------
    # find
    # --------------------------------
    # Localiza os servicos
    def find(self, service_id):
        if service_id in self.__services.keys():
            return self.__services[service_id]
        self.status.error("INVALID_SERVICE", None, ["Servico nao configurado", service_id])
        return None

    # --------------------------------
    # ready
    # --------------------------------
    # Retorna status indicando se houve algum erro no processo de configuracao dos servicos e se existe servicos para ser executado
    def ready(self):
        return self.status.ready() and (len(self.__services.keys()) > 0)

    # --------------------------------
    # __has_services
    # --------------------------------
    def __has_services(self, list_ids):
        error = False
        if (type(list_ids) == list) and (len(list_ids) > 0):
            for item in list_ids:
                if not re.match("^[0-9a-f]{24}$", Convert.to_str(item)):
                    error = True
        if error is True:
            self.status.error("INVALID_SERVICE", None, ["Lista de Servicos nao valida", list_ids])

        return self.status.ready()
