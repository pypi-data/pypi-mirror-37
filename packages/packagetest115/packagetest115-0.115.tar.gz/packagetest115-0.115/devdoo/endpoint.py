#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from check import Check


class Endpoint:
    def __init__(self, uri, endpoint, status):
        # pprint(endpoint)
        self.__ready = False
        self.status = status
        self.uri = uri

        self.__decode(endpoint)

    # --------------------------------
    # __decode
    # --------------------------------
    def __decode(self, endpoint):
        self.action = endpoint["action"]
        self.collection = endpoint["collection"]
        self.scheme = endpoint["scheme"]
        self.type = endpoint["type"]
        self.max_limit = endpoint["max_limit"]
        self.__fields = endpoint["fields"]
        self.__check_params()

    def fields(self, is_public_access = True):
        if is_public_access is True:
            return self.__fields["public"]
        else:
            return self.__fields["default"]


    def ready(self):
        return self.__ready

    # --------------------------------
    # show
    # --------------------------------
    # Imprime propriedade/valor do objeto
    def show(self, message=None):
        if message:
            print message, ":::------->>>"
        pprint(self.__dict__)

    def is_field_valid(self, field, status):
        # Caso o campo nao esteja registrado no scheme, registra na lista de campos com erro
        if field not in self.fields(False):
            # Caso o campo nao esteja registrado no scheme, registra mensagem de error
            status.error("DOES_NOT_EXIST_FIELD", None, [field])

    # --------------------------------
    # __check_params
    # --------------------------------
    # Verifica se o pacote de comunicação é válido
    def __check_params(self):
        errors = []

        # Verifica se foi definido a ação que será executado no base de dados
        if Check.is_empty(self.action) is True:
            errors.append("ACTION")

        # Verifica se foi definido a coleção que deverá ser usada
        if Check.is_empty(self.collection) is True:
            errors.append("COLLECTION")

        # Verifica se foi definido a lista de campos da coleção
        if Check.is_object(self.__fields) is not True:
            errors.append("FIELDS")

        # Verifica se foi definido schema da coleção
        if Check.is_object(self.scheme) is not True:
            errors.append("SCHEME")

        # Verifica se foi definido o tipo de retorna de dados do base de dados (item|list)
        if Check.is_empty(self.type) is True:
            errors.append("TYPE")

        # Verifica se foi definido o limit máximo de dados retornados do base de dados
        if type(self.max_limit) is not int:
            errors.append("MAX_LIMIT")

        if len(errors) > 0:
            self.status.error("INVALID_ENDPOINT_PARAMS", None, [(",".join(errors)), self.uri])
        else:
            self.__ready = True
