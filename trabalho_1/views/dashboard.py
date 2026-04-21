import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import calendar
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import func # Importante para usar o SUM
from criacao_db import Usuario, Registro, session # Certifique-se dos nomes dos arquivos

class Dashboard:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.parent_frame = parent_frame
        self.session = session
        
        # Dados do banco
        self.total_fadiga = 0
        self.total_tela = 0

        # 1. Configuração de expansão do Grid
        self._configurar_grid_pai()
        
        # 2. Criar a Barra Lateral (O que tinha sumido)
        self._criar_sidebar()
        
        # 3. Container de Conteúdo (Coluna 1)
        self.main_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        
        self.desenhar_conteudo()

    def _configurar_grid_pai(self):
        """Define pesos para que a coluna do conteúdo (1) cresça mais que a sidebar (0)."""
        self.parent_frame.grid_columnconfigure(0, weight=0) # Sidebar fixa
        self.parent_frame.grid_columnconfigure(1, weight=1) # Conteúdo flexível
        self.parent_frame.grid_rowconfigure(0, weight=1)

    def _criar_sidebar(self):
        """Reconstrói a barra lateral de navegação."""
        self.sidebar = ctk.CTkFrame(self.parent_frame, width=200, corner_radius=0, fg_color="#1e293b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo/Título
        ctk.CTkLabel(self.sidebar, text="PosturAI", font=("Helvetica", 20, "bold"), text_color="white").grid(row=0, column=0, padx=20, pady=30)
        
        # Botões de Navegação
        self._criar_botao_menu("🏠 Início", "principal", 1)
        self._criar_botao_menu("📊 Dashboard", "dashboard", 2, ativo=True)
        self._criar_botao_menu("👤 Meu Perfil", "perfil", 3)
        
        # Botão Sair (no fundo)
        self.sidebar.grid_rowconfigure(4, weight=1)
        ctk.CTkButton(
            self.sidebar, text="🚪 Sair", fg_color="#ef4444", 
            command=self.controller.realizar_logout
        ).grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def _criar_botao_menu(self, texto, destino, linha, ativo=False):
        """Cria botões padronizados para a sidebar."""
        cor = "#334155" if ativo else "transparent"
        btn = ctk.CTkButton(
            self.sidebar, text=texto, fg_color=cor, anchor="w", 
            command=lambda: self.controller.show_frame(destino)
        )
        btn.grid(row=linha, column=0, padx=20, pady=10, sticky="ew")

    def atualizar(self):
        """Busca dados e redesenha os KPIs."""
        email_atual = self.controller.usuario_logado_email
        if email_atual:
            usuario = self.session.query(Usuario).filter_by(email=email_atual).first()
            if usuario:
                self.total_fadiga = self.session.query(func.sum(Registro.QAF)).filter_by(usuario_id=usuario.id).scalar() or 0
                self.total_tela = self.session.query(func.sum(Registro.QAT)).filter_by(usuario_id=usuario.id).scalar() or 0
                self.desenhar_conteudo()

    def desenhar_conteudo(self):
        """Renderiza os cards e o gráfico."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        content = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Análise Mensal de Postura", font=("Helvetica", 26, "bold"), text_color="#1f2937").pack(anchor="w", pady=(0, 20))

        # KPIs
        self._renderizar_kpis(content)

        # Gráfico
        self._renderizar_grafico_linha(content)

    def _renderizar_kpis(self, master):
        kpi_frame = ctk.CTkFrame(master, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=10)
        kpi_frame.grid_columnconfigure((0, 1), weight=1)

        self._criar_card_metrica(kpi_frame, "Alertas de Tela", str(self.total_tela), "#2563eb", 0)
        self._criar_card_metrica(kpi_frame, "Alertas de Fadiga", str(self.total_fadiga), "#f59e0b", 1)

    def _criar_card_metrica(self, master, titulo, valor, cor, col):
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=12)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=titulo, font=("Helvetica", 14), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=("Helvetica", 32, "bold"), text_color=cor).pack(pady=(5, 15))

    def _renderizar_grafico_linha(self, master):
        chart_card = ctk.CTkFrame(master, fg_color="white", corner_radius=15)
        chart_card.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(chart_card, text="Evolução de Alertas por Dia", font=("Helvetica", 16, "bold")).pack(pady=15)

        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        ax.plot(list(range(1, 31)), [0]*30, color='#2563eb', marker='o', markersize=3)
        ax.set_facecolor('#ffffff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)