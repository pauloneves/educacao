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
notas_pesos = (1, 1, 1, 1, 2)  # peso do Inep com redação igual os demais
media_ponderada = lambda notas: np.average(notas, weights=notas_pesos)

# df_enem sãos as notas agrupadas por escola e ordenadas da melhor para a pior
def notas_enem(df_enem_rio) -> pd.DataFrame:
    # nota final e rank não deveria estar aqui
    df = df_enem_rio.loc[
        (df_enem_rio.TP_ST_CONCLUSAO == 2)  # concluiu ensino médio no ano da prova
        & (df_enem_rio.TP_ENSINO == 1),  # ensino regular, sem EJA nem supletivos
        notas_cols + ["CO_ESCOLA", "NU_ANO"],
    ]

    df["nota_final"] = calcula_nota_final(df)
    df = enem_ajusta_cols(df)
    notas_agg = {col: (col, "median") for col in df.columns if col.startswith("nota_")}
    notas_agg["num_alunos"] = ("nota_final", "count")  # type: ignore

    notas_agg.update(  # type: ignore
        {
            f"{col}_perc80": (col, lambda x: x.quantile(0.8))
            for col in df.columns
            if col.startswith("nota_")
        }
    )

    df_enem = (
        df.dropna()
        .groupby(["CO_ESCOLA", "Ano"])
        .agg(**notas_agg)
        .query("num_alunos > @const.MIN_ALUNOS")
        .sort_values("nota_final", ascending=False)
    )
    df_enem["rank"] = df_enem.nota_final.rank(ascending=False, method="min")

    # reduz tamanho do array
    tipos_pequenos = {n: "float16" for n in notas_agg.keys()}
    tipos_pequenos["rank"] = "int16"
    tipos_pequenos["Ano"] = "int16"
    return df_enem.reset_index().astype(tipos_pequenos)


def calcula_nota_final(df: pd.DataFrame):
    return df[notas_cols].apply(media_ponderada, axis=1).round(0)


def calcula_nota_final_sobre_medianas(
    df: pd.DataFrame,
    pesos={
        "nota_matemática": 1,
        "nota_ciências": 1,
        "nota_português": 1,
        "nota_redacao": 2,
        "nota_humanas": 1,
    },
):
    df["nota_ponderada"] = (
        df[pesos.keys()]
        .apply(lambda notas: np.average(notas, weights=pesos.values()), axis=1)
        .round(0)
    )
    df["rank_ponderado"] = df.nota_ponderada.rank(ascending=False, method="min")


def enem_ajusta_cols(df):
    return df.rename(
        columns={
            "NU_ANO": "Ano",
            "NU_NOTA_CN": "nota_ciências",
            "NU_NOTA_CH": "nota_humanas",
            "NU_NOTA_LC": "nota_português",
            "NU_NOTA_MT": "nota_matemática",
            "NU_NOTA_REDACAO": "nota_redação",
        }
    )
