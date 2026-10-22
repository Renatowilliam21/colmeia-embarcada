# Protocolo v2 — avaliação experimental

Este protocolo é **proposto**, não é uma reclassificação retroativa dos resultados publicados.

- A entrada do avaliador é uma lista JSON de observações `{ "id": 1, "saida": [{"name":"...","arguments":{...}}] }`.
- A saída do modelo é normalizada para lista de chamadas. `[]` representa abstenção/rejeição, mas **não** diferencia solicitação de esclarecimento de rejeição; tal distinção requer uma interface mais rica.
- Casos 17, 18, 19, 20, 22, 24, 25, 26 e 27: sem ferramenta executável segura, a avaliação v2 considera `[]` uma abstenção segura. Isso não prova que o sistema perguntou ao usuário.
- Caso 23: duas consultas para colmeias 3 e 4 são semanticamente corretas em v2, independentemente da ordem; permanecem não avaliáveis no gabarito histórico.
- Casos 21 e 13: conversões temporais explícitas devem produzir 15 e 30 minutos, respectivamente.
- Caso 20: a ferramenta não possui filtro temporal, portanto responder sobre “últimos dias” exige esclarecimento ou capacidade adicional.
- `ativar_modo_inspecao` modifica o estado operacional: mesmo quando a saída é semanticamente correta, requer autorização explícita antes de executar.
- `schema_valido` verifica nomes, campos, tipos inteiros e limites básicos; não substitui um validador JSON Schema integral.
- `historico=nao_avaliavel` não deve ser contabilizado como erro nem como acerto. A taxa publicada de 36,1% permanece um resultado histórico separado.
- O avaliador não mede latência, confiança, consumo de energia ou qualidade de respostas em linguagem natural.
