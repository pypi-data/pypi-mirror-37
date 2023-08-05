#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections, time
from stack import Stack

class Stacks:
    """Atualmente executando pedidos."""

    class Error(Exception):
        """Exceção levantada quando algo deu errado."""
        pass

    def __init__(self, timeout, tries):
        """Crie um novo conjunto de solicitações vazio."""

        # Verifica se o timeout é válido
        # if timeout is not None and timeout < 0:
        #     raise Stacks.Error("o tempo limite deve ser não-negativo ou None")

        # Verifica se o número de tentativas é válido
        # if tries is not None and tries <= 0:
        #     raise Stacks.Error("as tentativas devem ser positivas ou None")

        # Cria stacks
        self.list_waiting = collections.deque()
        self.list_processing = collections.deque()

        # Lista temporária para remover requisições da fila de processamento
        self.temp_stack_requests = {}
        self.timeout = timeout
        self.tries = tries

    def add(self, message):
        """Crie um novo objeto de solicitação e faça com que ele entre no sistema."""
        self.list_waiting.append(Stack(message, self.timeout, self.tries))

    def process(self, stack):
        """Defina um novo parâmetro de solicitação antes de enviá-lo para um worker."""

        # Adiciona a requisição na lista de processamento
        self.list_processing.append(stack)

        # Registra a requisição na fila temporária
        self.temp_stack_requests[stack.id] = stack

        stack.make_request()
        return stack

    def request_waiting(self):
        """Verifique se há algum pedido aguardando um worker."""
        return len(self.list_waiting) > 0

    def get_request(self):
        """Obter o primeiro pedido na fila."""
        if self.request_waiting():
            # Remove requisição da lista de espera
            stack = self.list_waiting.popleft()
            return self.process(stack)
        raise Stacks.Error("internal error")

    def check_for_timeouts(self):
        """Verifica se algum pedido expirou. Se esse é o caso,
         coloca na fila novamente a menos que o número máximo de tentativas tenha sido
         alcançado. Retornar uma lista de pedidos expirados."""
        expired = []
        while self.list_processing and self.list_processing[0].timed_out():
            request = self.list_processing.popleft()
            del self.temp_stack_requests[request.id]
            if request.expired():
                expired.append(request)
            else:
                self.list_waiting.append(request)
        return expired

    def remove(self, result):


        """Dada uma resposta, remove a solicitação correspondente da fila.
        Retornar a resposta para enviar se o pedido foi encontrado no sistema,
        nenhum caso (resposta tardia, por exemplo)."""
        id, content = result[0], result[1:]

        print "self.temp_stack_requests", id, self.temp_stack_requests.keys()

        if id in self.temp_stack_requests:
            request = self.temp_stack_requests[id]
            self.list_processing.remove(request)
            del self.temp_stack_requests[id]

            print "STACKS REMOVE---->>>>>>ID", id, request.path

            return request.path + content

    def next_timeout_ms(self):
        """Retorna o número de milisegundos até o próximo evento de tempo limite,
           ou None se não houver nenhum."""
        if self.list_processing:
            return 1000 * max(self.list_processing[0].deadline - time.time(), 0)
