#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import sys
import os
from check import Check


class Yml:
    # --------------------------------
    # __init__
    # --------------------------------
    def __init__(self, status):
        self.status = status
        pass

    # --------------------------------
    # service_id
    # --------------------------------
    # Obtém o identificador do serviço
    def id(self):

        # Tenta pegar configurações docker
        id = os.environ.get('devdoo')

        # Caso não consiga pegar o id do serviço no docker
        if not id:
            # Tenta pegar configurações de arquivo local
            id = self.__config()
        else:
            self.status.error("CONFIGURATION_SERVICE", None,
                              ["Não recebeu identificador de arquivo de configuracao (service id)"])
        return id

    # --------------------------------
    # __config
    # --------------------------------
    # Recupera informações de configuração em arquivo yml local
    def __config(self):
        file_open = None

        if len(sys.argv) > 1:
            # Recupera o endereço do arquivo de configuração
            path_file = str(sys.argv[1])
            # Verifica se o endereço do arquivo é válido
            if (type(path_file) == str) and (".yml" in path_file):
                try:
                    # Abre o arquivo
                    file_yml = open(path_file, "r")
                    # Converte o arquivo em objeto
                    file_open = yaml.load(file_yml)
                except Exception:
                    self.status.error("CONFIGURATION_SERVICE", None, ["Arquivo de configuracao YML nao encontrado"])
                    pass
            else:
                self.status.error("CONFIGURATION_SERVICE", None,
                                  ["Identificador do servico NAO fornecido na inicializacao"])

            # Verifica se o arquivo é válido e se existe configurações de serviços nele
            if (file_open is not None) and ("services" in file_open.keys()):
                # Processa o arquivo
                for item in file_open["services"]:
                    services = file_open["services"][item]
                    if "environment" in services:
                        environment = services["environment"]
                        if "devdoo" in environment:
                            # Recupera as configurações devdoo
                            value = environment["devdoo"]
                            # Verifica se recebeu configuração de devdoo válida
                            if (Check.is_string(value) is True) and (Check.is_empty(value) is False):
                                return value
                            else:
                                self.status.error("CONFIGURATION_SERVICE", None,
                                                  ["Arquivo de configuracao nao e um 'devdoo' valido"])
                        else:
                            self.status.error("CONFIGURATION_SERVICE", None,
                                              ["Arquivo de configuracao encontrou falhas no grupo 'devdoo'"])
                    else:
                        self.status.error("CONFIGURATION_SERVICE", None,
                                          ["Arquivo de configuracao encontrou falhas no grupo 'environment'"])
            else:
                self.status.error("CONFIGURATION_SERVICE", None,
                                  ["Arquivo de configuracao não possui o grupo 'services'"])
        else:
            self.status.error("CONFIGURATION_SERVICE", None,
                              ["Nao foi indicado nenhum endereco de arquivo de configuracao"])
