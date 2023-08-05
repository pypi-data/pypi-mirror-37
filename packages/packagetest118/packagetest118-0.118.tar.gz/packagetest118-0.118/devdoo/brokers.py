#!/usr/bin/env python
# -*- coding: utf-8 -*-

from broker import Broker

# --------------------------------
# Brokers
# --------------------------------
'''
Gerencia a lista de brokers utilizada pelo serviço
'''


class Brokers:
    '''
    Inicializa a classe

    :param service_port: Porta do serviço
    :param brokers: Objeto de broker para registrar
    :param status: Gerenciador de erros
    :param has_connection_backend:  Status indica se deve configurar endpoind para conexão backend
    :param has_connect_frontend: Status indica se deve configurar endpoind para conexão frontend
    '''

    def __init__(self, service_port, broker_id, status, has_connection_backend=False, has_connect_frontend=False):
        # Variaveis privadas
        self.__brokers = []
        self.__brokers.append(
            Broker(broker_id, status, service_port, has_connection_backend, has_connect_frontend)
        )

        # --------------------------------
        # available
        # --------------------------------
        '''
        Recupera o broker disponível para atender o serviço
        '''

    def available(self):
        return self.__brokers[0]
