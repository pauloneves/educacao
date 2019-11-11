# título

1. import pandas_profiling;pd.read_csv(''

1. Comparo melhores alunos das melhores escolas, comparando especialmente alunos das escolas que mais selecionaram, com as que menos selecionaram.
   1. Acredito que as boas escolas públicas sejam as que tenham menos seleção
   1. Ver reprovação das escolas

- Critérios filtro de escolas:
  - tirei A a Z, PH e Pensi (será que os outros critérios não bastam?)
  - 80% melhor percentil: para compensar quem reprova os alunos ruins. Ex: Santo Agostinho tem 80%, o Santo Inácio tem 95%
  - escolas que aumentam o número de alunos do 1º ano para o enem. Pode ser injusto com colégios em que saíram alunos.
  - só conta alunos que terminaram naquele ano (não tem quem está refazendo a prova ou treinando)
  - escolas com pelo menos 35 alunos fazendo a prova

## Dúvidas

1. consigo cruzar dados do aluno em uma escola com quem fez a prova do enem?
2. Dá para acompanhar se um aluno vai de uma escola para outra?
3. Consigo saber se um aluno do 3º ano estava no primeiro ano?
