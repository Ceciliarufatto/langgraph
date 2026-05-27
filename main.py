"""
Ponto de entrada principal do agente inteligente.
"""

import os
import uuid
import logging
from datetime import datetime
from dotenv import load_dotenv
from app.graph import build_graph
from app.memory import (
    load_memory,
    save_memory,
    clear_memory,
    list_checkpoints,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


def print_welcome():
    """Exibe mensagem de boas-vindas."""
    print("\n" + "=" * 70)
    print("🤖 Agente Inteligente com LangGraph")
    print("=" * 70)
    print("\nBem-vindo! Digite suas mensagens e o agente responderá.")
    print("\n📋 Comandos disponíveis:")
    print("  sair             - Encerrar a sessão")
    print("  limpar           - Limpar o histórico de conversa")
    print("  history          - Mostrar histórico da conversa")
    print("  checkpoints      - Listar checkpoints salvos")
    print("  help             - Mostrar este menu de ajuda")
    print("\n" + "-" * 70 + "\n")


def print_help():
    """Exibe menu de ajuda."""
    print("\n" + "=" * 70)
    print("📚 AJUDA - Comandos Disponíveis")
    print("=" * 70)
    print("""
    sair             Encerra a sessão atual
    limpar           Limpa o histórico de conversas
    history          Mostra todo o histórico da conversa
    checkpoints      Lista checkpoints salvos
    help             Mostra este menu de ajuda
""")
    print("=" * 70 + "\n")


def print_history(history):
    """Exibe o histórico da conversa."""
    if not history:
        print("\n📝 Histórico vazio\n")
        return
    
    print("\n" + "=" * 70)
    print("📜 Histórico da Conversa")
    print("=" * 70)
    
    for i, msg in enumerate(history, 1):
        if msg.startswith("user: "):
            print(f"\n{i//2 + 1}. 👤 {msg[6:]}")
        elif msg.startswith("assistant: "):
            print(f"   🤖 {msg[11:]}")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Função principal da aplicação."""
    print_welcome()
    
    session_id = str(uuid.uuid4())[:8]
    logger.info(f"Session started: {session_id}")
    
    graph = build_graph()
    
    history = load_memory(session_id)
    
    while True:
        try:
            user_input = input("👤 Você: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "sair":
                logger.info(f"Session ended by user: {session_id}")
                print("\n👋 Encerrando... Até logo!")
                break
            
            if user_input.lower() == "limpar":
                clear_memory(session_id)
                history = []
                print("✅ Histórico limpo!\n")
                logger.info(f"Memory cleared for session: {session_id}")
                continue
            
            if user_input.lower() == "history":
                print_history(history)
                continue
            
            if user_input.lower() == "checkpoints":
                checkpoints = list_checkpoints(session_id)
                if not checkpoints:
                    print("\n📌 Nenhum checkpoint salvo ainda\n")
                else:
                    print("\n📌 Checkpoints disponíveis:")
                    for cp in checkpoints:
                        print(f"   - {cp}")
                    print()
                continue
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            logger.info(f"Processing message for session {session_id}")
            
            result = graph.invoke({
                "message": user_input,
                "intent": "",
                "confidence": 0.0,
                "response": "",
                "history": history,
                "metadata": {"timestamp": datetime.now().isoformat()},
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            })
            
            response = result.get('response', 'Desculpe, não consegui processar sua mensagem')
            
            history = result.get('history', history)
            save_memory(session_id, history)
            
            print(f"🤖 Bot: {response}\n")
            
            logger.info(f"Response generated - Intent: {result.get('intent')}")
        
        except KeyboardInterrupt:
            logger.info(f"Session interrupted by user: {session_id}")
            print("\n\n👋 Sessão interrompida. Até logo!")
            break
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            print(f"❌ Erro ao processar mensagem: {e}")
            print("   Tente novamente ou digite 'sair' para encerrar\n")


if __name__ == "__main__":
    main()
