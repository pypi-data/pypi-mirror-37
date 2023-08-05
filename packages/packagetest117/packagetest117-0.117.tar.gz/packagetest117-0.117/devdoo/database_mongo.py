#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import pymongo

class DatabaseMongo:
    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, params, status):
        self.status = status
        self.collections = None
        self.mongodb = None
        self.mongo_server = None

        self.__config(params)

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # __collection
    # --------------------------------
    # Recupera instancia da coleção que receberá interação na base de dados
    def collection(self, database, collection):
        if self.mongo_server:
            # Recupera o base de dados mongo db
            database = self.mongo_server[database]
            # Recupera/Cria a coleção mongo db
            return database[collection]

    # --------------------------------
    # collection_changes
    # --------------------------------
    def collection_changes(self, database, collection):
        if self.mongo_server:
            # Recupera o base de dados mongo db
            database = self.mongo_server[database]
            # Recupera/Cria a coleção mongo db
            return database[collection + "_changes"]

    # --------------------------------
    # __collection_trash
    # --------------------------------
    def collection_trash(self, database, collection):
        if self.mongo_server:
            # Recupera o base de dados mongo db
            database = self.mongo_server[database]
            # Recupera/Cria a coleção mongo db
            return database[collection + "_trash"]

    # --------------------------------
    # __config
    # --------------------------------
    # Implementa auto configuração do broker
    # Vai até o servidor de configuração buscar informações de configuração para o broker
    def __config(self, params):
        for field in params:
            self.__dict__[field] = params[field]
        self.__prepare_mongo()

    def __prepare_mongo(self):
        # Conecta ao banco de dados
        '''
        self.mongo_server = MongoClient(
            self.ip,
            username=self.username,
            password=self.password,
            authSource=self.database,
            authMechanism='SCRAM-SHA-1',
            port=self.port)
        '''
        self.mongo_server = MongoClient(["mongodb://devdoo:mudar123@mdb-master.soocializer.com.br:27017", "mdb-slave1.soocializer.com.br:27017", "mdb-slave2.soocializer.com.br:27017"], replicaSet='devdoo')
