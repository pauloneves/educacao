# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import IPython
get_ipython().run_line_magic('matplotlib', 'notebook')
#pd.options.display.max_rows = None
#pd.options.display.max_columns = None


# %%
NUM_MELHORES = 40


# %%
CO_SAO_BENTO = 33062633
CO_SAO_VICENTE = 33063648
CO_PARQUE = 33065837
CO_ELEVA = 33178860

CO_MUN_RIO = 3304557
CO_UF_RIO = 33


# %%
df_turmas = pd.read_feather('dados/turmas2018.feather')
df_escolas = pd.read_feather('dados/escolas_rio_2018.feather')


# %%
df_enem_rio = pd.read_feather('dados/enem_rio_2018.feather')

# %% [markdown]
# ## Nota final
# Abaixo pode-se personalizar o cálculo de nota final. pondero pelas notas mais importantes.
# 
# O Inep costuma considerar a redação como tendo um peso igual às outras disciplinas. 
# 
# Algumas universidades consideram um peso distinto de acordo com a disciplina
# 
# ### Pesos UFRJ
# 
# Referência dos [pesos da UFRJ](https://oglobo.globo.com/sociedade/educacao/ufrj-usara-pesos-diferentes-em-provas-do-enem-2011-para-acesso-aos-cursos-de-graduacao-2865665).
# 
# - Redação: peso 3 (mínimo 300)
# - Ciência da Computação, Ciências Atuariais, Engenharias, Estatística, Matemática e Química Industrial
#     - Matemática tem peso 4
# - Ciências Econômicas, Geologia e Meteorologia
#     - Matemática peso 3
# - Engenharias e Química Industrial
#     - Ciências da Natureza: peso 4
# - Geologia
#     - Ciências da Natureza: peso 3
# - Humanas
#     - Ciências Humanas e Linguagens: peso 2
# 
# 

# %%
notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', ]
notas_pesos =(1, 1, 1, 1, 4)


# %%
media_ponderada = lambda notas: np.average(notas, weights=notas_pesos)

df_enem_rio['nota_final'] = df_enem_rio  .loc[df_enem_rio.TP_ST_CONCLUSAO == 2, notas_cols ]  .apply(media_ponderada, axis=1).round(0)
df_enem_rio[notas_cols+ ['nota_final']].head()


# %%
notas_agg = {col: (col, 'median') for col in notas_cols}
notas_agg['mediana'] = ('nota_final', 'median')
notas_agg['num'] = ('nota_final', 'count')

df_melhores = df_enem_rio.groupby('CO_ESCOLA')       .agg(**notas_agg).sort_values('mediana', ascending=False)
df_melhores = df_melhores[df_melhores.num > 30] #corte arbitrário, só quem tem mais de 30 alunos
df_melhores.head()


# %%
df_melhores['CO_ESCOLA'] = df_melhores.index.astype('category')
df_melhores['rank'] = df_melhores.mediana.rank(ascending=False, method='min')


# %%
df_melhores = df_melhores.merge(df_escolas, left_index=True, right_on='CO_ENTIDADE').loc[:,
    ['NO_ENTIDADE',  'mediana', 'num', 'rank'] + notas_cols + ['CO_ENTIDADE']]
df_melhores


# %%

df_enem = df_melhores[['CO_ENTIDADE']].merge(df_enem_rio, 
                     left_on='CO_ENTIDADE', right_on='CO_ESCOLA')\
          .loc[:,list(notas_cols) + ['CO_ESCOLA', 'nota_final']]
df_enem.head()


# %%
my_order = df_melhores.head(NUM_MELHORES).NO_ENTIDADE

# %% [markdown]
# Ajustar no gráfico abaixo:
# 
# - diminuir nomes de escola muito grandes
# 

# %%
df_melhores['rotulo'] = df_melhores.loc[:,['NO_ENTIDADE', 'num', 'rank']].apply(lambda x: '{:>s} {:03d}/{:>2.0f}'.format(x[0].title(), x[1], x[2]), axis=1)


# %%
df_melhores


# %%


def compara_distribuicoes(nota):
    sns.set(rc={'figure.figsize':(11,18), 'axes.xmargin': .1})
    #sns.palplot(sns.hls_palette(8, l=.3, s=.8))
    
    nota_agrupada = nota
    if nota=='nota_final':
        nota_agrupada = 'mediana'
    
    df_top = df_melhores.sort_values(nota_agrupada, ascending=False).head(NUM_MELHORES)
    ax = sns.boxplot(data=df_enem, y='CO_ESCOLA', x=nota, orient='h'
                     ,order=df_top.CO_ENTIDADE)
    ax.set(ylabel='', xlabel='')
    plt.gcf().subplots_adjust(top=.95)
    plt.suptitle(f'{nota} por escola',x=0, size=24, );
    locs, _ = plt.yticks()
    plt.yticks(locs, df_top.rotulo);
    ax.set_xlim(300, 1000)
    

compara_distribuicoes('nota_final');


# %%
compara_distribuicoes('NU_NOTA_MT');


# %%
compara_distribuicoes('NU_NOTA_REDACAO');


# %%
compara_distribuicoes('NU_NOTA_CH');

# %% [markdown]
# ## Sobrevivência no ensino médio
# 
# Quantos dos alunos que começam o ensino médio fazem Enem?
# 
# Motivos para diminuir:
# - Maus alunos são expulsos
# - Maus alunos não acreditam que passarão no Enem
# - Vai para universidade fora do Enem (ITAs, PUCs, USP, exterior etc.)
# 
# Motivos para aumentar:
# - Crise econômica (escolas públicas)
# - Bolsa para bons alunos 
# 
# ### ideias
# - comparar com último ano (dá ideia melhor da seleção feita pela escola)
# - comparar com quem fez prova (ideia melhor de auto seleção)

# %%
etapa_col = 'TP_ETAPA_ENSINO'
primeiro_ano = [25,  30, 35]
# todo: tratar ensinos médios de 4 anos
df_primeiro_ano_turmas = pd.read_feather('dados/primeiro_ano.feather')

           range(2007, 2018)

# %%
df_ano_um = df_primeiro_ano_turmas.groupby(['id_escola', 'ano'])['num_matriculas'].sum()
CO_ELEVA=33178860
df_ano_um.unstack().T


# %%
with pd.option_context('display.max_columns', None):
    display(df_primeiro_ano_turmas.loc[df_primeiro_ano_turmas.CO_ENTIDADE == CO_SAO_VICENTE].head())


# %%
df_ano_um = pd.concat([df_melhores.set_index('CO_ENTIDADE')[['rotulo', 'num', 'rank']], df_ano_um['NU_MATRICULAS']], axis=1)
df_ano_um.sort_values('rank').head(40)


# %%
df_ano_um['%'] = df_ano_um.num/df_ano_um.NU_MATRICULAS


# %%
df_ordered = df_ano_um.sort_values('rank').head(NUM_MELHORES).sort_values('%')
ax = df_ordered['%'].plot.bar()
loc, _ = plt.xticks()
plt.xticks(loc, df_ordered.rotulo);


