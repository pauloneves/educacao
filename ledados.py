# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..\\..\Users\paulo\AppData\Local\Temp'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

CO_MUN = 3304557 # Rio de Janeiro


#%%
df_enem = pd.read_csv('dados\microdados_enem2018\DADOS\MICRODADOS_ENEM_2018.csv', sep=';', encoding='iso8859-1')


#%%
df_enem.CO_MUNICIPIO_ESC


#%%
df_rio = pd.concat(df_enem.loc[df_enem.CO_MUNICIPIO_ESC== CO_MUN] for df_enem in
                   pd.read_csv('dados\microdados_enem2018\DADOS\MICRODADOS_ENEM_2018.csv',
                                chunksize=10000,
                                sep=';', encoding='iso8859-1'))


#%%
df_rio.shape


#%%
df_rio.head()


#%%
df_rio.columns.tolist()


#%%
df_rio.shape


#%%
df_g = df_rio.loc[:, [ 'CO_ESCOLA','NU_NOTA_REDACAO']].groupby('CO_ESCOLA').agg(media=('NU_NOTA_REDACAO','mean'), num=('NU_NOTA_REDACAO','count')).sort_values('media', ascending=False)
df_g.head()


#%%
df_melhores = df_g.loc[df_g.num>30]
df_melhores


#%%
df_escolas = pd.read_csv('dados\microdados_educacao_basica_2018\microdados_ed_basica_2018\DADOS\ESCOLAS.zip', sep='|', encoding='latin1', low_memory=False, index_col='CO_ENTIDADE')
df_escolas.head()


#%%

df_melhores.join(df_escolas).loc[:, ['media', 'num', 'NO_ENTIDADE']].reset_index()


#%%
get_ipython().run_line_magic('matplotlib', 'inline')
df_melhores.join(df_escolas).plot.bar(y='media')


#%%
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df_escolas.loc[(df_escolas.NO_ENTIDADE.str.contains('SAO VICENTE DE PAUL')) & (df_escolas.CO_UF == 33) & (df_escolas.CO_MUNICIPIO == 3304557)]


#%%
df_escolas.NO_ENTIDADE.str.contains('ELEVA')

#%% [markdown]
# SÃ£o Vicente Ã© cÃ³digo 33063648

#%%
df_sv = df_rio.loc[df_rio.CO_ESCOLA == 33063648]
notas = list(filter(lambda x: 'NOTA' in x, df_sv.columns.to_list() ))
df_sv[notas].mean()


#%%
df_melhores.shape


#%%
df_turmas = pd.read_csv('dados/Microdados_Censo_Escolar_2017/DADOS/TURMAS.CSV', sep='|', encoding='latin1')


#%%
df_turmas.head()


#%%
df_turmas.columns.tolist()

