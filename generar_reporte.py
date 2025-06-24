import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


def generar_reporte(archivo_datos="partida_simulada.json", winrate_log="winrate_por_ciclo.txt", salida_dir="graficas"):
    os.makedirs(salida_dir, exist_ok=True)

    # Winrate trends
    if os.path.exists(winrate_log):
        try:
            df_win = pd.read_csv(winrate_log, names=["ciclo", "winrate"])
            plt.figure()
            plt.plot(df_win["ciclo"], df_win["winrate"], marker="o")
            plt.title("Winrate por ciclo")
            plt.xlabel("Ciclo")
            plt.ylabel("Winrate (%)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(salida_dir, "winrate_trend.png"))
            plt.close()
        except Exception as e:
            logging.error("Error al generar grafico de winrate: %s", e)

    # Synergy usage
    if os.path.exists(archivo_datos):
        try:
            with open(archivo_datos, encoding="utf-8") as f:
                datos = json.load(f)
        except Exception as e:
            logging.error("Error al leer %s: %s", archivo_datos, e)
            datos = []

        conteo = {}
        for ronda in datos:
            for sin, val in ronda.get("sinergias", {}).items():
                conteo[sin] = conteo.get(sin, 0) + val

        if conteo:
            df_sin = pd.DataFrame(list(conteo.items()), columns=["sinergia", "uso"])
            df_sin.sort_values("uso", ascending=False, inplace=True)
            csv_path = os.path.join(salida_dir, "sinergias.csv")
            df_sin.to_csv(csv_path, index=False)

            plt.figure(figsize=(8, 4))
            plt.bar(df_sin["sinergia"], df_sin["uso"])
            plt.title("Uso de sinergias")
            plt.ylabel("Apariciones")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(os.path.join(salida_dir, "sinergias.png"))
            plt.close()


