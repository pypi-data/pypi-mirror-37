#!/usr/bin/env python
# -*- coding: utf-8 -*-
from connection import Connection
from check import Check
from convert import Convert
from endpoint import Endpoint
from pprint import pprint
from brokers import Brokers


class Database:
    def __init__(self, database_id, status, service_port=None):
        self.status = status
        self.connection = Connection(self.status)

        self.__endpoints = dict()

        self.collections = None

        # Identificador do broker
        self.id = database_id
        # Configurações da Rede utilizada pelo broker
        self.network = None
        # Listas de serviços que o broker conecta
        self.databases = None
        self.actions = None

        self.__config(service_port)

    def __setitem__(self, field, value):
        self.field = value

    def endpoint(self, method, source, status):
        return Endpoint(source, self.actions[method][source], status)

    # --------------------------------
    # endpoint
    # --------------------------------
    #def endpoint(self, source):
    #    if source in self.__endpoints.keys():
    #        return self.__endpoints[source]
    #    else:
    #        return None


    # --------------------------------
    # show
    # --------------------------------
    def ready(self):
        return self.status.ready()

    # --------------------------------
    # show
    # --------------------------------
    # Imprime propriedade/valor do objeto
    def show(self, message=None):
        if message:
            print message, ":::------->>>"
        pprint(self.__dict__)

    # --------------------------------
    # __config
    # --------------------------------
    # Implementa auto configuração do broker
    # Vai até o servidor de configuração buscar informações de configuração para o broker
    def __config(self, service_port):
        if self.id:
            data_response = self.connection.load_config(self.id)

            if data_response.ready():
                data = data_response.values()

                for field in data:
                    self.__dict__[field] = data[field]
                self.__output()
                self.__prepare_scheme()
            else:
                self.status.error("ERROR_DATABASE_CONFIG", None,
                                  ["AA-Nao obteve dados de configuracao do database", self.id])
        else:
            self.status.error("ERROR_DATABASE_CONFIG", None, ["BB-Nao recebeu identificador de database", "--"])

        if not self.status.ready():
            self.status.to_print()

    def __brokers(self, service_port):
        if self.brokers:
            self.brokers = Brokers(service_port, self.brokers, self.status, False, True)
        else:
            self.status.error("ERROR_DATABASE_CONFIG", None,
                              ["GG-Nao obteve dados de configuracao de brokers do database", self.id])

    def __output(self):
        if self.network:
            self.__brokers(self.network["port"])
        else:
            self.status.error("ERROR_DATABASE_CONFIG", None,
                              ["DD-Nao obteve dados de configuracao do network no database", self.id])


    # --------------------------------
    # fields_insert
    # --------------------------------
    # Prepara a lista de campos que pode ser incluída na base de dados
    #
    def fields_insert(self, body, endpoint):
        list_scheme_clean = dict()
        # Verifica se o campo tem valor default
        for item_name in endpoint.scheme:
            # Pega um esquema da lista
            item_scheme = endpoint.scheme[item_name]
            # Verifica se o campo tem valor default ou é requerido
            if Check.is_default(item_scheme) or self.__required(item_scheme):
                # Registra o dot field name do campo
                item_scheme["field"] = item_name
                # Verifica se o valor do campo não é vazio
                # Registra o valor do campo
                item_scheme["value"] = Convert.to_empty(item_scheme, self.__default(item_scheme))
                # Registra o schema válido na lista de esquema limpa
                list_scheme_clean[item_name] = item_scheme

        # Processa todos os campos de body para colocar em letra minuscula e criar lista de campos validos
        for item_body_field in body:
            # Processa o nome do campo recebido no body
            body_field = item_body_field.replace(' ', '_').lower().strip()

            # Verifica se o campo recebido via body esta configurado no esquema
            item_name, item_scheme = self.__check_body_item_scheme(body_field, endpoint.scheme)

            # Caso o campo recebido via body está registrado no esquema então adiciona na lista de esquema limpa
            if item_scheme is not None:
                # Registra o dot field name do campo
                item_scheme["field"] = item_name
                # Verifica se o valor do campo não é vazio
                # Registra o valor do campo
                item_scheme["value"] = Convert.to_empty(item_scheme, body[item_body_field])
                # Registra o schema válido na lista de esquema limpa
                list_scheme_clean[item_name] = item_scheme

            # Verifica se o campo é válido
            endpoint.is_field_valid(item_body_field, self.status)



        return list_scheme_clean

    # --------------------------------
    # fields_update
    # --------------------------------
    def fields_update(self, body, scheme, fields_default):

        list_scheme_clean = dict()

        # Processa todos os campos de body para colocar em letra minuscula e criar lista de campos validos
        for item_body_field in body:
            body_field = item_body_field.replace(' ', '_').lower().strip()
            item_name, item_scheme = self.__check_body_item_scheme(body_field, scheme)

            if item_scheme is not None:
                item_scheme["field"] = item_name
                item_scheme["value"] = Convert.to_empty(item_scheme, body[item_body_field])
                list_scheme_clean[item_name] = item_scheme

            # Caso o campo nao esteja registrado no scheme, registra mensagem de error
            if item_body_field not in fields_default:
                self.status.error("DOES_NOT_EXIST_FIELD", None, [item_body_field])

        return list_scheme_clean

    # --------------------------------
    # __check_body_item_scheme
    # --------------------------------
    # Verifica se o campo recebido via body esta configurado no esquema
    @staticmethod
    def __check_body_item_scheme(body_field, scheme):
        for item_scheme in scheme:
            if item_scheme == body_field:
                return body_field, scheme[item_scheme]
        return None, None

    # --------------------------------
    # __default
    # --------------------------------
    @staticmethod
    def __default(item_scheme):
        value = ""
        if 'default' in item_scheme.keys():
            value = item_scheme['default']
        return value

    # --------------------------------
    # __required
    # --------------------------------
    @staticmethod
    def __required(item_scheme):
        value = False
        if 'required' in item_scheme.keys():
            value = item_scheme['required']
        return value


    # --------------------------------
    # __collection
    # --------------------------------
    def __collection(self, uri, item, collections):
        collection = None
        name = None
        if "collection" in item.keys():
            name = item["collection"]
            if name in collections.keys():
                collection = collections[name]["schemes"]
            else:
                self.status.error("COLLECTION_INVALID", None, [name])
        else:
            self.status.error("COLLECTION_INVALID_IDENTIFIER", None, [uri])

        return name, collection

    # --------------------------------
    # __fields_public
    # --------------------------------
    @staticmethod
    def __fields_public(method, item, schemes):
        for i in schemes:
            if "public" in schemes[i].keys():
                if method != "put":
                    item["scheme"][i] = schemes[i]
                if schemes[i]["public"] is True:
                    (item["fields"]["public"]).append(schemes[i]["field"])

        return item

    # --------------------------------
    # __put_scheme
    # --------------------------------
    def __put_scheme(self, put, schemes):
        for item in put:
            index = 0
            for field in put[item]:
                put[item][index] = schemes[(put[item][index])]
                index = index + 1
        return put


    # --------------------------------
    # __prepare_scheme
    # --------------------------------
    def __prepare_scheme(self):
        collections = self.collections
        actions = self.actions

        for method in actions:
            endpoint = actions[method]
            for item in endpoint:
                name, schemes = self.__collection(item, endpoint[item], collections)
                if schemes is not None:
                    if self.__check_endpoint(item, endpoint[item]):
                        endpoint[item] = self.__fields_public(method, endpoint[item], schemes)
                        endpoint[item]["fields"]["default"] = self.__check_conflit_fields(endpoint[item]["fields"]["default"])
                        endpoint[item]["fields"]["public"] = self.__check_conflit_fields(endpoint[item]["fields"]["public"])
                        if method == "put":
                            endpoint[item]["scheme"] = self.__put_scheme(endpoint[item]["scheme"], schemes)

                        self.__endpoints[item] = Endpoint(item, endpoint[item], self.status)


                        #if method == "put":
                        #    pprint(endpoint[item])


    # --------------------------------
    # __check_endpoint
    # --------------------------------
    def __check_endpoint(self, uri, endpoint):
        errors = []
        if "action" not in endpoint.keys():
            errors.append("ACTION")

        if "collection" not in endpoint.keys():
            errors.append("COLLECTION")

        if "fields" not in endpoint.keys():
            errors.append("FIELDS")

        if "scheme" not in endpoint.keys():
            errors.append("SCHEME")

        if "type" not in endpoint.keys():
            errors.append("TYPE")

        if "max_limit" not in endpoint.keys():
            errors.append("MAX_LIMIT")

        if len(errors) > 0:
            self.status.error("INVALID_ENDPOINT_PARAMS", None, [(",".join(errors)), uri])
            return False
        else:
            return True

    # --------------------------------
    # __check_conflit_fields
    # --------------------------------
    # Verifica se existe conflito de nomes de campos em modo desenvolvimento de microserviços
    # Não permite incluir na lista campos pai que possuem campos filhos que podem sobrepor informações
    def __check_conflit_fields(self, fields_default):
        fields_clean = []
        fields_errors = dict()

        # Processa a lista de campos default
        for item_check in fields_default:
            # Retira um item da lista para comparar com outros itens da mesma lista
            for item_field in fields_default:
                # Caso um campo esteja em conflito com outros campos é adicionado na lista de erros
                if item_check + '.' in item_field:
                    fields_errors[item_check] = True

        # Gera a lista de campos default sem os campos que foram encontrados conflitos
        for item_field in fields_default:
            if item_field not in fields_errors.keys():
                fields_clean.append(item_field)

        if len(fields_errors) > 0:
            self.status.error("FIELD_CONFLICT", None, [(",".join(fields_errors))])

        return fields_clean
