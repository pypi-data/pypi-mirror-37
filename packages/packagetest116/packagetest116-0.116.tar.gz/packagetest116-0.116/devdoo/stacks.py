#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections, time
from stack import Stack
from pprint import pprint

class Stacks:
    """Atualmente executando pedidos."""

    class Error(Exception):
        """Exceção levantada quando algo deu errado."""
        pass

    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, timeout, tries):
        """Cria um novo conjunto de solicitações vazio."""

        # Verifica se o timeout é válido
        # if timeout is not None and timeout < 0:
        #     raise Stacks.Error("o tempo limite deve ser não-negativo ou None")

        # Verifica se o número de tentativas é válido
        # if tries is not None and tries <= 0:
        #     raise Stacks.Error("as tentativas devem ser positivas ou None")

        # Cria as pilhas
        self.list_waiting = collections.deque()
        self.list_processing = collections.deque()

        # Lista temporária para remover requisições da pilha de processamento
        self.temp_stack_requests = {}
        self.timeout = timeout
        self.tries = tries

    # --------------------------------
    # add
    # --------------------------------
    def add(self, message):
        """Crie um novo objeto de solicitação e faça com que ele entre no sistema."""
        self.list_waiting.append(Stack(message, self.timeout, self.tries))

    # --------------------------------
    # process
    # --------------------------------
    def process(self, stack):
        """Defina um novo parâmetro de solicitação antes de enviá-lo para um worker."""

        # Adiciona a requisição na lista de processamento
        self.list_processing.append(stack)

        #print "PROCESS-->>", stack

        # Registra a requisição na fila temporária
        self.temp_stack_requests[stack.id] = stack

        stack.make_request()
        return stack

    # --------------------------------
    # has_waiting
    # --------------------------------
    def has_waiting(self):
        # Verifica se há algum pedido aguardando um worker
        return len(self.list_waiting) > 0

    # --------------------------------
    # get_stack
    # --------------------------------
    def get_stack(self):
        # Obtém o primeiro pedido na fila
        if self.has_waiting():
            # Remove requisição da lista de espera
            stack = self.list_waiting.popleft()

            # Adiciona processo na lista de processamento
            # Retorna o processo na requisição
            return self.process(stack)
        raise Stacks.Error("internal error")

    # --------------------------------
    # check_for_timeouts
    # --------------------------------
    def check_for_timeouts(self):
        """Verifica se algum pedido expirou. Se esse é o caso,
        coloca na fila novamente a menos que o número máximo de tentativas
        tenha sido alcançado. Retorna uma lista de pedidos expirados."""
        expired = []
        while self.list_processing and self.list_processing[0].timed_out():
            request = self.list_processing.popleft()

            print "check_for_timeouts--->>>", request

            del self.temp_stack_requests[request.id]
            if request.expired():
                expired.append(request)
            else:
                self.list_waiting.append(request)
        return expired

    # --------------------------------
    # remove
    # --------------------------------
    def remove(self, result):
        """Dada uma resposta, remove a solicitação correspondente da fila.
        Retornar a resposta para enviar se o pedido foi encontrado no sistema,
        nenhum caso (resposta tardia, por exemplo)."""
        id, content = result[0], result[1:]

        if id in self.temp_stack_requests:
            request = self.temp_stack_requests[id]
            self.list_processing.remove(request)
            del self.temp_stack_requests[id]

            return request.main_path + content

    # --------------------------------
    # next_timeout_ms
    # --------------------------------
    def next_timeout_ms(self):
        """Retorna o número de milisegundos até o próximo evento de tempo limite,
           ou None se não houver nenhum."""
        if self.list_processing:
            return 1000 * max(self.list_processing[0].deadline - time.time(), 0)
