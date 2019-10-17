#!/bin/env python
"""
Baixando arquivos de dados do censo
"""

import os
#for i in xrange(2000, 2016):
#for i in xrange(2013, 2017):
for i in range(2017, 2019):
    if i <= 2003:
        m = 'http://download.inep.gov.br/microdados/micro_censo_escolar%i.zip' % i
    elif i <= 2005:
        m = 'http://download.inep.gov.br/microdados/microdados_censo_escolar_%i.zip' % i
    elif i == 2006:
        m = 'http://download.inep.gov.br/microdados/microdados_censo_escolar_2006_2.zip'
    elif i < 2018:
        m = 'http://download.inep.gov.br/microdados/micro_censo_escolar_%i.zip' % i
    else:
        m = f'http://download.inep.gov.br/microdados/microdados_educacao_basica_{i}.zip'

    os.system('wget -c ' + m)


#for i in range(1998, 2019):
for i in range(2005, 2019):
    m = f'http://download.inep.gov.br/microdados/micro_enem{i}.zip'
    if i >= 2005:
        m = f'http://download.inep.gov.br/microdados/microdados_enem{i}.zip'
    os.system('wget -c ' + m)