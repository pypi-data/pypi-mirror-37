#!/usr/bin/env python
# -*- coding: utf-8 -*-
from console import Console
from services import Services
from pprint import pprint
from socket import Socket

# --------------------------------
# Broker
# --------------------------------
'''
A classe Broker gerencia configurações do broker
'''

class Broker:

    '''
    Inicializa a classe

    :param broker_id: Identificador do broker
    :param status: Gerenciador de erros
    :param service_port: Porta do serviço
    :param has_connection_backend:  Status indica se deve configurar endpoind para conexão backend
    :param has_connect_frontend: Status indica se deve configurar endpoind para conexão frontend
    '''
    def __init__(self, broker_id, status, service_port=None, has_connection_backend=False, has_connect_frontend=False):
        # Variaveis privadas
        self.__sockets = dict()

        # Variaveis default
        self.network = None
        self.services = None
        self.type = None
        self.connect_backend = None
        self.connect_frontend = None

        # Variaveis parametros
        self.id = broker_id
        self.status = status
        self.has_connection_backend = has_connection_backend
        self.has_connect_frontend = has_connect_frontend
        self.service_port = service_port

        # Variaveis inicializadas
        self.connection = Console(status)

        # Verifica se o arquivo de configuração foi inicializado corretamente
        if self.__has_config() is not True:
            self.status.error("INVALID_SERVICE", None, ["FALHA NA INICIALIZACAO DE BROKER", broker_id])
            #self.status.to_print()
        else:
            self.status.show("BROKER_INIT", [self.id, self.type])
            #self.show("BROKER")

    # --------------------------------
    # __setitem__
    # --------------------------------
    '''
    Configura a classe para criar propriedades dinamicamente 
    '''
    def __setitem__(self, field, value):
        self.field = value

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
    # __bind
    # --------------------------------
    '''
    Configura endpoint de conexão backend
    Configura endpoint de conexão frontend
    Configura endpoint de conexão bind
    '''
    def __bind(self, service_port):
        # Verifica se uma rede foi definida e se a porta do serviço não foi fornecida
        if (self.network is not None) and (service_port is None):
            self.bind_frontend = "tcp://*:" + str(self.network["port"])
            print "Broker->Frontend:", self.bind_frontend

        # Verifica se uma rede foi definida e se a porta do serviço foi fornecida
        elif self.network and service_port:
            # Verifica se deve configurar um endpoint de conexão backend
            if self.has_connection_backend:
                self.connect_backend = "tcp://" + self.network["ip"] + ":" + str(service_port)
                print "Broker->Backend:", self.connect_backend

            # Caso contrário verifica se deve configurar um endpoint de conexão frontend
            elif self.has_connect_frontend:
                self.connect_frontend = "tcp://" + self.network["ip"] + ":" + str(self.network["port"])
                print "Broker->Frontend:", self.connect_frontend

            # Caso contrário configura um endpoint de conexão bind
            else:
                self.bind_backend = "tcp://*:" + str(service_port)
                print "Broker->Backend:", self.bind_backend
        else:
            self.status.error("ERROR_BROKER_CONFIG", None, ["Nao obteve dados de configuracao do network no broker", self.id])


    # --------------------------------
    # __config_services
    # --------------------------------
    '''
    Implementa configurações de serviços filhos do broker
    '''
    def __config_services(self):
        # Verifica se foi definido uma porta de serviço e se a lista de serviços existe
        if (self.service_port is None) and (self.services is not None):
            # Implementa lista de serviços
            self.services = Services(self.services, self.status, False)
            # Cria endpoints de conexões disponiveis para o broker
            self.__bind(service_port=None)
        # Caso contrário verifica se a porta foi fornecida
        elif self.service_port is not None:
            self.__bind(self.service_port)
        else:
            self.status.error("ERROR_BROKER_CONFIG", None, ["Nao obteve dados de configuracao dos servicos filhos do broker", self.id])

    # --------------------------------
    # __has_config
    # --------------------------------
    '''
    Implementa auto configuração do serviço
    Vai até o servidor de configuração buscar informações de configuração
    '''
    def __has_config(self):
        if self.id:
            # Recupera configurações no servidor de serviços API
            data_response = self.connection.load_config_broker(self.id)

            # Verifica se a resposta do servidor é válida
            if data_response.ready():
                # Registra na classe as propriedades da configuração
                data = data_response.values()
                for field in data:
                    self.__dict__[field] = data[field]

                # Configura serviços-filhos
                self.__config_services()
            else:
                self.status.error("ERROR_BROKER_CONFIG", None, ["Nao obteve dados de configuracao do broker", self.id])
        else:
            self.status.error("ERROR_BROKER_CONFIG", None, ["Nao recebeu identificador de broker", "--"])

        # Retorna se o status está pronto
        return self.status.ready()

    # --------------------------------
    # socket
    # --------------------------------
    '''
    Retorna o socket do serviço
    '''
    def socket(self, stack):
        socket = None
        if stack.ready():
            # Recupera o serviço
            service = self.services.find(stack.service_id)

            # Verifica se o serviço existe e possui um endpoint de backend na lista de sockets
            if (service is not None) and service.endpoint_backend() in self.__sockets.keys():
                socket = self.__sockets[service.endpoint_backend()]
            # Verifica se o serviço existe e o pacote é válido
            elif (service is not None) and stack.pack.ready():
                # Gera um novo Socket
                socket = Socket(service)
                # Verifica se o socket está pronto
                if socket.ready():
                    # Adiciona o novo socket na lista de sockets
                    self.__sockets[service.endpoint_backend()] = socket
                else:
                    # Gera um socket vazio
                    socket = Socket(None)
            else:
                # Gera um socket vazio
                socket = Socket(None)

            # Verifica se o socket não está pronto e adiciona mensagem de erro
            if socket.ready() is not True:
                stack.status.error("INVALID_SERVICE", None, ["Servico nao disponivel no servidor BROKER", stack.pack.service_id])

        # Retorna o Socket gerado
        return socket
