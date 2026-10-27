# Protocolo experimental documentado

## Ambiente

- Execução: Linux host.
- Motor: `nd_dump`, do projeto Needle 2 para ESP32.
- Commit de referência: `61cafad7014a5664bb3ffd5f0c457ce5aa6598ae`.
- Modelo: `needle2.cact`.
- Modelo SHA-256: `b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba`.
- Schema SHA-256: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`.

## Configuração registrada

- Dataset: 36 frases em português.
- Repetições: 1 por frase.
- `max_new`: 96.
- `think`: false.
- Timeout por inferência: 300 segundos.
- Dataset SHA-256: `44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e`.

## Arquivos

- `artefatos/dataset/dataset_original_36_casos.json`
- `artefatos/schema/schema_historico_original.json`
- `artefatos/execucao/metadata_original.json`
- `artefatos/execucao/raw_results_original.jsonl`

O motor e o arquivo binário do modelo não foram copiados para este pacote.
Sua obtenção e a compatibilidade do ambiente devem ser verificadas
separadamente antes de qualquer reprodução.

Não há comprovação de temperatura, top-k ou top-p no manifesto original.
Não inferir valores para esses parâmetros.
