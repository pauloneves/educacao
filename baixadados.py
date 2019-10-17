#!/bin/env python
"""
Baixando arquivos de dados do censo
"""

import os
import glob
import zipfile
from itertools import chain


def censo_urls(begin=2000, end=2018):
    for i in range(begin, end+1):
        if i <= 2003:
            u = 'http://download.inep.gov.br/microdados/micro_censo_escolar%i.zip' % i
        elif i <= 2005:
            u = 'http://download.inep.gov.br/microdados/microdados_censo_escolar_%i.zip' % i
        elif i == 2006:
            u = 'http://download.inep.gov.br/microdados/microdados_censo_escolar_2006_2.zip'
        elif i < 2018:
            u = 'http://download.inep.gov.br/microdados/micro_censo_escolar_%i.zip' % i
        else:
            u = f'http://download.inep.gov.br/microdados/microdados_educacao_basica_{i}.zip'
        yield u



def enem_urls(begin=1998, end=2018):
    for i in range(begin, end+1):
        u = f'http://download.inep.gov.br/microdados/micro_enem{i}.zip'
        if i >= 2005:
            u = f'http://download.inep.gov.br/microdados/microdados_enem{i}.zip'
        yield u

def baixa_dados():
    os.chdir('dados')
    try:
        for url in chain(censo_urls(2018), enem_urls(2018)):
            os.system('wget -c ' + url)
            filename = os.path.basename(url)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(filename.split('.')[0])
    finally:
        os.chdir('..')

def unzip_dados():
    os.chdir('dados')
    try:
        zips = set(glob.glob('*.zip') + glob.glob('*.ZIP'))
        for zip in zips:
            with zipfile.ZipFile(zip, 'r') as zip_ref:
                zip_ref.extractall(zip.split('.')[0])
    finally:
        os.chdir('..')
        



if __name__ == '__main__':
    baixa_dados()
