# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

CO_MUN = 3304557 # Rio de Janeiro
CO_UF_RIO = 33 # RJ

MIN_ALUNOS = 30 # Mínimo de alunos fazendo Enem para considerar na análise
NUM_MELHORES = 60

# %% [markdown]
# ## Lendo dados do Enem do Rio de Janeiro

# %%
df_enem_rio = pd.concat(df_enem.loc[df_enem.CO_UF_ESC== CO_UF_RIO] for df_enem in 
                        pd.read_csv('dados\microdados_enem2018\DADOS\MICRODADOS_ENEM_2018.csv', 
                                chunksize=10000, 
                                sep=';', encoding='iso8859-1'))
df_enem_rio.dropna(subset=['CO_ESCOLA'], inplace=True)
df_enem_rio['CO_ESCOLA'] = df_enem_rio.CO_ESCOLA.astype(int)
df_enem_rio.head()


# %%
df_enem_rio.shape

# %% [markdown]
# ## Lendo censo de escolas

# %%
df_escolas = pd.read_csv('dados\microdados_educacao_basica_2018\microdados_ed_basica_2018\DADOS\ESCOLAS.zip', sep='|', encoding='latin1', low_memory=False, index_col='CO_ENTIDADE')
df_escolas.head()


# %%
CO_SAO_VICENTE = 33063648
df_sv = df_enem_rio.loc[df_enem_rio.CO_ESCOLA == CO_SAO_VICENTE]
notas = list(filter(lambda x: 'NOTA' in x, df_sv.columns.to_list() ))
df_sv[notas].mean()

# %% [markdown]
# ## Lê dados históricos de turmas 

# %%
primeiro_ano = [25,  30, 35]


# %%
import glob
import patoolib
import os.path

def dados_turma(ano, try_rar=True):
    dir_censo = [i for i in glob.glob(f'dados/*{ano}*') if ('censo' in i or 'educacao_basica' in i) and 'zip' not in i]
    assert len(dir_censo) == 1, f'Só pode ter achado um arquivo e achou {len(dir_censo)}'

    arquivo_turmas = glob.glob(f'{dir_censo[0]}/*{ano}*/DADOS/TURMAS.*')
    if not arquivo_turmas:
        arquivo_turmas = glob.glob(f'{dir_censo[0]}/DADOS/TURMAS.*')
    
    result = [i for i in arquivo_turmas if i.lower().endswith('.csv')]
    if not result:
        result = [i for i in arquivo_turmas if i.lower().endswith('.zip')]
        if try_rar and not result:
            rar = [i for i in arquivo_turmas if i.lower().endswith('.rar')]
            if rar:
                patoolib.extract_archive(rar[0], outdir=os.path.dirname(rar[0]))
                result = dados_turma(ano, False)
                
    if result:
        result = result[0]
    else:
        result = None
    return result

for i in range(2007, 2019):
    print(">", dados_turma(i))
#estrutura diretórios bagunçados anets de 2007


# %%
col_turmas = pd.DataFrame({
    'id_etapa':       ['category', 'TP_ETAPA_ENSINO', 'TP_ETAPA_ENSINO', 'FK_COD_ETAPA_ENSINO'],
    'id_escola':      ['category', 'CO_ENTIDADE',     'CO_ENTIDADE',     'PK_COD_ENTIDADE'],
    'num_matriculas': ['uint8',    'NU_MATRICULAS',   'QT_MATRICULAS',   'NUM_MATRICULAS'], 
    'id_municipio':   ['category', 'CO_MUNICIPIO',    'CO_MUNICIPIO',    'FK_COD_MUNICIPIO'],
    'id_uf':          ['category', 'CO_UF',           'CO_UF',           'FK_COD_ESTADO'],
    }, index=['dtype', '2015', '2018', '2007'])
def colunas_turmas(columns):
    columns = set(columns)
    match = col_turmas.applymap(columns.__contains__).all(axis=1)
    assert match.sum()==1, f"Um e somente um registro de nomes de colunas deveria "                            "casar com todas as colunas dos dados lidos de disco {str(columns)}"
    colunas_map = col_turmas[match].iloc[0].to_dict()
    return colunas_map


# %%
def mapa_de_colunas(ano):
    df_teste = pd.read_csv(
            dados_turma(ano),
            sep="|",
            encoding="latin1",
            nrows=1
        )
    map_colunas = colunas_turmas(df_teste.columns)
    
    return {v:k for k,v in map_colunas.items()}
#mapa_de_colunas(2014), mapa_de_colunas(2015)


# %%
def le_turma(ano):
    print(f"Lendo ano {ano}")
    map_colunas = mapa_de_colunas(ano)
    df_t = pd.concat((
        df_t#.rename(columns=map_colunas).query('id_etapa.isin(@primeiro_ano) and id_uf == @CO_MUN_RIO')\
            #.merge(escolas, left_on='id_escola', right_on='CO_ENTIDADE')
        for df_t in pd.read_csv(
            dados_turma(ano),
            sep="|",
            encoding="latin1",
            chunksize=1000, 
            #error_bad_lines=False,
            usecols=map_colunas.keys(),
            #nrows=100 #debug
        )), 
        sort=True
    )
    df_t['ano'] = ano
    return df_t
    
# df_primeiro_ano_turmas = pd.concat(
#     (le_turma(i, df_escolas.CO_ENTIDADE, primeiro_ano) for i in range(2007, 2019)), #2007 e 2008, 2009 falharam linhas diferentes
#     sort=True)
# print(df_primeiro_ano_turmas.shape)
# df_primeiro_ano_turmas.head()
def le_tudo():
    for i in range(2007, 2019):
        le_turma(i)
#le_tudo()        


# %%
def le_turmas_padronizadas(filtro):
    return pd.concat(
        [le_turma(i)\
          .rename(columns=mapa_de_colunas(i))\
          .astype(col_turmas.loc['dtype'].to_dict()) #precisa do to_dict?
          .query(filtro)
          .assign(ano=i)
         for i in 
           range(2007, 2019)
           #range(2014, 2016) 
        ], sort=True
    )
                         
df_primeiro_ano_turmas = le_turmas_padronizadas('id_etapa.isin(@primeiro_ano) and id_uf == @CO_UF_RIO')
print(df_primeiro_ano_turmas.shape)
df_primeiro_ano_turmas.head()

# %% [markdown]
# ## Grava tudo em formato binário em disco

# %%

#df_turmas.reset_index().to_feather('dados/turmas2018.feather')
df_enem_rio.reset_index().to_feather('dados/enem_rio_2018.feather')
df_escolas.reset_index().to_feather('dados/escolas_rio_2018.feather')
df_primeiro_ano_turmas.reset_index().to_feather('dados/primeiro_ano.feather')


