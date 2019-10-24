# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import IPython
get_ipython().run_line_magic('matplotlib', 'notebook')
pd.options.display.max_rows = None
pd.options.display.max_columns = None


#%%
df_melhores = pd.read_feather('dados/melhores.feather')
df_turmas = pd.read_feather('dados/turmas2018.feather')
df_enem_rio = pd.read_feather('dados/enem_rio_2018.feather')
df_escolas = pd.read_feather('dados/escolas_rio_2018.feather')

#%% [markdown]
# ## Nota final
# Inventando meu cálculo de nota final. pondero pelas notas mais importantes

#%%
notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', ]
notas_pesos =(1, 2, 1, 2, 3)


#%%
media_ponderada = lambda notas: np.average(notas, weights=notas_pesos)

df_enem_rio['nota_final'] = df_enem_rio  .loc[:, notas_cols ]  .apply(media_ponderada, axis=1).round(0)
df_enem_rio[notas_cols+ ['nota_final']].head()


#%%
notas_agg = {col: (col, 'median') for col in notas_cols}
notas_agg['mediana'] = ('nota_final', 'median')
notas_agg['num'] = ('nota_final', 'count')

df_melhores = df_enem_rio.groupby('CO_ESCOLA')       .agg(**notas_agg).sort_values('mediana', ascending=False)
df_melhores = df_melhores[df_melhores.num > 30] #corte arbitrário, só quem tem mais de 30 alunos
df_melhores.head()


#%%
CO_SAO_BENTO = 33062633
CO_SAO_VICENTE = 33063648
CO_PARQUE = 33065837


#%%
#df_melhores = df_melhores[:50]
#df_melhores['CO_ESCOLA'] = df_melhores.CO_ESCOLA.astype('category')


#%%
df_melhores['rank'] = df_melhores.mediana.rank(ascending=False, method='min')


#%%
df_melhores = df_melhores.merge(df_escolas, left_index=True, right_on='CO_ENTIDADE').loc[:,
    ['NO_ENTIDADE',  'mediana', 'num', 'rank'] + notas_cols + ['CO_ENTIDADE']]
df_melhores


#%%
df_enem_rio.columns[df_enem_rio.columns.str.contains('ESC')]


#%%
NUM_MELHORES = 40
df_enem = df_melhores.head(NUM_MELHORES).merge(df_enem_rio,
                                     left_on='CO_ENTIDADE', right_on='CO_ESCOLA')\
          #.loc[:,list(notas_agg.keys()) + ['CO_ESCOLA']]
df_enem.head()


#%%
my_order = df_melhores.head(NUM_MELHORES).NO_ENTIDADE
my_order.shape

#%% [markdown]
# Ajustar no gráfico abaixo:
#
# - nomes escolas -> santo agostinho barra, ph iguais, tudo maiúculo
#

#%%
df_melhores['rotulo'] = df_melhores.loc[:,['NO_ENTIDADE', 'num', 'rank']].apply(lambda x: '{:>s} {:03d}/{:>2.0f}'.format(x[0].title(), x[1], x[2]), axis=1)


#%%
import seaborn as sns
sns.set(rc={'figure.figsize':(11,18), 'axes.xmargin': .1, 'ytick.alignment': 'top'})
ax = sns.boxplot(data=df_enem, y='CO_ESCOLA', x='nota_final', orient='h',
                 order=df_melhores.head(NUM_MELHORES).CO_ENTIDADE)
ax.set(ylabel='', xlabel='')
#plt.suptitle('Distribuição de notas por escola', x=.25, va='bottom', size=24);
locs, _ = plt.yticks()
plt.yticks(locs, df_melhores.rotulo);


#%%
import seaborn as sns
sns.set()


#%%
ax = sns.boxplot(
    data=df_enem, y='CO_ESCOLA', x='nota_final', orient='h',
    order=df_melhores.head(NUM_MELHORES).CO_ENTIDADE)


#%%
import seaborn as sns
sns.set()
ax = sns.boxplot(data=df_enem, y='CO_ESCOLA', x='nota_final', orient='h',
                 order=df_melhores.head(NUM_MELHORES).CO_ENTIDADE)
locs, labels = plt.yticks()
plt.yticks(locs, labels);

print(locs, labels)


#%%
sns.boxplot(data=df_enem_rio, y='NO_ENTIDADE', x='NU_NOTA_REDACAO', orient='h',
            order=df_melhores.sort_values('rank')['NO_ENTIDADE'].head(NUM_MELHORES));


#%%
df_escolas.columns.tolist()

