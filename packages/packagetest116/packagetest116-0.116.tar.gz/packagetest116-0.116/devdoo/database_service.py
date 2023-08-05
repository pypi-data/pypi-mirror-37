#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bson
import time
from bson import ObjectId
from datetime import datetime
from convert import Convert
from status import Status
from bson.json_util import dumps
from pprint import pprint

from database_prepare import DatabasePrepare
from database_get import DatabaseGet
from database_post import DatabasePost
from database_delete import DatabaseDelete
from database_put import DatabasePut


class DatabaseService:

    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, message, service):
        self.status = Status()
        self.dbPrepare = DatabasePrepare(message, service, self.status)
        self.__result = {"ERROR": "ERROR DatabaseService"}
        self.__action()

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # result
    # --------------------------------
    def result(self):
        return dumps(self.__result)

    # --------------------------------
    # getOne
    # --------------------------------
    # Realiza consulta na base de dados retornando um unico documento
    def getOne(self):
        self.__result = DatabaseGet.one(self.dbPrepare)

    # --------------------------------
    # getMany
    # --------------------------------
    # Realiza consulta na base de dados retornando uma lista de documentos
    def getMany(self):
        self.__result = DatabaseGet.many(self.dbPrepare)

    # --------------------------------
    # postOne
    # --------------------------------
    # Insere um documento na base de dados
    def postOne(self):
        self.__result = DatabasePost.post_one(self.dbPrepare)

    # --------------------------------
    # postMany
    # --------------------------------
    # Insere um documento na base de dados
    def postMany(self):
        self.__result = DatabasePost.post_many(self.dbPrepare)

    # --------------------------------
    # deleteOne
    # --------------------------------
    # Remove um documento na base de dados
    #
    def deleteOne(self):
        self.__result = DatabaseDelete.one(self.dbPrepare)

    # --------------------------------
    # deleteMany
    # --------------------------------
    # Remove uma lista de documento na base de dados
    #
    def deleteMany(self):
        self.__result = DatabaseDelete.many(self.dbPrepare)

    # --------------------------------
    # send
    # --------------------------------
    def send(self):
        return self.datarest.send_database()

    # --------------------------------
    # putOne
    # --------------------------------
    def putOne(self):
        self.__result = DatabasePut.one(self.dbPrepare)

    # --------------------------------
    # putMany
    # --------------------------------
    def putMany(self):
        self.__result = DatabasePut.many(self.dbPrepare)

    # --------------------------------
    # __action
    # --------------------------------
    def __action(self):
        operation = self.dbPrepare.operation()
        if hasattr(self, operation):
            method = getattr(self, operation)
            method()
        else:
            self.status.error("INVALID_ACTION_DB", None, [operation])
