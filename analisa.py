# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Analisa dados do ENEM
#
# Lê os dados pré-processados que foram gerados pelo notebook `ledados.ipynb` e os analisa. Vá para o final para ver os ranking final.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import IPython
get_ipython().run_line_magic('matplotlib', 'inline')
#pd.options.display.max_rows = None
#pd.options.display.max_columns = None


# %%
NUM_MELHORES = 60
MIN_ALUNOS = 30 #Mínimo de alunos que fizeram Enem para considerar a escola


# %%
CO_SAO_BENTO = 33062633
CO_SAO_VICENTE = 33063648
CO_PARQUE = 33065837
CO_ELEVA = 33178860
CO_ST_INACIO = 33063729
CO_MUN_RIO = 3304557
CO_UF_RIO = 33


# %%

df_escolas = pd.read_feather('dados/escolas_rio_2018.feather')
df_primeiro_ano_turmas = pd.read_feather('dados/primeiro_ano.feather')


# %%
df_enem_rio = pd.read_feather('dados/enem_rio_2018.feather')

# %% [markdown]
#  ## Cálculo da nota final
#  Abaixo pode-se personalizar o cálculo de nota final. pondero pelas notas mais importantes.
#
#  O Inep costuma considerar a redação como tendo um peso igual às outras disciplinas.
#
#  Algumas universidades consideram um peso distinto de acordo com a disciplina
#
#  ### Pesos UFRJ
#
#  Referência dos [pesos da UFRJ](https://oglobo.globo.com/sociedade/educacao/ufrj-usara-pesos-diferentes-em-provas-do-enem-2011-para-acesso-aos-cursos-de-graduacao-2865665).
#
#  - Redação: peso 3 (mínimo 300)
#  - Ciência da Computação, Ciências Atuariais, Engenharias, Estatística, Matemática e Química Industrial
#      - Matemática tem peso 4
#  - Ciências Econômicas, Geologia e Meteorologia
#      - Matemática peso 3
#  - Engenharias e Química Industrial
#      - Ciências da Natureza: peso 4
#  - Geologia
#      - Ciências da Natureza: peso 3
#  - Humanas
#      - Ciências Humanas e Linguagens: peso 2
#
#

# %%
notas_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', ]
notas_pesos =(1, 1, 1, 1, 4) #peso do Inep com redação igual os demais
notas_pesos =(1, 1, 1, 1, 1) #peso do Inep com redação igual os demais


# %%
media_ponderada = lambda notas: np.average(notas, weights=notas_pesos)

#df_enem_rio me dá as notas do enem de cada aluno de escola do rio de janeiro
df_enem_rio['nota_final'] = df_enem_rio.loc[df_enem_rio.TP_ST_CONCLUSAO == 2, notas_cols ]                                       .apply(media_ponderada, axis=1)                                       .round(0)
df_enem_rio[notas_cols+ ['nota_final']].head()


# %%
#df_enem sãos as notas agrupadas por escola e ordenadas da melhor para a pior
def notas_enem(df_enem_rio):
    notas_agg = {col: (col, 'median') for col in notas_cols}
    notas_agg['mediana'] = ('nota_final', 'median')
    notas_agg['num'] = ('nota_final', 'count')

    return df_enem_rio.groupby('CO_ESCOLA')                      .agg(**notas_agg)                      .sort_values('mediana', ascending=False)                      .query('num > @MIN_ALUNOS')#corte arbitrário
df_enem = notas_enem(df_enem_rio)
df_enem


# %%
df_enem['rank'] = df_enem.mediana.rank(ascending=False, method='min')


# %%
#vamos colocar o nome das escolas
df_enem = df_enem.merge(df_escolas[['NO_ENTIDADE', 'CO_ENTIDADE']], left_index=True, right_on='CO_ENTIDADE')


# %%
df_enem

# %% [markdown]
# Respondendo uma pergunta sinistra: quantas escolas com ensino médio não tiveram qualquer aluno fazendo Enem?
#
# ih, não dá, já filtrei o df_enem

# %%
my_order = df_enem.head(NUM_MELHORES).NO_ENTIDADE

# %% [markdown]
# Ajustando nomes de escolas. Estão muito grandes.
#

# %%
df_nomes_grandes = df_enem[:100][['CO_ENTIDADE', 'NO_ENTIDADE']]
df_nomes_grandes['comprido'] = df_nomes_grandes.NO_ENTIDADE.str.len()
df_nomes_grandes.sort_values('comprido', ascending=False).head(30)

#vamos ajustar alguns nomes
df_enem.loc[df_enem.CO_ENTIDADE==33176825, 'NO_ENTIDADE'] = 'COLEGIO SANTO AGOSTINHO - BARRA'
df_enem.loc[df_enem.CO_ENTIDADE==33066523, 'NO_ENTIDADE'] = 'CAP - UERJ'
df_enem.loc[df_enem.CO_ENTIDADE==33132534, 'NO_ENTIDADE'] = 'GARRA VESTIBULARES - UNID 1'
df_enem.loc[df_enem.CO_ENTIDADE==33057206, 'NO_ENTIDADE'] = 'INSTITUTO GAYLUSSAC'
df_enem.loc[df_enem.CO_ENTIDADE==33142726, 'NO_ENTIDADE'] = 'COL ISRAELITA LIESSIN'
df_enem.loc[df_enem.CO_ENTIDADE==33027722, 'NO_ENTIDADE'] = 'COLEGIO SAGRADO CORACAO DE JESUS'
df_enem.loc[df_enem.CO_ENTIDADE==33065250, 'NO_ENTIDADE'] = 'CAP - UFRJ'
df_enem.loc[df_enem.CO_ENTIDADE==33106754, 'NO_ENTIDADE'] = 'COLEGIO PROF CLOVIS TAVARES PRO-UNI'
df_enem.loc[df_enem.CO_ENTIDADE==33155259, 'NO_ENTIDADE'] = 'COLEGIO SALESIANO REGIAO OCEANICA'

for i, j in (('COLEGIO', 'COL'),
             ('INSTITUTO', 'INST'),
             ('FILIAL', '-'),
             ('UNIDADE ', ''),
             ('PROFESSOR', 'PROF'),
             ('EDUCACIONAL', 'EDUC.'),
            ):
    df_enem['NO_ENTIDADE'] = df_enem.NO_ENTIDADE.str.replace(i, j)

df_nomes_grandes.sort_values('comprido', ascending=False).head(30)


# %%
df_enem['rotulo'] = df_enem.loc[:,['NO_ENTIDADE', 'num', 'rank']].apply(lambda x: '{:>s} {:03d}/{:>2.0f}'.format(x[0].title(), x[1], x[2]), axis=1)


# %%
df_enem

# %% [markdown]
# ## Distribuição das notas parece bimodal
#
# Um monte de escolas com notas baixa (500), depois outro grupo com notas mais altas (700). Seria legal ver as distribuições por grupos.

# %%
ax = df_enem.mediana.hist(bins=24).plot();
#ax.tick_params(which='both', bottom=False, labelbottom=False)

# %% [markdown]
# ## Comparando distribuições das escolas
#
# Legenda: Nome da escola <nº alunos fizeram Enem>/<posição ranking nota final>

# %%


def compara_distribuicoes(nota, num_escolas=NUM_MELHORES):
    sns.set(rc={'figure.figsize':(14,18), 'axes.xmargin': .1})
    #sns.palplot(sns.hls_palette(8, l=.3, s=.8))

    nota_agrupada = nota
    if nota=='nota_final':
        nota_agrupada = 'mediana'

    df_top = df_enem.sort_values(nota_agrupada, ascending=False).head(num_escolas)
    ax = sns.boxplot(data=df_enem_rio, y='CO_ESCOLA', x=nota, orient='h'
                     ,order=df_top.CO_ENTIDADE)
    ax.set(ylabel='', xlabel='')
    plt.gcf().subplots_adjust(top=.95)
    plt.suptitle(f'{nota} por escola',x=0, size=24, );
    locs, _ = plt.yticks()
    plt.yticks(locs, df_top.rotulo);
    ax.set_xlim(300, 1000)


compara_distribuicoes('nota_final');


# %% [markdown]
# Um dado estranho, o Santo Inácio tem 245 alunos que disseram que completaram agora, mas há apenas 235 no 3º ano de 2018. Será que é preenchimento errado? Será que estou contando jovens e adultos? Será que acontece o mesmo com outras escolas?

# %%
compara_distribuicoes('NU_NOTA_MT');


# %%
compara_distribuicoes('NU_NOTA_REDACAO', 90);


# %%
compara_distribuicoes('NU_NOTA_CH');

# %% [markdown]
# ## Distribuição notas de redação

# %%
plt.style.use('seaborn-whitegrid')
plt.box(False)
plt.set_cmap(plt.cm.Pastel1)
num_ploted=0
def plot_cdf(co_escola, label):
    global num_ploted
    plt.hist(df_enem_rio.query("CO_ESCOLA == @co_escola").NU_NOTA_REDACAO.dropna(),
             cumulative=True, histtype='step', linewidth=3,
             color=plt.cm.Set1.colors[num_ploted],
             density=True, bins=df_escola.size, label=label);
    num_ploted += 1

#plot_cdf(CO_SAO_VICENTE, 'São Vicente')
#plot_cdf(CO_SAO_BENTO, 'São Bento')
#plot_cdf(CO_PARQUE, 'Parque')
plot_cdf(CO_ST_INACIO, 'Santo Inácio')
#plt.legend(fontsize='xx-large', framealpha=.1, facecolor='white' )

plt.yticks(np.linspace(0, 1, 11));
plt.xticks(np.linspace(0, 1000, 11));



# %%
plt.cm.Dark2.colors

# %% [markdown]
#  ## Sobrevivência no ensino médio
#
#  Quantos dos alunos que começam o ensino médio fazem Enem?
#
#  Motivos para diminuir:
#  - Maus alunos são expulsos
#  - Maus alunos não acreditam que passarão no Enem
#  - Vai para universidade fora do Enem (ITAs, PUCs, USP, exterior etc.)
#
#  Motivos para aumentar:
#  - Crise econômica (escolas públicas)
#  - Bolsa para bons alunos
#
#  ### ideias
#  - comparar com último ano (dá ideia melhor da seleção feita pela escola)
#  - comparar com quem fez prova (ideia melhor de auto seleção)

# %%
plt.cm.Paired.colors


# %%
etapa_col = 'TP_ETAPA_ENSINO'
primeiro_ano = [25,  30, 35]
# todo: tratar ensinos médios de 4 anos
df_primeiro_ano_turmas = pd.read_feather('dados/primeiro_ano.feather')



# %%
df_ano_um = df_primeiro_ano_turmas.groupby(['id_escola', 'ano'])['num_matriculas'].sum()
CO_ELEVA=33178860
df_ano_um = df_ano_um.unstack()
df_ano_um


# %%
df_ano_um[df_ano_um==1] = np.nan  # tem um Pensi aqui com dado esquisito
porcentagem_variacao = .5
anos_idx = slice(0, 11) #colunas com dados de alunos no primeiro ano
df = (df_ano_um.drop(2007, axis='columns')
          .merge(df_enem.head(NUM_MELHORES)[['CO_ENTIDADE', 'rotulo', 'rank']],
                 left_index=True, right_on='CO_ENTIDADE') #pegando nome das escolas e só das melhores
         .set_index('rotulo')
         .assign(alta_variacao=  #variação do número de alunos
                 lambda df: (df.iloc[:,anos_idx].max(axis='columns') - df.iloc[:,anos_idx].min(axis='columns'))
                            /df.iloc[:,anos_idx].max(axis='columns'))
         .query('alta_variacao > @porcentagem_variacao')
         .sort_values('alta_variacao', ascending=False) #mostrando primeiro as com maior variação
         .drop(['CO_ENTIDADE', 'rank'], axis='columns')
         .dropna(thresh=6) # joga fora quem não tem pelo menos 6 anos preenchidos
     )
alta_variacao = df.pop('alta_variacao')
df = df.T

sns.set(rc={'figure.figsize':(10,18), 'axes.xmargin': .1})
axes = df.plot.line(subplots=True, layout=(11,3), sharey=True);

i = 0
for axes2 in axes:
    for ax in axes2:
        if i < len(alta_variacao):
            ax.set_title(df.columns[i], ha='left', x=0, size=10)
            #ax.legend().set_visible(False)
            ax.legend(['{:.0%}'.format(alta_variacao.iloc[i])])
            ax.set_yscale("log", basey=2)
        i += 1
sns.set()
fig = plt.gcf()
fig.suptitle("Bons colégios com variação de mais de {:.0%} nº alunos no 1º ano".format(porcentagem_variacao),
                 size=22, ha='left', x=0);
plt.subplots_adjust(hspace=.3, wspace=.2, left=.04, top=.93, bottom=0)
plt.xticks(range(2008, 2019));

# %% [markdown]
# Escrito na legenda acima está a variação entre o máximo e mínimo de alunos do primeiro ano de cada escola.
#
# - Pensi tem grandes variações, tanto uma queda drástica em 2012, como um grande crescimento
# - Vários colégios de Niterói/São Gonçalo perdendo alunos:  Salesiano Santa Rosa, Abel, Santa Mônica
# - escola parque barra crescendo
# - PH varia muito (com queda drástica no final)
# %% [markdown]
# ## Comparando nº alunos que fizeram ENEM vs alunos no 1º ano

# %%
df = df_enem.head(NUM_MELHORES).set_index('CO_ENTIDADE')
df = df.join(df_ano_um[[2016]] )
df['%'] = df.num/df[2016]
# tirando do plot alguns outliers. Tem escola com 10 vezes mais alunos!
df[df['%']<1.5].plot.scatter(x='%', y='mediana', c='blue');

# %% [markdown]
# Entre os bem colocados, quem aumenta o número de alunos?

# %%
df.loc[df['%']>=1, ['rotulo', '%', 'mediana', 'rank', 'num']].sort_values('%', ascending=False)

# %% [markdown]
# Quem aumenta o número de alunos? Pensi, de A a Z e PH. Estes são mais cursinhos pré-vestibular do que escolas. Vou tirá-los da lista. O Colégio [Dom Bosco](https://www.colegiodombosco.com.br/) é um colégio tradicional de Resende, então vou manter.

# %%
df_sem_outliers = df[df['%']<1.06]
sns.set()
sns.regplot(data=df_sem_outliers, x='%', y='mediana');
print("A correlação de {:.2n} entre notas e perdas de alunos é fraca".format(df_sem_outliers[['%', 'mediana']].corr().iat[0,1]))


# %%
df.loc[:, ['rotulo', 2016, 'num', '%', 'mediana', 'rank']].style.hide_index().format({'%': '{:.0%}'.format})

# %% [markdown]
# Entre os que mais diminuem o número de alunos também estão o Pensi e o PH. Impressionante, o CAP da Uerj tem bem poucos alunos fazendo Enem. Vamos dar uma olhada como os colégios que também são cursos variam de número de alunos.

# %%
df_cursos = df.loc[(df.rotulo.str.contains('Ph|Curso Pensi|A A Z')),['rotulo', 'mediana', 'rank', '%']]
df_cursos.style.hide_index().format({'%': '{:.0%}'.format})

# %% [markdown]
# A variação de alunos destes cursos é impressionante. O melhor colocado tem menos de metade dos alunos do início do ensino médio. Enquanto outros tem um aumento impressionante. Não parece uma comparação justa com as escolas mais tradicionais.

# %%
df.loc[df['%']<4, '%'].hist(bins=30).plot();


# %%
df.loc[df['%']<4, '%'].describe()


# %%
df['%'].quantile([i/10 for i in range(11)])


# %%
# isso aqui é enrolado. Entre as NUM_ESCOLAS melhores escolas, quais mais cortam alunos entre
# primeiro ano e o Enem?
menor_quantil = df['%'].quantile(.2) #arbitrário
menor_quantil

# %% [markdown]
# ## Seleção de escolas para ranking
#
# Retirando quem eu não quero contar:
# - quem aumenta o número de alunos (só fica o Dom Bosco com variação 1.02)
# - quem corta aluno demais, isto é os 80% que menos cortam, isto é, pelo menos 64% dos alunos do 1º ano devem fazer Enem (não verifico se são os mesmos alunos). Isso privilegia as escolas que menos cortam alunos. Por outro lado prejudica escolas cujos bons alunos foram para outra escola.
# - Pelo menos 35 alunos fazendo Enem.
#
#
# Os 2 primeiro critérios cortam quase todos os cursinhos: Pensi, A a Z e PH
#
# E depois vem o critério mais radical. Contarei quantos alunos eriam 64% do primeiro ano e contarei apenas este número das melhores notas. Isto privilegiará as escolas que mantém um número de alunos constante do primeiro ao último ano do ensino médio.

# %%
df_escolas_selecionadas = df.loc[(df['%'] < 1.02) &
                                 (df['%'] >= .62 ) &  #menor_quantil) &
                                 (df['num'] >= 35),

                                 ['rotulo', 2016, '%']
                                ]
print("Antes dos cortes tínhamos {:n} melhores escolas, depois ficamos com {:n}, cortando {:.1%}"
      .format( NUM_MELHORES, len(df_escolas_selecionadas), (NUM_MELHORES-len(df_escolas_selecionadas))/NUM_MELHORES) )

# %% [markdown]
# Agora vem o radical, pegaremos apenas os melhores 64 percentil das notas.

# %%
#df_escolas_selecionadas ['num_candidatos_considerados'] = (df_escolas_selecionadas[[2016]] * menor_quantil).round().astype('int16')
df_escolas_selecionadas ['num_candidatos_considerados'] = (df_escolas_selecionadas[[2016]] * .7).round().astype('int16')
df_escolas_selecionadas


# %%

df_melhores_alunos = pd.concat(g.nlargest(df_escolas_selecionadas.at[escola_id, 'num_candidatos_considerados'], columns='nota_final')
                               for escola_id, g in df_escolas_selecionadas[['rotulo']]
                                                    .merge(df_enem_rio.sort_values(['CO_ESCOLA', 'nota_final']), left_index=True, right_on='CO_ESCOLA')
                                                    .groupby('CO_ESCOLA')
                     )
df_melhores_alunos = df_enem_rio
df_final = notas_enem(df_melhores_alunos).join(df_escolas_selecionadas[['rotulo']], how='inner')
df_final['rank'] = df_final.mediana.rank(ascending=False, method='min')
df_final

#     notas_agg = {col: (col, 'median') for col in notas_cols}
#     notas_agg['mediana'] = ('nota_final', 'median')
#     notas_agg['num'] = ('nota_final', 'count')

#     return df_enem_rio.groupby('CO_ESCOLA')\
#                       .agg(**notas_agg)\
#                       .sort_values('mediana', ascending=False)\
#                       .query('num > @MIN_ALUNOS')#corte arbitrário


# %%
df_final.reset_index().to_feather('dados/final.feather')


# %%
#dever de casa

# %% [markdown]
# analisar colégios que estão com NAN na percentagem acima, especialmente o **Santo Agostinho Barra**

