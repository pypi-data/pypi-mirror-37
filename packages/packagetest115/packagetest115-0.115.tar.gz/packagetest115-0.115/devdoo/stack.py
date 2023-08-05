#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import uuid
from pack import Pack
from status import Status


class Stack:
    """Um pedido que entrou no sistema."""

    def __init__(self, message, timeout, tries):
        """Cria um novo pedido com um número máximo de tentativas.
         Depois disso, o pedido será considerado uma falha."""

        self.deadline = None
        self.status = Status()
        self.timeout = timeout
        self.tries = tries
        self.msg = message

        # Separa o path e o conteúdo do pedido
        self.extract_path(message)

    def extract_path(self, request):
        """Separa informações de roteamento e dados de um pedido recebido."""
        self.__pack(request)
        # Verifica se o pacote de configurações é válido
        if self.pack.ready():
            self.id = self.pack.id
            self.service_id = self.pack.service_id
            self.path = [str(self.id), '']

            print "STACK.ID=============================>>>>>", self.id
            print "self.path=============================>>>>>", self.path
            #print "self.content=============================>>>>>", self.content

    def update_deadline(self):
        """Atualize o prazo de solicitação se um tempo limite tiver sido especificado."""
        if self.timeout is not None:
            self.deadline = time.time() + self.timeout
        if self.tries is not None:
            self.tries -= 1

    def make_request(self):
        """Devolve um pedido por sua identificação exclusiva para ser enviada a um worker.
         Isso também atualiza o prazo de solicitação."""
        self.update_deadline()

        # self.path[0] = self.id
        self.message = self.path + self.content

    def expired(self):
        """Se verdadeiro o número máximo de tentativas foi realizado."""
        return self.tries == 0

    def timed_out(self):
        """Se verdadeiro passamos o prazo de execução do pedido."""
        return self.deadline is not None and time.time() > self.deadline

    # --------------------------------
    # __find_service
    # --------------------------------
    def __pack(self, request):
        if type(request) == list and len(request) == 3:
            self.content = request[2:]
            if type(self.content)==list and len(self.content)==1:
                # Prepara configurações recebidas do rest
                self.pack = Pack(self.content[0], self.status)
            else:
                self.status.error("ERROR_STACK", None, ["__pack de dados vindo do broker nao recebeu conteudo valido"])
        else:
            self.status.error("ERROR_STACK", None, ["__pack de dados vindo do broker nao e valido"])

    # --------------------------------
    # ready
    # --------------------------------
    def ready(self):
        return self.status.ready() and self.pack.ready()

    # --------------------------------
    # send_error
    # --------------------------------
    def send_error(self):
        return self.path + self.pack.send_error()
