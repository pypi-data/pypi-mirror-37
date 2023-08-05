#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class DatabaseGet:
    # --------------------------------
    # one
    # --------------------------------
    # Realiza consulta na base de dados buscando um ou muitos documentos
    @staticmethod
    def one(dbPrepare):
        print "OPERATION-GETONE"
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera configurações
        db_fields = dbPrepare.fields()
        db_filter = dbPrepare.filter()

        # Consulta o base de dados
        # find_result = collection.find(db_filter, db_fields).skip(db_skip).sort(db_sort.items())
        find_result = collection.find_one(db_filter, db_fields)

        # Registra o total de elementos encontrados
        if (find_result is not None):
            totals = {"count": 1}
            is_success = True
        else:
            totals = {"count": 0}
            is_success = False

        return DatabaseGet.response_one(dbPrepare, find_result, db_filter, db_fields, is_success, totals)

    @staticmethod
    def response_one(dbPrepare, data, filter, fields, is_success, totals):
        result = {
            "id": dbPrepare.id(),
            "response": {
                "operation": "getOne",
                "success": is_success,
                "data": data,
                "totals": totals
            }
        }
        if dbPrepare.show_filter() or dbPrepare.show_fields() or dbPrepare.show_links():
            result["response"]["query"] = {}

            if dbPrepare.show_filter() == True:
                result["response"]["query"]["filter"] = filter

            if dbPrepare.show_fields() == True:
                result["response"]["query"]["fields"] = fields

            if dbPrepare.show_links() == True:
                result["response"]["query"]["links"] = {
                    "self": "https://api.predicthq.com/v1/endpoint/?offset=0&limit=10"
                }
        return result

    # --------------------------------
    # many
    # --------------------------------
    # Realiza consulta na base de dados buscando um ou muitos documentos
    @staticmethod
    def many(dbPrepare):
        print "OPERATION-MANY"
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera configurações
        db_fields = dbPrepare.fields()
        db_filter = dbPrepare.filter()
        db_limit = dbPrepare.limit()
        db_skip = dbPrepare.skip()
        db_sort = dbPrepare.sort()

        # Consulta o base de dados
        # find_result = collection.find(db_filter, db_fields).skip(db_skip).sort(db_sort.items())
        find_result = collection.find(db_filter, db_fields).skip(db_skip).sort(db_sort)

        # Obtém o resultado da consulta
        find_result_limit = find_result.limit(db_limit)

        if dbPrepare.show_totals() == True:
            totals = {
                "count": find_result_limit.count(),
                "total": find_result.count(),
                "skip": db_skip,
                "limit": db_limit
            }
        else:
            # Registra o total de elementos encontrados para retornar ao cliente
            totals = {
                "count": find_result.count()
            }

        links = {
            "previous": None,
            "next": "https://api.predicthq.com/v1/endpoint/?offset=10&limit=10",
            "self": "https://api.predicthq.com/v1/endpoint/?offset=0&limit=10"
        }

        return DatabaseGet.response("getMany", dbPrepare, find_result_limit, db_filter, db_fields, db_sort, totals, links)

    @staticmethod
    def response(operation, dbPrepare, data, filter, fields, sort, totals, links):
        result = {
            "id": dbPrepare.id(),
            "response": {
                "operation": operation,
                "success": True,
                "data": data,
                "totals": totals
            }
        }

        if dbPrepare.show_filter() or dbPrepare.show_fields() or dbPrepare.show_sort() or dbPrepare.show_links():
            result["response"]["query"] = {}

            if dbPrepare.show_filter() == True:
                result["response"]["query"]["filter"] = filter

            if dbPrepare.show_fields() == True:
                result["response"]["query"]["fields"] = fields

            if dbPrepare.show_sort() == True:
                result["response"]["query"]["sort"] = sort

            if dbPrepare.show_links() == True:
                result["response"]["query"]["links"] = links

        return result
