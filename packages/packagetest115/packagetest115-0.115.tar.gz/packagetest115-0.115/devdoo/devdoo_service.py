#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from actions import Actions
from service import Service
from status import Status
from yml import Yml

# --------------------------------
# DevdooService
# --------------------------------
'''
A classe DevdooService prepara todas as configurações database dos serviços API
'''


# TODO:: Enviar para o servidor console a informação de falha de configuração
class DevdooService(object):
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
        super(DevdooService, self).__init__()

        # Variaveis default
        self.actions = None
        self.id = None
        self.service = None
        self.zmq_socket_database = None
        self.zmq_socket_rest = None

        # Variaveis inicializadas
        self.status = Status()

        # Verifica se o arquivo de configuração foi inicalizado corretamente
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
        self.id = yml.id()

        # Verifica se existe um identificador do servico
        if self.status.ready() and self.id:
            self.service = Service(self.id, self.status, True)

        return self.status.ready() and self.service.ready()

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

        # Adaptador de conexão worker
        self.zmq_socket_database = context.socket(zmq.REQ)
        self.zmq_socket_database.connect(self.service.database_connect_frontend())


        # Adaptador de conexão broker
        self.zmq_socket_rest = context.socket(zmq.REP)
        self.zmq_socket_rest.connect(self.service.broker_connect_backend())

        print "AAA", self.service.database_connect_frontend()
        print "BBB", self.service.broker_connect_backend()

        self.run()

    # --------------------------------
    # operation
    # --------------------------------
    '''
    Executa a ação do Serviço
    
    :return: void
    '''

    def operation(self):
        # Recebe do mensagem do servidor cliente
        message = self.zmq_socket_rest.recv_multipart()
        print "RECV <<<-->>>", message

        # Inicia o Serviço
        self.actions = Actions(message, self.service)

        # Verifica se o servico está pronto
        if self.actions.ready():

            # Envia mensagem para o servidor de base de dados
            self.zmq_socket_database.send_multipart([self.actions.send_database()])
            print "SOCKET VALIDO ENVIOU ADIANTE", "----->>>>", self.actions.send_database()

            # Recebe mensagem do servidor de base de dados
            # Envia mensagem de retorno para o cliente
            print "XXXX--->", self.service.broker_connect_backend()
            rec_msg = self.zmq_socket_database.recv()
            print "RECV", rec_msg
            self.zmq_socket_rest.send(rec_msg)
            print "SOCKET VALIDO VOLTOU", "<<<<------"

        # Em caso de falha
        else:
            # Nao processa a operação e envia mensagem de retorno para o cliente
            self.zmq_socket_rest.send(self.actions.send_error())
            print "SOCKET FALHOU E VOLTOU", "<<<<------"

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
            except DevdooService.Error:
                pass
                # except Exception as inst:
                #    print "API::RUN::ERROR", inst.args
