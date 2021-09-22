#!/bin/env python
"""
Baixando arquivos de dados do censo

Pode rodar várias vezes que não baixará de novo arquivos
"""

import os
import glob
import zipfile
from itertools import chain

import const


def censo_urls(begin=2000, end=const.ANO_ULT):
    for i in range(end, begin - 1, -1):
        if i <= 2003:
            u = "http://download.inep.gov.br/microdados/micro_censo_escolar%i.zip" % i
        elif i <= 2005:
            u = (
                "http://download.inep.gov.br/microdados/microdados_censo_escolar_%i.zip"
                % i
            )
        elif i == 2006:
            u = "http://download.inep.gov.br/microdados/microdados_censo_escolar_2006_2.zip"
        elif i < 2018:
            u = "http://download.inep.gov.br/microdados/micro_censo_escolar_%i.zip" % i
        else:
            u = f"http://download.inep.gov.br/microdados/microdados_educacao_basica_{i}.zip"
        yield u


def enem_urls(begin=2011, end=const.ANO_ULT):  # 1998,
    for i in range(begin, end + 1):
        u = f"http://download.inep.gov.br/microdados/micro_enem{i}.zip"
        if i >= 2005:
            u = f"http://download.inep.gov.br/microdados/microdados_enem_{i}.zip"
            if i >= 2011:
                u = f"http://download.inep.gov.br/microdados/microdados_enem{i}.zip"
        yield u


def baixa_dados():
    os.chdir("dados")
    try:
        for url in chain(censo_urls(), enem_urls()):
            os.system("wget -c " + url)
            filename = os.path.basename(url)
            dir_destino = filename.split(".")[0]
            if not os.path.exists(dir_destino):
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall(dir_destino)
    finally:
        os.chdir("..")


def unzip_dados():
    os.chdir("dados")
    try:
        zips = set(glob.glob("*.zip") + glob.glob("*.ZIP"))
        for zip_file in zips:
            print(zip_file)
            with zipfile.ZipFile(zip_file, "r") as zfile:
                zfile.extractall(path=zip_file.split(".")[0])

    finally:
        os.chdir("..")


if __name__ == "__main__":
    baixa_dados()
