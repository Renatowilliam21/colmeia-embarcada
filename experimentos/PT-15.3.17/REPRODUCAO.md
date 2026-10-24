# PT-15.3.17 — Guia de reprodução

## Ambiente

- Plataforma: ESP32-S3 N16R8
- ESP-IDF: 5.4.2
- Modelo: Needle 2
- Configuração C2: prefixo 205, sink 192, tail 13

## 1. Clonar o projeto

    git clone -b revisao-ercemapi-2026 https://github.com/Renatowilliam21/colmeia-embarcada.git
    cd colmeia-embarcada

## 2. Obter o motor Needle 2

    mkdir -p external
    git clone https://github.com/andrisgauracs/needle-2-esp32.git external/needle-2-esp32
    git -C external/needle-2-esp32 checkout 61cafad7014a5664bb3ffd5f0c457ce5aa6598ae

## 3. Aplicar o patch do cache KV

    git -C external/needle-2-esp32 apply ../../experimentos/PT-15.3.17/patches/needle2_kv_snapshot_PT15317.patch

Verificar a aplicação:

    git -C external/needle-2-esp32 diff --stat

O patch modifica nd_model.c e nd_model.h.

## 4. Preparar o ESP-IDF

    source "$HOME/esp/esp-idf/export.sh"
    idf.py --version

## 5. Compilar o firmware

    cd firmware/esp32/colmeia_needle
    idf.py set-target esp32s3
    idf.py build

## 6. Modelo na memória flash

O firmware depende de um modelo Needle 2 compatível previamente gravado na partição esperada.
A compilação não grava automaticamente o modelo.
Não executar erase-flash em dispositivos com o modelo já instalado.

## 7. Evidências experimentais

- PT-15.3.17-D/integridade_kv.md
- PT-15.3.17-E/resultados.csv
- relatorio_PT-15.3.17.md

## 8. Limitações

A aplicação do patch foi validada sobre o commit-base identificado.
O firmware instrumentado foi compilado e executado no ambiente experimental original.
A compilação em um clone limpo ainda não foi verificada independentemente.
As ferramentas foram executadas em modo simulado.
