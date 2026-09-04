# Colmeia v2.0 + Needle 2 — Schema de Tools e Plano de Trabalho

## 1. Schema de ferramentas (`tools/colmeia.json`)

Ponto de partida com **3 ferramentas** (dentro do orçamento confortável de tokens do
Needle 2 — cada ferramenta adicional custa ~40-80 tokens do contexto de 256 tokens).
Uma 4ª ferramenta (`consultar_historico`) fica marcada como opcional/fase 2, a testar
depois que as 3 primeiras estiverem validadas.

```json
[
  {
    "name": "consultar_status_colmeia",
    "description": "Consulta peso, temperatura e umidade atuais de uma colmeia",
    "parameters": {
      "type": "object",
      "properties": {
        "colmeia_id": {
          "type": "integer",
          "minimum": 1,
          "maximum": 50
        }
      },
      "required": ["colmeia_id"]
    }
  },
  {
    "name": "listar_colmeias_alerta",
    "description": "Lista colmeias com peso, temperatura ou umidade fora da faixa normal",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "ativar_modo_inspecao",
    "description": "Pausa alertas e aumenta frequencia de leitura durante inspecao manual",
    "parameters": {
      "type": "object",
      "properties": {
        "colmeia_id": {
          "type": "integer",
          "minimum": 1,
          "maximum": 50
        },
        "duracao_min": {
          "type": "integer",
          "minimum": 5,
          "maximum": 60
        }
      },
      "required": ["colmeia_id", "duracao_min"]
    }
  }
]
```

**Fase 2 (opcional, só depois de validar as 3 acima):**

```json
{
  "name": "consultar_historico",
  "description": "Consulta media de peso e temperatura de uma colmeia num periodo",
  "parameters": {
    "type": "object",
    "properties": {
      "colmeia_id": { "type": "integer", "minimum": 1, "maximum": 50 },
      "periodo": {
        "type": "string",
        "enum": ["hoje", "7dias", "30dias"]
      }
    },
    "required": ["colmeia_id", "periodo"]
  }
}
```

### Notas de design (aprendidas do repositório de referência)

- **Descrições curtas e específicas carregam peso real** — o texto do campo é o que
  ajusta o modelo a interpretar o comando certo. Evitar descrições genéricas tipo
  "consulta dados"; usar termos que apareceriam na fala real do apicultor (peso,
  temperatura, alerta, inspeção).
- **Nomes de ferramenta ≤ 39 caracteres.**
- **Tipos aceitos:** `string` (com `enum`), `integer`, `number`, `boolean`. Nada de
  objetos aninhados ou arrays — são rejeitados na compilação da gramática.
- **O modelo só preenche campos que consegue fundamentar no texto** — se o apicultor
  disser "a colmeia 3" sem mencionar duração, `ativar_modo_inspecao` fica sem
  `duracao_min` preenchido; o handler em C precisa tratar esse caso com um valor
  padrão (ex: 15 min), do mesmo jeito que o exemplo `set_servo` do repositório trata
  `degrees` ausente com `arg_num(args, "degrees", 90)`.
- **JSON precisa estar compactado** (sem indentação) no momento de embutir no
  firmware — o modelo foi treinado em schemas sem espaço em branco; um schema
  indentado degrada a precisão silenciosamente. Guardar a versão legível (acima)
  como fonte, e gerar a versão compactada no build, exatamente como o projeto de
  referência faz.

### Esqueleto de handler em C (adaptar do `main.c` de referência)

```c
static void tool_consultar_status_colmeia(const char *args)
{
    int id = (int)arg_num(args, "colmeia_id", -1);
    if (id < 1) { printf("ACT none\n"); fflush(stdout); return; }

    /* TODO: buscar peso/temp/umidade mais recentes da colmeia `id`
       (API HTTP da estacao Colmeia v2.0, ou leitura local se estiver
       no mesmo barramento) */

    printf("ACT status colmeia_id=%d peso=%.1f temp=%.1f umid=%.1f\n",
           id, peso, temperatura, umidade);
    fflush(stdout);
}
```

---

## 2. Plano de trabalho — Luiz Henrique (esqueleto de 2 meses)

Extensão de escopo dentro do plano já em andamento no Colmeia v2.0: interface de
comando por linguagem natural via Needle 2, rodando offline em um ESP32-S3 N16R8
dedicado (companheiro da estação apícola, comunicando por WiFi/HTTP local).

### Semana 1-2 — Estudo e setup do hardware
- [ ] Adquirir uma placa ESP32-S3 N16R8 (DevKitC-1 ou equivalente).
- [ ] Instalar ESP-IDF v5.5+ e clonar o repositório de referência
      (`andrisgauracs/needle-2-esp32`).
- [ ] Rodar o exemplo padrão (`led.json` + `set_servo`) até confirmar boot,
      resposta ao comando e LED reagindo — validação de que o hardware está correto
      antes de tocar em código próprio.
- [ ] Registrar no diário de bordo: tempo de boot, tempo por requisição, qualquer
      erro de PSRAM/console (comuns e documentados no troubleshooting do repo).

### Semana 3-4 — Mapeamento de tools e handlers
- [ ] Levantar quais dados a Colmeia v2.0 já expõe (peso, temperatura, umidade,
      histórico) e por qual via (API/serial/MQTT).
- [ ] Escrever `tools/colmeia.json` com as 3 ferramentas do schema acima.
- [ ] Implementar os handlers em `main.c`, inicialmente com dados simulados/mock.
- [ ] Testar cada ferramenta isoladamente com frases variadas em português
      ("como está a colmeia 3", "colmeia 3, peso e temperatura", "tem alguma
      colmeia com problema").

### Semana 5-6 — Integração com a estação real
- [ ] Substituir os mocks pelas chamadas reais à Colmeia v2.0.
- [ ] Implementar a comunicação companheira → estação (HTTP local, reusando o
      padrão de token do admin já existente no firmware da estação).
- [ ] Montar um pequeno conjunto de teste (20-30 frases) cobrindo variações de
      fala real de um apicultor, incluindo frases fora de escopo (para confirmar
      que o modelo devolve chamada vazia em vez de "chutar").
- [ ] Medir taxa de acerto e latência por requisição no hardware real.

### Semana 7 — Ajuste fino (opcional, se sobrar tempo)
- [ ] Gerar traços sintéticos de comando/resposta específicos do vocabulário
      apícola.
- [ ] Rodar `needle finetune` localmente e comparar acurácia antes/depois.

### Semana 8 — Documentação e entrega
- [ ] Relatório técnico curto (schema, decisões de design, resultados de teste).
- [ ] Vídeo demo do fluxo completo (fala → tool call → ação/consulta).
- [ ] Atualizar o plano de trabalho e o guia de entregáveis já existentes do
      Colmeia v2.0 com esta extensão de escopo.

### Critério de sucesso mínimo
Reconhecer corretamente os 3 comandos-base em pelo menos 80% de um conjunto de
teste de frases naturais, com latência aceitável para uso em campo (a referência
mede ~25-47s por requisição — combinar com Luiz Henrique se isso é aceitável para
o fluxo de inspeção ou se precisa ficar mais rápido reduzindo o schema).
