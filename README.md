# 🤖 Agente Inteligente com LangGraph

Protótipo de agente de atendimento inteligente desenvolvido utilizando **LangGraph** e **Python**, com orquestração baseada em grafos para simular um sistema de suporte ao cliente com múltiplos estados, decisões dinâmicas e persistência de contexto.

## 📋 Objetivo

Este projeto implementa um agente conversacional que:
- **Analisa a intenção** do usuário (pedido, suporte técnico, consulta geral)
- **Decide qual caminho seguir** através de um fluxo em grafo com decisões condicionais
- **Responde baseado no estado atual** mantendo estado interno e contexto
- **Salva e carrega contexto** da conversa para continuidade

## 🚀 Como Executar

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/Ceciliarufatto/langgraph.git
cd langgraph
```

### Passo 2: Criar ambiente virtual

```bash
python -m venv venv
```

### Passo 3: Ativar ambiente virtual

**No macOS/Linux:**
```bash
source venv/bin/activate
```

**No Windows:**
```bash
venv\Scripts\activate
```

### Passo 4: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 5: Executar o agente

```bash
python main.py
```

## 💬 Exemplos de Uso

```
👤 Você: Quero rastrear meu pedido
🤖 Bot: 🛒 Entendi que você quer informações sobre pedido...

👤 Você: Esqueci minha senha
🤖 Bot: 🆘 Entendo que você precisa de suporte técnico...

👤 Você: sair
👋 Encerrando... Até logo!
```

## 📊 Estrutura do Projeto

```
langgraph/
├── app/
│   ├── __init__.py              # Inicialização do módulo
│   ├── state.py                 # Definição do estado
│   ├── nodes.py                 # Nós do grafo
│   ├── graph.py                 # Construção do grafo
│   └── memory.py                # Persistência
├── main.py                       # Interface CLI
├── tests.py                      # Testes
├── requirements.txt              # Dependências
├── .env.example                  # Exemplo de env
└── README.md                     # Este arquivo
```

## 🔄 Fluxo de Funcionamento

1. **Usuário envia mensagem** → `main.py` invoca o grafo
2. **Detect Intent** → Analisa e classifica a intenção
3. **Route Intent** → Decide qual nó processar
4. **Handler específico** → Processa a solicitação
5. **Memory** → Salva contexto da conversa
6. **Resposta** → Enviada ao usuário

## 👥 Divisão de Responsabilidades

- **Cecilia Rufatto** - Pesquisa bibliográfica e implementação
- **Felipe Proença** - Desenvolvimento do fluxo em LangGraph
- **Leonardo Moino** - Implementação da persistência
- **Leonardo Quartaroli** - Desenvolvimento do fluxo
- **Lorena Scabello** - Documentação e apresentação

## 📚 Referências

1. [LangGraph Overview and Graph API](https://python.langchain.com/docs/langgraph/)
2. [LangGraph — Human in the Loop](https://python.langchain.com/docs/langgraph/how-tos/human-in-the-loop/)
3. [LangGraph Checkpointing and Persistence](https://python.langchain.com/docs/langgraph/concepts/persistence/)

---

**Desenvolvido com ❤️ por Cecilia Rufatto, Felipe Proença, Leonardo Moino, Leonardo Quartaroli e Lorena Scabello**
