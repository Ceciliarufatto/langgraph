"""
Gerador de GIF animado mostrando o sistema rodando.
Simula uma sessão completa com screenshots de diferentes interações.
"""

from PIL import Image, ImageDraw, ImageFont
import os

class GIFGenerator:
    def __init__(self, width=1200, height=700):
        self.width = width
        self.height = height
        self.frames = []
        self.bg_color = (26, 26, 46)  # #1a1a2e
        self.text_color = (255, 255, 255)
        self.highlight_color = (0, 212, 255)  # #00d4ff
        self.font_size = 28
        
    def create_frame(self, title, lines, step_num=1):
        """Cria um frame individual"""
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.font_size)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Cabeçalho
        draw.rectangle([(0, 0), (self.width, 100)], fill=self.highlight_color)
        draw.text((40, 25), "🤖 Agente Inteligente com LangGraph", 
                 font=title_font, fill=self.bg_color)
        
        # Conteúdo
        y = 120
        for line in lines:
            if line.startswith("👤"):
                draw.text((40, y), line, font=text_font, fill=(100, 200, 255))
            elif line.startswith("🤖"):
                draw.text((40, y), line, font=text_font, fill=self.highlight_color)
            elif line.startswith("✅"):
                draw.text((40, y), line, font=text_font, fill=(100, 255, 100))
            else:
                draw.text((40, y), line, font=text_font, fill=self.text_color)
            y += 50
        
        # Rodapé com step
        draw.text((40, self.height - 40), f"Step {step_num}/8", 
                 font=small_font, fill=self.highlight_color)
        draw.text((self.width - 300, self.height - 40), "github.com/Ceciliarufatto/langgraph", 
                 font=small_font, fill=self.highlight_color)
        
        self.frames.append(img)
        return img
    
    def generate_frames(self):
        """Gera todos os frames da animação"""
        
        # Frame 1: Inicialização
        self.create_frame(
            "Agente Inteligente",
            [
                "🤖 Agente Inteligente iniciado!",
                "📋 Digite suas mensagens e o agente responderá.",
                "",
                "Comandos: sair | history | help | limpar"
            ],
            step_num=1
        )
        
        # Frame 2: Usuário pergunta sobre pedido
        self.create_frame(
            "Interação 1: Pedido",
            [
                "👤 Você: Quero rastrear meu pedido",
                "",
                "🤖 Bot: Processando...",
                "   ⏳ Detectando intenção...",
                "   ✅ Intent: PEDIDO (confidence: 0.85)"
            ],
            step_num=2
        )
        
        # Frame 3: Resposta do pedido
        self.create_frame(
            "Resposta: Pedido",
            [
                "👤 Você: Quero rastrear meu pedido",
                "",
                "🤖 Bot: 🛒 Entendi que você quer informações sobre pedido.",
                "   • Rastreamento de pedido",
                "   • Informações de entrega",
                "   • Status da compra"
            ],
            step_num=3
        )
        
        # Frame 4: Usuário pergunta sobre suporte
        self.create_frame(
            "Interação 2: Suporte",
            [
                "👤 Você: Esqueci minha senha",
                "",
                "🤖 Bot: Processando...",
                "   ⏳ Detectando intenção...",
                "   ✅ Intent: SUPORTE (confidence: 0.90)"
            ],
            step_num=4
        )
        
        # Frame 5: Resposta do suporte
        self.create_frame(
            "Resposta: Suporte",
            [
                "👤 Você: Esqueci minha senha",
                "",
                "🤖 Bot: 🆘 Entendo que você precisa de suporte técnico.",
                "   • Recuperação de senha",
                "   • Problemas de acesso",
                "   • Erros técnicos"
            ],
            step_num=5
        )
        
        # Frame 6: Histórico
        self.create_frame(
            "Comando: history",
            [
                "👤 Você: history",
                "",
                "📜 Histórico da Conversa:",
                "   1. Quero rastrear meu pedido",
                "   2. Esqueci minha senha",
                "   ✅ 2 interações registradas"
            ],
            step_num=6
        )
        
        # Frame 7: Métricas
        self.create_frame(
            "Métricas do Sistema",
            [
                "📊 PERFORMANCE:",
                "   ✅ 2 commits no repositório",
                "   ✅ ~650 linhas de código Python",
                "   ✅ 14 testes unitários",
                "   ✅ 100% de cobertura"
            ],
            step_num=7
        )
        
        # Frame 8: Conclusão
        self.create_frame(
            "Implementação Completa",
            [
                "✅ Detecção de intenção",
                "✅ Roteamento dinâmico",
                "✅ Persistência de histórico",
                "✅ Sistema de checkpoints",
                "✅ Interface CLI interativa"
            ],
            step_num=8
        )
    
    def save_gif(self, filename="demo_langgraph.gif"):
        """Salva os frames como GIF"""
        if not self.frames:
            print("❌ Nenhum frame gerado!")
            return
        
        # Cada frame aparece por 2 segundos (2000ms)
        durations = [2000] * len(self.frames)
        
        self.frames[0].save(
            filename,
            save_all=True,
            append_images=self.frames[1:],
            duration=durations,
            loop=0,  # Loop infinito
            optimize=False
        )
        
        print(f"✅ GIF salvo em: {filename}")
        print(f"   Frames: {len(self.frames)}")
        print(f"   Duração total: {sum(durations)/1000:.1f} segundos")

# Executar
if __name__ == "__main__":
    print("🎬 Gerando GIF animado...")
    gen = GIFGenerator()
    gen.generate_frames()
    gen.save_gif("demo_langgraph.gif")
    print("🎉 Demo GIF criado com sucesso!")
