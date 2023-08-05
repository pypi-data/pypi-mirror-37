#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from service import Service
from status import Status
from yml import Yml
from pprint import pprint
from database_service import DatabaseService
from pymongo import MongoClient

# --------------------------------
# DevdooDatabase
# --------------------------------
'''
A classe DevdooDatabase prepara todas as configurações database dos serviços API
'''


# TODO:: Enviar para o servidor console a informação de falha de configuração
class DevdooDatabase(object):
    # --------------------------------
    # Error
    # --------------------------------
    # TODO:: Remover classe de error
    class Error(Exception):
        pass

    # --------------------------------
    # __init__
    # --------------------------------
    '''
    Inicializa a classe
    '''

    def __init__(self):
        super(DevdooDatabase, self).__init__()

        # Mensagens de alerta/erros
        self.status = Status()

        # Verifica se o arquivo de configuração foi inicializado corretamente
        if self.__has_config():
            self.__init()
        else:
            self.status.error("INVALID_SERVICE", None, ["FALHA NA INICIALIZACAO DO SERVICO", "DEVDOO-SERVICE"])
            self.status.to_print()

    # --------------------------------
    # __has_config
    # --------------------------------
    '''
    Obtem configurações do servico
    
    :return: boolean
    '''

    def __has_config(self):
        # Recupera o identificador do servico
        yml = Yml(self.status)
        service_id = yml.id()

        # Verifica se existe um identificador do servico
        if self.status.ready() and service_id:
            self.service = Service(service_id, self.status, True)

        # Retorna o status do serviço de API
        return self.status.ready() and self.service and self.service.ready()

    # --------------------------------
    # __init
    # --------------------------------
    '''
    Inicializa o serviço
    
    :return: void
    '''

    def __init(self):
        # Cria contexto ZMQ
        context = zmq.Context()

        # Adaptador de conexão broker primário
        self.zmq_socket_rest = context.socket(zmq.REP)
        self.zmq_socket_rest.connect(self.service.broker_connect_backend())

        print "Service->Backend:", self.service.broker_connect_backend()

        # Executa o loop da operação
        self.run()

    # --------------------------------
    # operation
    # --------------------------------
    '''
    Executa a ação do Serviço
    '''

    def operation(self):
        # Recebe mensagem do servidor cliente
        message = self.zmq_socket_rest.recv_multipart()
        self.dbService = DatabaseService(message, self.service)

        # Verifica se o servico está pronto
        if self.dbService.ready():
            self.zmq_socket_rest.send(self.dbService.result())
            print ("SOCKET VALIDO VOLTOU <<<<------")

        # Em caso de falha
        else:
            # Nao processa a operação e envia mensagem de retorno para o cliente
            self.zmq_socket_rest.send(self.dbService.result())
            print ("SOCKET FALHOU E VOLTOU <<<<------")

    # --------------------------------
    # run
    # --------------------------------
    #
    '''
    Executa a operação em um loop infinito

    :return: void
    '''

    # TODO:: Implementar ping de verificação de disponibilidade do serviço
    def run(self):
        while True:
            try:
                self.operation()
            except DevdooDatabase.Error:
                # except Exception as inst:
                #    print "API::RUN::ERROR", inst.args
                self.status.error("SERVICE_FAILURE", None, ["FALHA NA EXECUCAO DO SERVICO", "DEVDOO-SERVICE"])
                #self.status.to_print()
