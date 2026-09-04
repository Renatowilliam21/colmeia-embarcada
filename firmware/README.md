# Firmware — como obter e configurar o motor Needle 2

Este diretório NÃO contém uma cópia do motor Needle 2. Passos:

1. Fazer fork de https://github.com/andrisgauracs/needle-2-esp32 no GitHub
   (mantém histórico e atribuição corretos).
2. Clonar o fork localmente dentro desta pasta, por exemplo:
   `git clone <seu-fork> firmware/needle-2-esp32`
3. Substituir `tools/led.json` do fork por `firmware/tools/colmeia.json`
   deste repositório.
4. Implementar os 3 handlers em `main.c` (ver `docs/guia-desenvolvimento.md`
   para o código completo dos handlers e o registro na TOOL_TABLE).
5. Baixar o modelo `needle2.cact` via script Python (huggingface_hub) — não
   versionar esse binário neste repositório.
6. Build e flash: `idf.py set-target esp32s3 && idf.py build && idf.py -p <porta> flash`.

Placa validada neste experimento: Sparkle IoT XH-S3E N16R8
(ESP32-S3-WROOM-1, 16 MB flash, 8 MB PSRAM octal).
