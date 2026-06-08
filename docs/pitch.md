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

"Os pontos principais são:
- `StateGraph`: grafo de estados com `TypedDict` compartilhado.
- `Node`: função Python que recebe o estado e devolve o estado.
- `Conditional Edge`: decisão condicional que escolhe o próximo nó com base no estado.
- `Reducer`: regra de mesclagem quando vários nós atualizam o mesmo campo.
- `Checkpointer`: persistência entre execuções.
- `Human-in-the-Loop`: opção de pausar o grafo para input humano."

### Leonardo Moino — estado da arte e arquitetura

"Em 2022 a LangChain popularizou pipelines lineares; em 2024 surgiu o LangGraph 0.0.x e em 2025 a versão 1.0 com durable execution. Diferente de CrewAI, AutoGen e OpenAI Swarm, o LangGraph combina estado tipado, ciclos e checkpointers nativos.

No protótipo de atendimento, a entrada passa por `detect_intent`, é classificada em `pedido`, `suporte` ou `geral`, e `route_intent` dispara o handler correto. Cada handler gera a resposta e grava o histórico em JSON."

### Felipe — experimento

"Montamos um dataset de 40 mensagens em português rotuladas em três classes. Cada frase foi processada pelo grafo compilado; latência foi medida com `time.perf_counter` e métricas foram calculadas com scikit-learn.

Resultados: accuracy de 85%, Macro F1 de 0,85, latência média de 33 ms e P95 de 56 ms. `pedido` e `suporte` alcançaram F1 acima de 0,86; a classe `geral` agrega as frases ambíguas e domina os erros. O GIF no GitHub mostra os roteamentos ao vivo: um pedido vai para `pedido`, uma senha perdida vai para `suporte`, e o histórico é mantido."

### Lorena — discussão

"O StateGraph torna o roteamento declarativo e testável; a persistência em JSON foi adequada para o protótipo.

A principal limitação é a classificação por keywords, que não captura semântica. A classe `geral` tem precision 0,73 porque agrega sentenças ambíguas, e mensagens multi-intenção acabam forçadas a uma rota única.

Evolução natural:
- trocar o classificador por LLM few-shot com saída estruturada via Pydantic;
- incluir Human-in-the-Loop quando a confiança for baixa;
- migrar a persistência para `SqliteSaver` para durable execution."

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
