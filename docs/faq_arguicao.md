# Perguntas prováveis na arguição

Lista de perguntas que provavelmente vão cair quando o professor passar pro Q&A. Cada um do grupo fica responsável por umas três.

---

**Qual a diferença prática entre LangChain e LangGraph?**

LangChain executa cadeias lineares — etapas em ordem fixa. LangGraph executa um grafo de estados com nós e arestas, inclusive condicionais e cíclicas. Em LangChain não dá pra retentar ou voltar a um nó anterior nativamente; em LangGraph é só uma aresta. LangChain é bom pra fluxos determinísticos curtos; LangGraph, pra agentes com decisão e estado.

**Por que não usaram só o AgentExecutor do LangChain?**

O AgentExecutor faz loop ReAct internamente, mas é caixa-preta — não dá controle granular sobre estado nem persistência. LangGraph é declarativo: você desenha o grafo, vê o fluxo, testa cada nó isoladamente, e plugga checkpointer sem reescrever nada.

**O StateGraph é igual a uma máquina de estados clássica?**

Não exatamente. Numa máquina de estados clássica os estados são entidades de primeira classe (S0, S1, S2). No StateGraph os "estados" são os nós (funções), e o estado em si é um dicionário tipado que flui entre eles. O grafo é determinístico estruturalmente, mas o estado é dinâmico. Fica mais próximo de um dataflow graph do que de um FSM.

**O que é um Reducer no LangGraph?**

É a estratégia de merge de um campo do estado quando dois nós escrevem nele. Por padrão sobrescreve. Mas dá pra anotar o campo com `Annotated[list, add_messages]` pra concatenar em vez de sobrescrever — útil pro histórico de mensagens.

---

**Por que classificaram por keywords em vez de LLM?**

Decisão consciente. A gente queria isolar o framework do classificador, pra mostrar que o grafo funciona independente da qualidade da detecção. Keywords dão resultado determinístico, latência sub-ms e zero custo — bom pra benchmark. A limitação é exatamente o que aparece no painel: precision baixa em frases ambíguas. O próximo passo é justamente trocar por LLM few-shot.

**Como o confidence é calculado?**

Heurística simples. Começa em 0,3 (fallback geral) e sobe pra `min(0,9, 0,5 + len(keywords) * 0,1)` quando bate em alguma keyword. É ingênuo de propósito — não é probabilidade real, é uma proxy. Numa versão LLM, viria do logprobs da saída estruturada.

**Por que persistir em JSON e não em SQLite?**

Pro protótipo, JSON era o menor denominador comum — qualquer ambiente roda sem dependência. LangGraph já oferece SqliteSaver, PostgresSaver e RedisSaver oficiais. A migração é trocar uma linha. A gente quis focar no grafo, não na infra.

**O grafo de vocês tem ciclos?**

Nessa versão não — todo handler vai direto pro END. Mas a estrutura suporta: era só fazer `add_edge("pedido", "detect_intent")` pra criar um loop. O ponto do painel é mostrar o framework, não usar todas as features. A próxima iteração com HITL teria ciclo.

**Como vocês validaram o grafo?**

Três níveis: testes manuais pela CLI durante o desenvolvimento; eval automatizado (o `evals.py` que aparece no painel) com 40 mensagens rotuladas; e inspeção visual do grafo compilado via `draw_mermaid_png`.

---

**40 amostras é pouco. Por que não mais?**

É pouco pra produção, suficiente pra prova de conceito do framework. Com 40 já dá pra ver tendência (matriz clara) e a classe-problema (geral). Pra produção, faríamos cross-validation com mil amostras estratificadas e CI nos números.

**Por que a precision de `geral` é tão baixa?**

Geral é a classe-fallback: tudo que não bate em nenhuma keyword cai nela. Aí recebe falsos positivos das outras duas classes. É estrutural da abordagem por keywords, não bug. Solução é classificador semântico.

**33 ms de latência é boa?**

Pra esse caso é excelente. Comparado a um classificador LLM via API (500–2000 ms), é 20 a 60 vezes mais rápido. O custo é a qualidade — que é o trade-off do painel.

**O recall de geral (0,92) é alto, mas a precision é baixa. Como interpretar?**

Geral "pesca" quase tudo que cai nela (recall alto), mas muito do que pesca não devia estar lá (precision baixa). Comportamento típico de fallback. A matriz mostra: pedido e suporte perdem amostras pra geral, mas geral não perde muito pras outras.

---

**Como evoluiriam isso pra produção?**

Quatro coisas: trocar o `detect_intent` por classificador LLM few-shot com saída estruturada via Pydantic; adicionar nó de Human-in-the-Loop pra casos com confidence baixo; migrar a persistência de JSON pra SqliteSaver; e instrumentar com LangSmith pra observabilidade.

**Quando não usar LangGraph?**

Três casos. Fluxo estritamente linear sem decisão — chain do LangChain resolve, mais simples. Single-shot prompt — chamada direta da API, LangGraph é over-engineering. E time sem familiaridade com Python e prazo curto — a curva tem custo, CrewAI ou Swarm podem ser mais ágeis pra MVP.

---

## Perguntas-bônus, se o professor for fundo

**Como vocês lidariam com concorrência se vários usuários invocarem o grafo ao mesmo tempo?**

O `session_id` separa contextos. O MemorySaver JSON não é thread-safe pra escrita concorrente — pra produção, SqliteSaver ou PostgresSaver resolvem com locks ou transações.

**O que é durable execution no LangGraph 1.x?**

Capacidade de o grafo retomar exatamente do ponto onde parou se o processo cair — porque o checkpointer salva snapshot a cada nó. Permite long-running agents (horas, dias) com tolerância a falha.

**Como implementariam streaming de resposta?**

LangGraph tem `graph.stream()` em vez de `graph.invoke()`. Itera sobre os steps do grafo conforme cada nó completa. Pra streaming token-a-token de um LLM dentro de um nó, usa `astream_events`.

---

## Dicas

Não tentar decorar resposta inteira — saber o núcleo conceitual é o que conta. Se não souber, ser honesto: "não testamos esse caso, mas a abordagem seria...". É bem melhor que inventar.
