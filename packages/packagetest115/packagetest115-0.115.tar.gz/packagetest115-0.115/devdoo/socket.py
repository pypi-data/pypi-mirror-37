#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq

class Socket:

    def __init__(self, service):
        self.__ready = False
        self.__connect_backend = None
        self.backend = None
        self.__service = service

        if (service is not None) and service.ready():
            self.backend = service.endpoint_backend()
            # Cria contexto ZMQ
            context = zmq.Context()
            # Abre portas para os Serviços no backend
            self.__connect_backend = context.socket(zmq.DEALER)
            self.__connect_backend.bind(service.endpoint_backend())
            self.__ready = True


    def connect_backend(self):
        print "ID-->>", self.__service.id
        return self.__connect_backend

    def ready(self):
        return self.__ready
