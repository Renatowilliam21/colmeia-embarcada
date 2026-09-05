# Backlog — Colmeia + Needle 2 (pós-submissão ERCEMAPI 2026)

Itens identificados durante a preparação do artigo que não entraram na
submissão atual por restrição de prazo. Organizados por esforço estimado.

## Dataset e experimento

- [ ] **Repetir cada um dos 36 casos 3x**, para distinguir erro sistemático
      de variação estocástica do modelo. Recalcular Tabelas 1 e 2 com
      média/desvio-padrão em vez de execução única.
- [ ] **Balancear as categorias** — `parametro_implicito` e `ambiguos` têm
      só 6 casos cada; subir para 10-12 por categoria reduz a sensibilidade
      da métrica a um único caso.
- [ ] **Aguardar e incorporar o retorno do especialista em apicultura**
      (formulário PDF já enviado — `dataset_avaliacao_especialista.pdf`).
- [ ] **Adicionar casos com ruído de transcrição/digitação** (erros de
      ASR simulados), preparando terreno para a futura interface de voz.
- [ ] **Segundo anotador para o gabarito**, especialmente nos casos
      ambíguos, para medir concordância entre avaliadores.
- [ ] **Resolver formalmente o tratamento do caso 23** (dupla chamada) na
      contagem da Tabela 1 — hoje fica mencionado como "emergente" sem
      entrar no denominador de forma explícita.

## Modelo e hardware

- [ ] **V2 do plano de versões**: retomar a validação em hardware real
      (Sparkle N16R8) com o schema `colmeia.json`, resolvendo de vez a
      instabilidade de comunicação serial no Windows (avaliar WSL2 +
      usbipd como caminho já testado parcialmente, ou Linux nativo).
- [ ] **Medir latência fim-a-fim numa sessão já "primed"** no hardware
      real, para números de usabilidade em campo mais realistas do que os
      atuais (medidos com priming repetido a cada chamada).
- [ ] **V3 do plano de versões**: fine-tuning local via LoRA
      (`cactus-needle`) com corpus próprio de comandos apícolas em
      português, comparando acurácia antes/depois.
- [ ] **Adaptar o dataset Uirapuru** (tool-calling bilíngue PT-BR/EN-US,
      SynastrIA Networks, Hugging Face) como base complementar de dados
      de fine-tuning, em vez de escrever todo o corpus manualmente.
- [ ] **Integração real dos handlers** com a API de uma estação de
      monitoramento de colmeias (substituindo os dados mockados atuais).
- [ ] **Validação de campo com apicultores reais**, testando o sistema
      fora do ambiente controlado do motor host.

## Artigo (versão estendida / TCC / futura submissão)

- [ ] Adicionar citações de **RFCB** (Ionov & Malykh, 2026 — benchmark de
      function-calling para russo, precedente metodológico direto) e
      **Uirapuru** (dataset PT-BR de tool-calling) na Introdução.
- [ ] Mover a ressalva sobre latência (host vs. hardware real) para
      aparecer também na Metodologia, não só na Discussão — apontado no
      parecer simulado de avaliador como possível questionamento.
- [ ] Reordenar os parágrafos da Introdução por tema (domínio → tecnologia
      → contribuição) para reduzir o zigue-zague entre apicultura e IA
      identificado na revisão de legibilidade.
- [ ] Considerar mencionar o uso comercial real do Needle 2 (Pebble) como
      evidência de relevância prática além de benchmarks controlados.
- [ ] Publicar o dataset de 36 casos (ampliado) no Zenodo ou Hugging Face
      **após** a decisão do double-blind, com DOI citável.
- [ ] Se aceito, adicionar autoria completa (Renato + Luiz Henrique) e
      afiliação institucional na versão final camera-ready.

## Repositório

- [ ] Tornar o repositório `colmeia-embarcada` público (ou manter privado
      e criar um novo específico) **somente após** a decisão do double-blind.
- [ ] Definir licença final para código, dataset e artigo (sugestão: MIT
      para código, CC-BY para dataset e artigo).
