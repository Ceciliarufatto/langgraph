# Pitch do painel

Roteiro pra falar com quem parar no painel. Duração-alvo: 4 minutos, com folga pra perguntas. Quem não estiver falando fica do lado, pronto pra apontar o bloco em discussão.

## Divisão

| Tempo | Quem | Bloco |
|---|---|---|
| 0:00–0:40 | Cecilia | Contexto |
| 0:40–1:20 | Leonardo Quartaroli | Conceitos |
| 1:20–2:00 | Leonardo Moino | Estado da arte + arquitetura |
| 2:00–3:00 | Felipe | Experimento e resultados |
| 3:00–3:40 | Lorena | Discussão e próximos passos |
| 3:40–4:00 | quem estiver à mão | Fecho + QR |

## Falas

### Cecilia — contexto

"Oi, a gente é o G1. Trabalhou com LangGraph, um framework pra construir agentes de IA. A motivação central é que frameworks lineares como o LangChain tradicional rodam etapas em sequência fixa: primeiro isso, depois aquilo, fim. Mas agentes de verdade precisam de três coisas que o modelo linear não dá nativamente: ciclos pra refletir e retentar, estado persistente entre execuções, e decisões condicionais dinâmicas. LangGraph resolve isso modelando o agente como um grafo de estados."

### Leonardo Quartaroli — conceitos

"Os conceitos centrais são cinco. Primeiro o StateGraph, que é o grafo em si, com um estado tipado em TypedDict que todos os nós compartilham. Node é uma função Python que recebe o estado e devolve o estado. Conditional Edge é uma aresta condicional — uma função decide pra qual nó ir baseado no estado atual. Reducer define como o estado se atualiza quando dois nós escrevem no mesmo campo. E Checkpointer é a persistência: salva o estado entre execuções em SQLite, Postgres ou Redis. Ainda tem o Human-in-the-Loop, que pausa o grafo esperando input humano."

### Leonardo Moino — estado da arte e arquitetura

"Em 2022 a LangChain lançou chains lineares. Em 2024 saiu o LangGraph 0.0.x, e em 2025 a versão 1.0 estável com durable execution. Comparando com concorrentes: CrewAI tem ciclos limitados, AutoGen organiza tudo por chat entre agentes, OpenAI Swarm não tem persistência nativa. LangGraph é o único com estado tipado, ciclos e checkpointers oficiais ao mesmo tempo.

Nosso protótipo é um agente de atendimento ao cliente. Esse aqui é o grafo (apontar): a mensagem entra em `detect_intent`, é rotulada em pedido, suporte ou geral, e a aresta condicional `route_intent` despacha pro handler. Cada handler responde e grava o histórico em JSON."

### Felipe — experimento

"A gente montou um dataset de 40 mensagens em português rotuladas nessas três classes. Rodamos cada mensagem no grafo compilado, medindo latência com `time.perf_counter` e métricas com scikit-learn.

Os resultados (apontar tabela): accuracy de 85%, Macro F1 de 0,85, latência média de 33 ms — P95 em 56, ou seja, viável pra chat síncrono. Por classe, pedido e suporte ficam com F1 acima de 0,86. A matriz de confusão (apontar) mostra que os erros se concentram em frases que caem na classe geral, que funciona como fallback.

No GitHub tem um GIF curto da CLI: usuário manda 'quero rastrear meu pedido', o grafo roteia pro nó pedido; manda 'esqueci minha senha', vai pro suporte. Tudo persistido entre execuções."

### Lorena — discussão

"Do lado positivo, o StateGraph deixou o roteamento declarativo e testável — dá pra escrever testes em cima do grafo compilado direto. A persistência em JSON foi suficiente pro protótipo.

A limitação principal é que a classificação por keywords não captura semântica. A classe geral tem precision 0,73 porque vira sumidouro de frases ambíguas. Mensagens multi-intenção, tipo 'meu produto chegou quebrado e quero suporte', são forçadas a uma única rota.

A evolução natural são três passos: trocar o classificador por LLM few-shot com saída estruturada via Pydantic; adicionar nó de Human-in-the-Loop quando o confidence for baixo; e migrar a persistência pra SqliteSaver pra ter durable execution."

### Fecho

"Todo o código, dataset, métricas e o painel estão no nosso GitHub — o QR aqui no rodapé. A gente também trouxe one-pager pra levar (oferece). Valeu."

## Versões alternativas

**Pitch curto, 90 segundos**, caso a pessoa esteja com pressa:

"A gente trabalhou com LangGraph, framework pra agentes de IA baseado em grafos de estado. Construímos um agente de atendimento que classifica intenção (pedido, suporte ou geral) e roteia via aresta condicional. Conseguimos 85% de accuracy num dataset de 40 mensagens, com latência média de 33 ms. A limitação principal é que usamos classificação por keywords — a evolução natural é trocar por LLM few-shot. Código no QR aqui."

**Pitch técnico, 5 minutos**, pro professor: o roteiro acima com os trechos abaixo expandidos:

- Detalhar o AgentState (TypedDict, campos, reducers).
- Como `add_conditional_edges` funciona (mapping dict, função router).
- Por que JSON checkpointer em vez de SqliteSaver no protótipo.
- Como o confidence é calculado e por que é ingênuo.
- Trade-off de não usar LLM no classificador (custo, latência, determinismo).

## Coisas pra lembrar

- Não ler o painel. Olhar pra pessoa e usar o painel como apoio visual.
- Apontar fisicamente o bloco que está sendo descrito.
- Se a pessoa demonstrar interesse, pausar pra perguntas no meio.
- Quem não estiver falando fica em silêncio mas presente.
- Cronometrar pelo menos dois ensaios antes da sessão.

## Antes de começar

- Combinaram quem fica defendendo na primeira metade e quem visita.
- One-pagers à mão.
- Celular com o QR testado e o GIF carregado.
- Painel fixado firme.
