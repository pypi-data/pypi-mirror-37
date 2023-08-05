#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from broker import Broker
from status import Status
from yml import Yml
from stacks import Stacks

# --------------------------------
# DevdooBroker
# --------------------------------
'''
A classe DevdooBroker gerencia a conexão entre o rest e os serviços API
'''
# TODO:: Enviar para o servidor console a informação de falha de configuração
# TODO:: Enviar para o console mensagem de erro de serviço não disponível

class DevdooBroker(object):

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
    
    :return: void
    '''
    def __init__(self):
        super(DevdooBroker, self).__init__()

        # Variaveis default
        self.broker = None
        self.timeout = 2
        self.tries = 3
        self.zmq_socket_service = None
        self.zmq_socket_client = None
        self.id_zmq = None

        # Mensagens de alerta/erros
        self.status = Status()

        # Verifica se o arquivo de configuração foi inicializado corretamente
        if self.__has_config():
            # Inicializa o broker
            self.__init()
        else:
            self.status.error("INVALID_SERVICE", None, ["FALHA NA INICIALIZACAO DO SERVICO", "DEVDOO-BROKER"])
            self.status.to_print()

    # --------------------------------
    # __has_config
    # --------------------------------
    '''
    Obtem configurações do servico
    
    :return: void
    '''
    def __has_config(self):
        # Recupera o identificador do servico
        yml = Yml(self.status)
        self.id = yml.id()

        # Verifica se existe um identificador de servico válido
        if self.status.ready() and self.id:
            self.broker = Broker(broker_id=self.id, status=self.status)

        # Retorna o status do broker
        return self.status.ready()

    # --------------------------------
    # __init
    # --------------------------------
    def __init(self):
        '''
        Inicializa o serviço de Broker
        '''

        # Obtem o contexto ZMQ
        self.context = zmq.Context()

        # Inicializa o poll ZMQ
        self.poller = zmq.Poller()

        # Cria objeto de conexão para receber requisições do REST
        self.zmq_socket_client = self.context.socket(zmq.ROUTER)

        # Configura a porta de entrada para receber requisições do REST
        self.zmq_socket_client.bind(self.broker.bind_frontend)

        # Registra na lista de sockets o socket de entrada
        self.poller.register(self.zmq_socket_client, zmq.POLLIN)

        # Cria um novo gerenciador de solicitações vazio
        self.stacks = Stacks(self.timeout, self.tries)

        #self.status.show("DEVDOO_BROKER_INIT", [self.broker.id])

        # Executa o loop de operação
        self.run()

    # --------------------------------
    # operation
    # --------------------------------
    '''
    Permuta pacotes entre o frontend e o backend
    
    :return: void
    '''
    # TODO:: Verificar se existe um serviço para o service_id solicitado antes de tentar pegar na lista
    # TODO:: Verificar se o serviço está disponível antes de tentar fazer conexão
    # TODO:: Verificar se a mensagem foi corretamente convertida de string para dic antes de tentar pegar um elemento
    # TODO:: Procurar formas de desregistrar sockets que não obtiveram respostas dentro do tempo limite
    def operation(self):
        # Indica se há requisições em espera
        has_waiting = self.stacks.has_waiting()

        # Verifica se há requisições em espera
        if has_waiting:
            # Obtém o primeiro pedido da fila
            stack = self.stacks.get_stack()

            # Verifica se há um pedido aguardando
            if stack.ready():
                # Obtém o socket do serviço
                self.zmq_socket_service = self.broker.socket(stack)
                if self.zmq_socket_service.ready():
                    # Registra requisição no poller
                    self.poller.register(self.zmq_socket_service.connect_backend, zmq.POLLIN)

                    # Obtém a primeira mensagem do cliente da fila de espera
                    message = stack.message

                    # Envia o pacote para o Worker
                    self.zmq_socket_service.connect_backend().send_multipart(message)
                    # Recebe retorno do Worker
                    worker_result = self.zmq_socket_service.connect_backend().recv_multipart()

                    #print "WORKER_RESULT", worker_result[0]

                    # Prepara a mensagem recebida
                    content = self.stacks.remove(worker_result)

                    #print "CONTENT->>>", content

                    # Retorna a resposta ao cliente
                    self.zmq_socket_client.send_multipart(content)
                    self.poller.unregister(self.zmq_socket_service.connect_backend)

        # Obtém o tempo limite da próxima requisição
        timeout_ms = self.stacks.next_timeout_ms()

        # Itera a lista de poller e recupera um socket
        for (socket, event) in self.poller.poll(timeout_ms):
            # Verifica se o socket obtido é do tipo cliente
            if socket == self.zmq_socket_client:
                # Recebe solicitação do client REST
                message = self.zmq_socket_client.recv_multipart()

                # Cria um novo request com a mensagem do cliente e adiciona na lista de espera
                self.stacks.add(message)

        # Retorna para o cliente a mensagem contendo informações dos erros encontrados
        for stack in self.stacks.check_for_timeouts():
            self.zmq_socket_client.send_multipart(stack.send_error())

        # TERCEIRA OPERAÇÂO
        # Verifica se há requisições em espera
        '''
        if has_waiting and self.zmq_socket_service.ready():
            # Remove a requisição do poller
            if self.zmq_socket_service and (self.zmq_socket_service.connect_backend in self.poller):
                self.poller.unregister(self.zmq_socket_service.connect_backend)
            else:
                self.status.error("INVALID_SERVICE", None,
                    ["XXX Falha na configuracao do zmq_socket_service.connect_backend ", self.broker.id])
        '''

        # Imprime mensagens de erro/status
        self.status.to_print()

    # --------------------------------
    # run
    # --------------------------------
    '''
    Executa a operação em um loop infinito
    '''
    def run(self):
        # Executa indefinidamente
        while True:
            try:
                self.operation()
            except DevdooBroker.Error:
                # except Exception as inst:
                self.status.error("SERVICE_FAILURE", None, ["FALHA NA EXECUCAO DO SERVICO", "DEVDOO-BROKER"])
                self.status.to_print()
