#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq

# --------------------------------
# Socket
# --------------------------------
class Socket:

    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, service):
        self.__ready = False
        self.__connect_backend = None
        self.backend = None
        self.__service = service

        # Verifica se o serviço existe e está pronto
        if (service is not None) and service.ready():
            self.backend = service.endpoint_backend()

            # Cria contexto ZMQ
            context = zmq.Context()
            
            # Abre portas para os Serviços no backend
            self.__connect_backend = context.socket(zmq.DEALER)
            self.__connect_backend.bind(service.endpoint_backend())
            self.__ready = True

    # --------------------------------
    # connect_backend
    # --------------------------------
    def connect_backend(self):
        return self.__connect_backend

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.__ready
