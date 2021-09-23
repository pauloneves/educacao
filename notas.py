import numpy as np
import pandas as pd
import const

notas_cols = [
    "NU_NOTA_CN",  # ciências natureza
    "NU_NOTA_CH",  # ciências humanas
    "NU_NOTA_LC",  # português
    "NU_NOTA_MT",  # matemática
    "NU_NOTA_REDACAO",
]
notas_pesos = (1, 1, 1, 1, 4)  # peso do Inep com redação igual os demais
notas_pesos = (1, 1, 1, 1, 1)  # peso do Inep com redação igual os demais
media_ponderada = lambda notas: np.average(notas, weights=notas_pesos)

# df_enem sãos as notas agrupadas por escola e ordenadas da melhor para a pior
def notas_enem(df_enem_rio) -> pd.DataFrame:
    df_enem_rio = calcula_notas(df_enem_rio)
    notas_agg = {col: (col, "median") for col in notas_cols}
    notas_agg["num_alunos"] = ("nota_final", "count")  # type: ignore
    notas_agg["mediana"] = ("nota_final", "median")
    notas_agg["perc_80"] = ("nota_final", lambda x: x.quantile(0.8))  # type: ignore

    df_enem = (
        df_enem_rio[["CO_ESCOLA", "NU_ANO", "nota_final"] + notas_cols]  # type: ignore
        .groupby(["CO_ESCOLA", "NU_ANO"])
        .agg(**notas_agg)
        .query("num_alunos > @const.MIN_ALUNOS")
        .sort_values("mediana", ascending=False)
    )
    df_enem["rank"] = df_enem.mediana.rank(ascending=False, method="min")
    tipos_pequenos = {n: "float16" for n in notas_agg.keys()}
    tipos_pequenos["rank"] = "int16"
    tipos_pequenos["NU_ANO"] = "int16"
    return df_enem.reset_index().astype(tipos_pequenos)


def calcula_notas(df: pd.DataFrame):
    # tira todo mundo que tirou alguma nota zero
    for nota in notas_cols:
        df = df[df[nota] > 0]
    df["nota_final"] = (
        df.loc[
            (df.TP_ST_CONCLUSAO == 2)  # concluiu ensino médio no ano da prova
            & (df.TP_ENSINO == 1),  # ensino regular, sem EJA nem supletivos
            notas_cols,
        ]
        .apply(media_ponderada, axis=1)
        .round(0)
    )
    return df
