"""
Esqueleto do script de execucao em lote do dataset de teste.

IMPORTANTE: os nomes de funcao abaixo (conectar_serial, enviar_e_receber)
sao placeholders. Abrir needle_tui.py do fork, achar a funcao real que
envia um prompt e le a resposta da placa, e importar/reaproveitar essa
funcao aqui em vez de reescrever o protocolo serial do zero.
"""
import json
import time
import csv

# from needle_tui import conectar_serial, enviar_e_receber  # ajustar import real

DATASET_PATH = "../../dataset/colmeia-needle2-dataset-teste.json"
OUTPUT_PATH = "../../results/resultados_brutos.csv"
PORTA = "/dev/ttyACM0"


def main():
    with open(DATASET_PATH, encoding="utf-8") as f:
        dataset = json.load(f)["casos"]

    # porta = conectar_serial(PORTA)
    resultados = []

    for caso in dataset:
        inicio = time.time()
        # saida = enviar_e_receber(porta, caso["frase"])
        saida = None  # TODO: substituir pela chamada real
        duracao = time.time() - inicio
        resultados.append({
            "id": caso["id"],
            "categoria": caso["categoria"],
            "frase": caso["frase"],
            "saida_bruta": saida,
            "duracao_s": round(duracao, 1),
        })
        print(f"[{caso['id']:02d}] {duracao:5.1f}s  {caso['frase'][:40]:40}  -> {saida}")

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=resultados[0].keys())
        w.writeheader()
        w.writerows(resultados)


if __name__ == "__main__":
    main()
