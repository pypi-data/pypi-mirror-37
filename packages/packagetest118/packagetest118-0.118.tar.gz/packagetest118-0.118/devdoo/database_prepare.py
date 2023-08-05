#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check import Check
from convert import Convert
from status import Status
from pack import Pack
from pymongo.collection import Collection
import time, copy
import datetime
from bson.timestamp import Timestamp
import bson
from pprint import pprint


# TODO:: Fazer revisão completa da classe para fechar
# TODO:: Mover todas as mensagens de erros para a classe status
# TODO:: Remover todos os prints
class DatabasePrepare(object):

    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, message, service, status):
        self.service = service
        self.status = status
        # self.database = service.database
        self.dbMongo = service.dbMongo
        self.pack = Pack(message, status)
        self.pack.to_print('PACK-->')

    # --------------------------------
    # action
    # --------------------------------
    def action(self):
        '''
        Identifica a acao que devera ser executada pelo servico
        :return: Identificador da acao
        '''
        return self.pack.params["action"]

    # --------------------------------
    # operation
    # --------------------------------
    def operation(self):
        '''
        Identifica a operação que devera ser executada pelo servico
        :return: Identificador da operacao
        '''
        return self.pack.params["operation"]

    def body(self):
        data = self.pack.body
        return data

    # --------------------------------
    # collection
    # --------------------------------
    def collection(self):
        '''
        Recupera os nomes do banco de dados e da colecao
        Verifica se o nome da colecao esta registrado no servico
        Verifica se o objeto da colecao e valido

        :return: Objeto Pymongo::collection
        '''

        database_name = self.pack.params["info"]["database"]["name"]
        collection_name = self.pack.params["info"]["database"]["collection"]

        # Verfica se a colecao existe
        # has_collection = collection_name in self.dbMongo.collections
        # if has_collection:
        collection = self.dbMongo.collection(database_name, collection_name)
        # Verifica se conseguiu um objeto de colecao valido
        if type(collection) == Collection:
            return collection
        else:
            self.status.error("INVALID_DATABASE_CONNECTION", None, ["Falha para conectar no banco de dados", database_name])
        # else:
        #    self.status.error("INVALID_COLLECTION", None, ["Colecao nao registrada no servico", collection_name])

    # --------------------------------
    # collection_changes
    # --------------------------------
    def collection_changes(self):
        '''
        Recupera os nomes do banco de dados e da colecao
        Verifica se o nome da colecao esta registrado no servico
        Verifica se o objeto da colecao e valido

        :return: Objeto Pymongo::collection
        '''

        database_name = self.pack.params["info"]["database"]["name"]
        collection_name = self.pack.params["info"]["database"]["collection"]

        # Verfica se a colecao existe
        # has_collection = collection_name in self.dbMongo.collections
        # if has_collection:
        collection = self.dbMongo.collection_changes(database_name, collection_name)
        # Verifica se conseguiu um objeto de colecao valido
        if type(collection) == Collection:
            return collection
        else:
            self.status.error("INVALID_DATABASE_CONNECTION", None, ["Falha para conectar no banco de dados", database_name])
        # else:
        #    self.status.error("INVALID_COLLECTION", None, ["Colecao nao registrada no servico", collection_name])


    # --------------------------------
    # collection_trash
    # --------------------------------
    def collection_trash(self):
        '''
        Recupera os nomes do banco de dados e da colecao
        Verifica se o nome da colecao esta registrado no servico
        Verifica se o objeto da colecao e valido

        :return: Objeto Pymongo::collection
        '''

        database_name = self.pack.params["info"]["database"]["name"]
        collection_name = self.pack.params["info"]["database"]["collection"]

        # Verfica se a colecao existe
        # has_collection = collection_name in self.dbMongo.collections
        # if has_collection:
        collection = self.dbMongo.collection_trash(database_name, collection_name)
        # Verifica se conseguiu um objeto de colecao valido
        if type(collection) == Collection:
            return collection
        else:
            self.status.error("INVALID_DATABASE_CONNECTION", None, ["Falha para conectar no banco de dados", database_name])
        # else:
        #    self.status.error("INVALID_COLLECTION", None, ["Colecao nao registrada no servico", collection_name])

    # --------------------------------
    # fields
    # --------------------------------
    def fields(self):
        #TODO::Verificar se tem ID de aplicação no filtro
        return self.pack.query["fields"]

    # --------------------------------
    # fieldsUpdate
    # --------------------------------
    def fieldsUpdate(self):
        fields = self.pack.query["fields"]
        fields["_info.user.change_id"] = True
        fields["_info.document.checksum"] = True
        fields["_info.document.changed_at"] = True
        fields["_info.document.size"] = True
        return fields

    # --------------------------------
    # filter
    # --------------------------------
    def filter(self):
        return self.pack.query["filter"]

    # --------------------------------
    # id
    # --------------------------------
    def id(self):
        return self.pack.id

    # --------------------------------
    # info
    # --------------------------------
    def info(self, data):
        ts = time.time()
        tmpTime = datetime.datetime.fromtimestamp(ts, None)
        self.pack.body["_info"]["document"]["created_at"] = tmpTime
        self.pack.body["_info"]["document"]["changed_at"] = tmpTime

        # TODO:: Implementar métricas de utilização e consumo dos serviços
        self.pack.body["_info"]["document"]["size"] = len(bson.BSON.encode(data)) + (len(bson.BSON.encode(data)) * 1.5)
        self.pack.body["_info"]["document"]["checksum"] = Convert.to_checksum(data)
        return self.pack.body

    # --------------------------------
    # info_update
    # --------------------------------
    def info_update(self, data):
        ts = time.time()
        tmpTime = datetime.datetime.fromtimestamp(ts, None)
        tmp_data = []

        for item in data:
            if item != "_info":
                tmp_data.append({item: data[item]})
            else:
                print "data[item]", data[item]["user"]
                _info = {
                    "document": {
                        "checksum": data[item]["document"]["checksum"],
                        "size": data[item]["document"]["size"]
                    },
                    "user": data[item]["user"]
                }
                tmp_data.append({"_info": _info})

        checksum = Convert.to_checksum(tmp_data)
        self.pack.body["$set"]["_info.document.changed_at"] = tmpTime

        '''
        self.pack.body = {
            "$set": {"_info.document.changed_at": tmpTime},
            "$inc": {"total_occurrences": 1}
        }
        self.pack.body
        '''

        print "self.pack.body", self.pack.body

        # TODO:: Atualizar dados do checksum e size após realizar update
        # self.pack.body["$set"]["_info.document.checksum"] = Convert.to_checksum(data)

        return checksum

    def change_id(self, data):
        print "DATA"
        pprint(data)
        return Convert.to_checksum(data)

    # --------------------------------
    # limit
    # --------------------------------
    def limit(self):
        return self.pack.query["limit"]

    # --------------------------------
    # skip
    # --------------------------------
    def skip(self):
        return self.pack.query["skip"]

    # --------------------------------
    # sort
    # --------------------------------
    def sort(self):
        return (self.pack.query["sort"]).items()

    # --------------------------------
    # show_filter
    # --------------------------------
    def show_filter(self):
        return self.pack.query["show"]["filter"]

    # --------------------------------
    # show_fields
    # --------------------------------
    def show_fields(self):
        return self.pack.query["show"]["fields"]

    # --------------------------------
    # show_sort
    # --------------------------------
    def show_sort(self):
        return self.pack.query["show"]["sort"]

    # --------------------------------
    # show_links
    # --------------------------------
    def show_links(self):
        return self.pack.query["show"]["links"]

    # --------------------------------
    # show_totals
    # --------------------------------
    def show_totals(self):
        return self.pack.query["show"]["totals"]
