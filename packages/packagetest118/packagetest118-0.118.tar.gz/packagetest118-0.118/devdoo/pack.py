#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from check import Check
from convert import Convert
from bson.json_util import dumps
from pprint import pprint


class Pack:

    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, message, status):
        self.status = status

        self.auth = None
        self.id = None
        self.params = None
        self.network = None
        self.query = None
        self.body = None
        self.show = None
        self.info = None
        self.length_in = None
        self.length_out = None
        self.service_id = None
        self.connection = None
        self.open = None
        self.success = None
        self.time_start = None
        self.alerts = None

        self.__decode(message)
        print "connection_id::", self.id

    # --------------------------------
    # decode
    # --------------------------------
    def __decode(self, message):
        if (type(message) == list) and (len(message) == 1):
            message = message[0]
        if Check.is_string(message):
            # Converte o terceiro elemento da lista em object (dic)
            pack = Convert.to_object(message)
            # Verifica se é um objeto válido
            if Check.is_object(pack) and 'error' not in pack:
                for field in pack:
                    self.__dict__[field] = pack[field]
            else:
                self.status.error("CONFIGURATION_SERVICE", None, ["Arquivo de configuracao invalido"])
        else:
            self.status.error("CONFIGURATION_SERVICE", None, ["Arquivo de configuracao invalido"])


    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # send_error
    # --------------------------------
    # Montar mensagem de erro para ser retornada ao servidor rest
    # TODO: Preparar filtro para ser retornado ao cliente
    def send_error(self):
        message = {
            "error": "ERROR",
        }
        return [dumps(message)]

    # --------------------------------
    # to_print
    # --------------------------------
    def to_print(self, message=None):
        if message:
            print message, ":::------->>>"
        pprint(self.__dict__)
