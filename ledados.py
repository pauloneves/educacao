# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os

try:
    # os.chdir(os.path.join(os.getcwd(), '..\\..\..\Users\ppppp\AppData\Local\Temp'))
    print(os.getcwd())
except:
    pass
#%%
from IPython import get_ipython

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# get_ipython().run_line_magic('matplotlib', 'inline')

CO_MUN = 3304557  # Rio de Janeiro


#%%
df_enem_rio = pd.concat(
    df_enem.loc[df_enem.CO_MUNICIPIO_ESC == CO_MUN]
    for df_enem in pd.read_csv(
        "dados\microdados_enem2018\DADOS\MICRODADOS_ENEM_2018.csv",
        chunksize=10000,
        sep=";",
        encoding="iso8859-1",
    )
)
df_enem_rio.dropna(subset=["CO_ESCOLA"], inplace=True)
df_enem_rio["CO_ESCOLA"] = df_enem_rio.CO_ESCOLA.astype(int)
df_enem_rio.head()


#%%
df_enem_rio.shape


#%%
df_g = (
    df_enem_rio.loc[:, ["CO_ESCOLA", "NU_NOTA_REDACAO"]]
    .groupby("CO_ESCOLA")
    .agg(mediana=("NU_NOTA_REDACAO", "median"), num=("NU_NOTA_REDACAO", "size"))
    .sort_values("mediana", ascending=False)
)
df_g.head()


#%%
CO_SAO_BENTO = 33062633
# df_enem_rio[df_enem_rio.CO_ESCOLA == CO_SAO_BENTO]
plt.hist(
    df_enem_rio.loc[df_enem_rio.CO_ESCOLA == CO_SAO_BENTO, "NU_NOTA_REDACAO"], bins="fd"
)


#%%
with pd.option_context("display.max_rows", None):
    print(df_enem_rio.loc[df_enem_rio.CO_ESCOLA == CO_SAO_BENTO, "NU_NOTA_REDACAO"])

    print(
        df_enem_rio.loc[df_enem_rio.CO_ESCOLA == CO_SAO_BENTO, "NU_NOTA_REDACAO"].size
    )


#%%
df_melhores = df_g.loc[df_g.num >= 30]
df_melhores


#%%
df_escolas = pd.read_csv(
    "dados\microdados_educacao_basica_2018\microdados_ed_basica_2018\DADOS\ESCOLAS.zip",
    sep="|",
    encoding="latin1",
    low_memory=False,
    index_col="CO_ENTIDADE",
)
df_escolas.head()


#%%

df_melhores.join(df_escolas).loc[
    :, ["mediana", "num", "NO_ENTIDADE"]
].reset_index().head(50)


#%%
# get_ipython().run_line_magic('matplotlib', 'inline')
df_melhores.join(df_escolas).plot.bar(y="mediana")

#%% [markdown]
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# df_escolas.loc[(df_escolas.NO_ENTIDADE.str.contains('SAO VICENTE DE PAUL')) & (df_escolas.CO_UF == 33) & (df_escolas.CO_MUNICIPIO == 3304557)]

#%%
df_escolas[df_escolas.NO_ENTIDADE.str.contains("ELEVA")]
# por que a Eleva não aparece? Checar turmas no censo


#%%
CO_ELEVA = 33178860


#%%
CO_SAO_VICENTE = 3063648
df_sv = df_enem_rio.loc[df_enem_rio.CO_ESCOLA == CO_SAO_VICENTE]
notas = list(filter(lambda x: "NOTA" in x, df_sv.columns.to_list()))
df_sv[notas].mean()


#%%
df_eleva = df_enem_rio.loc[df_enem_rio.CO_ESCOLA == 33178860]
notas = list(filter(lambda x: "NOTA" in x, df_eleva.columns.to_list()))
df_eleva[notas].mean()


#%%
df_melhores.shape


#%%
df_turmas = pd.concat(
    df_t[df_t.CO_MUNICIPIO == CO_MUN]
    for df_t in pd.read_csv(
        "dados\microdados_educacao_basica_2018\microdados_ed_basica_2018\DADOS\TURMAS.zip",
        sep="|",
        encoding="latin1",
        chunksize=1000,
    )
)
df_turmas.head()


#%%
df_turmas.columns.tolist()


#%%
df_turmas[df_turmas.CO_ENTIDADE == CO_ELEVA].sort_values(by="NO_TURMA")


#%%

df_melhores.reset_index().to_feather("dados/melhores.feather")
df_turmas.reset_index().to_feather("dados/turmas2018.feather")
df_enem_rio.reset_index().to_feather("dados/enem_rio_2018.feather")
df_escolas.reset_index().to_feather("dados/escolas_rio_2018.feather")

