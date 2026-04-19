import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import calendar

class Dashboard:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.parent_frame = parent_frame

        self._configurar_grid()
        self._criar_sidebar()
        
        self.main_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        
        self.desenhar_conteudo()

    def _configurar_grid(self):
        self.parent_frame.grid_columnconfigure(1, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.parent_frame, width=200, corner_radius=0, fg_color="#1e293b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="PosturAI", font=("Helvetica", 20, "bold"), text_color="white").grid(row=0, column=0, padx=20, pady=30)
        self._criar_botao_menu("🏠 Início", "principal", 1)
        self._criar_botao_menu("📊 Dashboard", "dashboard", 2, ativo=True)
        self._criar_botao_menu("👤 Meu Perfil", "perfil", 3)
        
        self.sidebar.grid_rowconfigure(4, weight=1)
        ctk.CTkButton(self.sidebar, text="🚪 Sair", fg_color="#ef4444", command=lambda: self.controller.show_frame("login")).grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def _criar_botao_menu(self, texto, destino, linha, ativo=False):
        cor = "#334155" if ativo else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=texto, fg_color=cor, anchor="w", command=lambda: self.controller.show_frame(destino))
        btn.grid(row=linha, column=0, padx=20, pady=10, sticky="ew")

    def desenhar_conteudo(self):
        """Renderiza os KPIs e o gráfico de linha."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        content = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Análise Mensal de Postura", font=("Helvetica", 26, "bold"), text_color="#1f2937").pack(anchor="w", pady=(0, 20))

        # --- SEÇÃO DE CARDS (KPIs) ---
        self._renderizar_kpis(content)

        # --- SEÇÃO DO GRÁFICO ---
        self._renderizar_grafico_linha(content)

    def _renderizar_kpis(self, master):
        kpi_frame = ctk.CTkFrame(master, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=10)
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._criar_card_metrica(kpi_frame, "Tempo Total", "42h 15m", "#2563eb", 0)
        self._criar_card_metrica(kpi_frame, "Média Diária", "1h 24m", "#10b981", 1)
        self._criar_card_metrica(kpi_frame, "Total Alertas", "128", "#f59e0b", 2)

    def _criar_card_metrica(self, master, titulo, valor, cor, col):
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=12)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=titulo, font=("Helvetica", 12), text_color="gray").pack(pady=(10, 0))
        ctk.CTkLabel(card, text=valor, font=("Helvetica", 22, "bold"), text_color=cor).pack(pady=(0, 10))

    def _renderizar_grafico_linha(self, master):
        """
        Gera um gráfico de linha usando Matplotlib e o incorpora no CustomTkinter.
        """
        chart_card = ctk.CTkFrame(master, fg_color="white", corner_radius=15)
        chart_card.pack(fill="both", expand=True, pady=20)

        ctk.CTkLabel(chart_card, text="Evolução de Alertas por Dia", font=("Helvetica", 16, "bold"), text_color="#1f2937").pack(pady=15)

        # 💡 BACKEND TIP: Estes dados virão de um SELECT COUNT(*) GROUP BY dia_do_mes
        dias = list(range(1, 31))
        alertas = [5, 3, 8, 2, 5, 10, 15, 8, 4, 2, 1, 6, 8, 12, 5, 4, 3, 7, 9, 11, 4, 2, 5, 8, 6, 4, 3, 2, 1, 0]

        # Configuração do Gráfico Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor('white') # Fundo da figura
        ax.set_facecolor('#ffffff')      # Fundo do gráfico

        # Desenho da linha
        ax.plot(dias, alertas, color='#2563eb', marker='o', markersize=4, linewidth=2, label='Alertas')
        
        # Estilização dos eixos
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel("Dia do Mês", fontsize=10, color='gray')
        ax.set_ylabel("Qtd. Alertas", fontsize=10, color='gray')
        ax.tick_params(axis='both', colors='gray', labelsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Incorporando no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _criar_card_metrica(self, master, titulo, valor, cor_destaque, coluna):
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=12)
        card.grid(row=0, column=coluna, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=titulo, font=("Helvetica", 14), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=("Helvetica", 28, "bold"), text_color=cor_destaque).pack(pady=(5, 15))