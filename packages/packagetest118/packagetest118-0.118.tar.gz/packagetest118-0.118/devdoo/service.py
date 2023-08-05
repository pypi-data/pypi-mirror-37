#!/usr/bin/env python
# -*- coding: utf-8 -*-
from console import Console
from brokers import Brokers
from database_mongo import DatabaseMongo
from pprint import pprint

# --------------------------------
# Service
# --------------------------------
'''
A classe Service gerencia todas as interações do serviço
'''
class Service:

    # --------------------------------
    # __init__
    # --------------------------------
    '''
    Inicializa a classe

    :param service_id: Identificador do serviço
    :param status: Gerenciador de erros
    :param has_connection_backend: Indica se deve configurar endpoind para conexão backend
    '''
    def __init__(self, service_id, status, has_connection_backend=False, use_database=True):
        # Variaveis default
        self.brokers = None
        self.database = None
        self.mongodb = None
        self.network = None
        self.use_database = use_database

        # Variaveis de parametros
        self.id = service_id
        self.status = status
        self.has_connection_backend = has_connection_backend

        # Variaveis inicializadas
        self.connection = Console(self.status)

        # Verifica se o arquivo de configuração foi inicializado corretamente
        if self.__has_config() is not True:
            self.status.error("INVALID_SERVICE", None, ["FALHA NA INICIALIZACAO DO SERVICO", service_id])
            #self.status.to_print()
        else:
            self.status.show("SERVICE_INIT", [self.id])

    # --------------------------------
    # broker_connect_backend
    # --------------------------------
    '''
    Recupera o endpoint de conexão connect_backend
    '''
    def broker_connect_backend(self):
        if self.brokers is not None:
            broker = self.brokers.available()
            return broker.connect_backend
        else:
            self.status.error("INVALID_BROKER", None, ["Nao foi encontrado broker disponivel para obter o 'connect_backend'.", self.id])

    # --------------------------------
    # endpoint_backend
    # --------------------------------
    '''
    Obtém o endereço utilizado pelo serviço para conectar o broker seguinte
    '''
    def endpoint_backend(self):
        broker = self.brokers.available()
        # Verifica se o objeto de broker foi criado e se está válido
        if broker and broker.ready():
            return broker.bind_backend
        else:
            self.status.error("INVALID_SERVICE", None, ["Nao foi encontrado broker disponivel par obter o 'endpoint_backend'.", self.id])

    # --------------------------------
    # ready
    # --------------------------------
    '''
    Status indica se está pronto
    
    :return: void
    '''
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # show
    # --------------------------------
    '''
    Imprime propriedade/valor do objeto

    :param title: Título identificador
    :return: void
    '''
    def show(self, title=None):
        if title is not None:
            print title, ":::------->>>"
        pprint(self.__dict__)

    # --------------------------------
    # __has_config
    # --------------------------------
    '''
    Implementa auto configuração do serviço
    Vai até o servidor de configuração buscar informações
    
    :return: boolean
    '''
    def __has_config(self):
        if self.id:
            # Recupera configurações no servidor de serviços API
            data_response = self.connection.load_config_service(self.id)

            # Verifica se a resposta do servidor é válida
            if data_response.ready():
                # Registra na classe as propriedades da configuração
                data = data_response.values()
                for field in data:
                    self.__dict__[field] = data[field]

                # Configura serviços-filhos
                if self.use_database:
                    self.__config_database()

                self.__config_network()
        else:
            self.status.error("ERROR_SERVICE_CONFIG", None, ["Não recebeu identificador de serviço"])

        return self.status.ready()

    # --------------------------------
    # __config_brokers
    # --------------------------------
    '''
    Implementa configurações de brokers-filhos do serviço

    :return: void
    '''
    def __config_brokers(self, service_port):
        if self.broker_id and self.network:
            self.brokers = Brokers(service_port, self.broker_id, self.status, self.has_connection_backend)
        else:
            self.status.error("ERROR_SERVICE_CONFIG", None, ["Nao obteve dados de configuracao de brokers do servico", self.id])

    # --------------------------------
    # __config_database
    # --------------------------------
    '''
    Implementa configurações de database-filho do serviço

    :return: void
    '''
    def __config_database(self):
        if self.mongodb is not None:
            self.dbMongo = DatabaseMongo(self.mongodb, self.status)

    # --------------------------------
    # __network
    # --------------------------------
    '''
    Implementa configuração de rede do serviço

    :return: void
    '''
    def __config_network(self):
        if self.network:
            self.__config_brokers(self.network["port"])
        else:
            self.status.error("ERROR_BROKER_CONFIG", None, ["Nao obteve dados de configuracao do network no service", self.id])
