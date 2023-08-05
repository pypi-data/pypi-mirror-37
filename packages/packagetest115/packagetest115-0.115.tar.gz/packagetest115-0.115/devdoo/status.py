#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO:: Refatorar completamente a classe Status
# TODO:: Implementar multi-idiomas classe Status
# TODO:: Remover de dentro da classe Status todas as mensagens
class Status:
    def __init__(self):
        self.__has_error = False
        self.__has_info = False
        self.__has_log = False
        self.__has_warn = False

        self.__list_errors = []

        self.show_messages = {
            "MONGO_CLIENT": {
                "message": "CRIADO::-->Banco de dados MongoDB"
            },
            "SERVICE_ID": {
                "message": "SERVICE-ID::{0}"
            },
            "REGISTER_SERVICE": {
                "message": "REGISTER-SERVICE-ID::{0}"
            },
            "BROKER_INIT": {
                "message": "INIT-BROKER::{0}"
            },
            "SERVICE_INIT": {
                "message": "INIT-SERVICE::{0}"
            },
            "DEVDOO_SERVICE_INIT": {
                "message": "DEVDOO-SERVICE-INIT::{0}, {1}, {2}"
            },
            "DEVDOO_BROKER_INIT": {
                "message": "INIT-DEVDOO-BROKER::{0}"
            },
            "CONFIG_INIT": {
                "message": "INIT-CONFIG::{0}"
            }
        }

        self.error_messages = {
            "TYPE_INVALID_ARRAY": {
                "code": 4505845,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor do tipo array [\"a\", \"b\", 1, 2]",
                "message_except": "ERRO ARRAY no campo {0}, {1}"
            },
            "TYPE_INVALID_BOOLEAN": {
                "code": 5454575,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor entre true | false | 0 | 1",
                "message_except": "ERRO BOOLEAN no campo {0}, {1}"
            },
            "TYPE_INVALID_DATE": {
                "code": 5454587,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize os formatos de data AAAA-MM-DD ou AAAA-MM-DDTHH:MM:SS.mmm",
                "message_except": "ERRO DATE no campo {0}, {1}"
            },
            "TYPE_INVALID_DECIMAL": {
                "code": 8545255,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor entre -x ate x.",
                "message_except": "ERRO DECIMAL no campo {0}, {1}"
            },
            "TYPE_INVALID_ENUM": {
                "code": 4505845,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize uma das opcões de valor : {2}",
                "message_except": "ERRO ENUM no campo {0}, {1}"
            },
            "TYPE_INVALID_NUMBER": {
                "code": 8545255,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor entre -9223372036854775808 ate 9223372036854775807.",
                "message_except": "ERRO NUMBER no campo {0}, {1}"
            },
            "TYPE_INVALID_OBJECT": {
                "code": 545465454,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor do tipo object json.",
                "message_except": "ERRO OBJECT no campo {0}, {1}"
            },
            "TYPE_INVALID_OBJECT_ID": {
                "code": 6565482,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor do tipo object_id, exemplo: '5abcd65b8356694714f893e9'.",
                "message_except": "ERRO OBJECT_ID no campo {0}, {1}"
            },
            "TYPE_INVALID_TIMESTAMP": {
                "code": 32456454,
                "message": "O valor do campo '{0}' nao pode ser '{1}', vazio ou null, utilize um valor do tipo timestamp, exemplo: '1522343386'.",
                "message_except": "ERRO TIMESTAMP no campo {0}, {1}"
            },
            "DOES_NOT_EXIST_FIELD": {
                "code": 34563456,
                "message": "O campo '{0}' nao existe no microservico.",
                "message_except": "ERRO FIELD campo {0}, {1}"
            },
            "DOES_NOT_EXIST_FIELD_TYPE": {
                "code": 5454542,
                "message": "No campo '{0}' o tipo configurado '{1}', nao existe.",
                "message_except": "ERRO FIELD no campo {0}, {1}"
            },
            "MAX_LENGTH": {
                "code": 65734747,
                "message": "No campo '{0}' O tamanho maximo permitido e '{1}', foi recebido '{2}.",
                "message_except": "ERRO MAX_LENGTH no campo {0}, {1}"
            },
            "MIN_LENGTH": {
                "code": 4567567,
                "message": "No campo '{0}' O tamanho minimo permitido e '{1}', foi recebido '{2}.",
                "message_except": "ERRO MIN_LENGTH no campo {0}, {1}"
            },
            "MIN_VALUE": {
                "code": 4564568,
                "message": "No campo '{0}' O valor minimo permitido e '{1}', foi recebido '{2}.",
                "message_except": "ERRO MIN_VALUE no campo {0}, {1}"
            },
            "MAX_VALUE": {
                "code": 7685685,
                "message": "No campo '{0}' O valor maximo permitido e '{1}', foi recebido '{2}.",
                "message_except": "ERRO MAX_VALUE no campo {0}, {1}"
            },
            "FIELD_REQUIRED": {
                "code": 8484545,
                "message": "O campo '{0}' e requerido.",
                "message_except": "ERRO FIELD_REQUIRED no campo {0}, {1}"
            },
            "FALHA_DE_SERVICE": {
                "code": 6545454,
                "message": "Identificador do servico nao valido:: '{0}' != '{1}' :: '{2}' != '{3}'.",
                "message_except": "ERRO FALHA DE SERVICE {0}, {1}"
            },
            "MAX_LIMIT_EXCEEDED": {
                "code": 85545454,
                "message": "O limite maximo ({0}) foi excedido. Limite solicitado ({1}).",
                "message_except": "ERRO MAX LIMIT EXCEEDED {0}, {1}"
            },
            "INVALID_ENDPOINT": {
                "code": 564564654,
                "message": "Endpoint nao registrado '{0}' no microservico '{1}' para o metodo '{2}'.",
                "message_except": "ERRO INVALID_ENDPOINT {0}, {1}"
            },
            "INVALID_ACTION": {
                "code": 5646546517,
                "message": "Acao '{0}' nao registrada no microservico '{1}' - '{2}' - para o metodo '{3}'.",
                "message_except": "ERRO INVALID ACTION {0}, {1}"
            },
            "INVALID_ACTION_DB": {
                "code": 654654654,
                "message": "Acao '{0}' nao disponivel para interacões base de dados.",
                "message_except": "ERRO INVALID ACTION DB {0}, {1}"
            },
            "FIELD_CONFLICT": {
                "code": 5646546517,
                "message": "O campo '{0}' nao pode ser utilizado por existir campos filhos.",
                "message_except": "ERRO FIELD CONFLICT {0}, {1}"
            },
            "NO_DATA_TO_INSERT": {
                "code": 545645645,
                "message": "Nao foi enviado dados para ser inserido na base de dados. {0}",
                "message_except": "ERRO NO DATA TO INSERT {0}, {1}"
            },
            "NO_DATA_TO_UPDATE": {
                "code": 34545645632,
                "message": "Nao foi enviado dados para ser atualizao na base de dados.",
                "message_except": "ERRO NO DATA TO UPDATE {0}, {1}"
            },
            "INVALID_SCHEME_UPDATE": {
                "code": 645456653,
                "message": "Esquema de update Invalido nao encontrado $set, $inc...",
                "message_except": "ERRO INVALID SCHEME UPDATE {0}, {1}"
            },
            "WARN_FIND_ITEM": {
                "code": 5356456445,
                "message": "O filtro da busca encontrou mais mais itens do que o esperado, nenhum item e retornado.",
                "message_except": "WARN FIND ITEM {0}, {1}"
            },
            "WARN_INSERT_ITEM": {
                "code": 5356456445,
                "message": "Muitos documentos foram inseridos utilizando um endpoit do tipo 'item', somente o primeiro documento e retornado.",
                "message_except": "WARN INSERT ITEM {0}, {1}"
            },
            "SERVICE_INVALID": {
                "code": 66565,
                "message": "Microservice parametro invalido :: {1} em {0}.",
            },
            "MICROSERVICE_INVALID": {
                "code": 36645764,
                "message": "Microservice invalido :: Service ID:: {1}.",
            },
            "CONFIGURATION_SERVICE": {
                "code": 24545454,
                "message": "{0}"
            },
            "INVALID_PACKAGE": {
                "code": 84545754,
                "message": "{0}"
            },
            "INVALID_PACKAGE_PARAMS": {
                "code": 545454545,
                "message": "{0} :: {1}"
            },
            "INVALID_SERVICE": {
                "code": 54621854,
                "message": "{0}--{1}"
            },
            "INVALID_BROKER": {
                "code": 684484,
                "message": "{0}--{1}"
            },
            "FAIL_LOAD_FILE_CONFIG": {
                "code": 855618,
                "message": "{0}--{1}"
            },
            "COLLECTION_INVALID": {
                "code": 654545,
                "message": "Nome de colecao registrada no servico invalido em '{0}'."
            },
            "COLLECTION_INVALID_IDENTIFIER": {
                "code": 65465658,
                "message": "Identificador da colecao invalido ou nao definido em '{0}'."
            },
            "INVALID_ENDPOINT_PARAMS": {
                "code": 84545454,
                "message": "Parametros de configuracao do de enpoint nao definido ou invalido: '{0}' na uri '{1}'."
            },
            "INVALID_DATABASE_CONFIG": {
                "code": 845487545,
                "message": "Configuracao do base de dados falhou: '{0}'."
            },
            "INVALID_NETWORK_CONFIG": {
                "code": 845485748,
                "message": "Configuracao de rede falhou: '{0}'."
            },
            "INVALID_CONFIG": {
                "code": 8754557,
                "message": "Nao recebeu parametro de configuracao: '{0}'."
            },
            "ERROR_BROKER_CONFIG": {
                "code": 854520854,
                "message": "ERROR_BROKER_CONFIG: '{0}', '{1}'."
            },
            "ERROR_SERVICE_CONFIG": {
                "code": 887854,
                "message": "ERROR_SERVICE_CONFIG: '{0}', '{1}'."
            },
            "ERROR_DATABASE_CONFIG": {
                "code": 4542454,
                "message": "ERROR_DATABASE_CONFIG: '{0}', '{1}'."
            },
            "RESPONSE": {
                "code": 52454245454,
                "message": "ERROR_RESPONSE: '{0}', '{1}'."
            },
            "DATA_RESPONSE": {
                "code": 85456455,
                "message": "ERROR_DATA_RESPONSE: '{0}'."
            },
            "ERROR_STACK": {
                "code": 865454952,
                "message": "ERROR_STACK: '{0}'."
            }

        }

    # --------------------------------
    # addx
    # --------------------------------
    def addx(self, code, value, params):
        error = self.error_messages[code]
        self.add(error["code"], error["message"].format(*params))

        if (value is not None) and (type(value) == dict) and ("error" in value.keys()):
            params = [(params[1]), (value["error"])]
            self.add(error["code"], error["message_except"].format(*params))

    def alerts(self, code, value, params):
        self.__has_error = True
        self.addx(code, value, params)

    def error(self, code, value, params):
        self.__has_error = True
        self.addx(code, value, params)

    def show(self, code, params=None):
        if params is not None:
            print self.show_messages[code]["message"].format(*params)
        else:
            print self.show_messages[code]["message"]

    def info(self, code, value, params):
        self.__has_info = True
        self.addx(code, value, params)

    def log(self, code, value, params):
        self.__has_log = True
        self.addx(code, value, params)

    def warn(self, code, value, params):
        self.__has_warn = True
        self.addx(code, value, params)

    # --------------------------------
    # add_errors
    # --------------------------------
    # Adiciona uma lista de erros na lista de erros retornada
    #
    def add_errors(self, list_errors):
        if list_errors is not None:
            for error in list_errors:
                self.add(error['code'], error['message'])

    def add(self, code, message):
        self.__has_error = True
        self.__list_errors.append(
            {"code": code, "message": message}
        )

    def add_required(self, code, message):
        self.__has_error = True
        self.__list_errors.append(
            {"code": code, "message": message}
        )

    def add_field_required(self, field, code, message):
        self.__has_error = True
        self.__list_errors.append(
            {"field": field, "code": code, "message": message}
        )

    def to_list(self):
        if len(self.__list_errors) > 0:
            return self.__list_errors
        return None

    def to_print(self):
        if len(self.__list_errors) > 0:
            print self.__list_errors
        return None

    def ready(self):
        return self.__has_error is not True

    def has_error(self):
        return self.__has_error
