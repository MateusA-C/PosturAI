import customtkinter as ctk

class Principal:
    """
    Tela principal do sistema. 
    Atua como o Dashboard onde o usuário inicia o monitoramento de postura.
    """
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.parent_frame = parent_frame

        self._configurar_layout_base()
        self._criar_sidebar()
        self._criar_conteudo_principal()

    def _configurar_layout_base(self):
        """Define a estrutura de grid responsiva para a janela principal."""
        self.parent_frame.grid_columnconfigure(1, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

    def _criar_sidebar(self):
        """Constrói o menu lateral de navegação."""
        self.sidebar = ctk.CTkFrame(self.parent_frame, width=200, corner_radius=0, fg_color="#1e293b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo
        ctk.CTkLabel(
            self.sidebar, text="PosturAI", 
            font=("Helvetica", 20, "bold"), text_color="white"
        ).grid(row=0, column=0, padx=20, pady=30)

        # --- BOTÕES DE NAVEGAÇÃO ---
        
        # Botão Início (Já selecionado por padrão nesta tela)
        self.btn_inicio = ctk.CTkButton(
            self.sidebar, text="🏠 Início", 
            fg_color="#334155", anchor="w", # Cor de destaque por ser a tela atual
            command=lambda: self.controller.show_frame("principal")
        )
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Botão Dashboard (Estatísticas de Tempo)
        self.btn_dash = ctk.CTkButton(
            self.sidebar, text="📊 Dashboard", 
            fg_color="transparent", anchor="w", hover_color="#334155",
            command=lambda: self.controller.show_frame("dashboard")
        )
        self.btn_dash.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Botão Perfil
        self.btn_perfil = ctk.CTkButton(
            self.sidebar, text="👤 Meu Perfil", 
            fg_color="transparent", anchor="w", hover_color="#334155",
            command=lambda: self.controller.show_frame("perfil")
        )
        self.btn_perfil.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Espaçador dinâmico para empurrar o botão Sair para o rodapé
        self.sidebar.grid_rowconfigure(4, weight=1) 

        # Botão Sair
        self.btn_sair = ctk.CTkButton(
            self.sidebar, text="🚪 Sair", 
            fg_color="#ef4444", hover_color="#dc2626",
            command=lambda: self.controller.show_frame("login")
        )
        self.btn_sair.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def _criar_conteudo_principal(self):
        """Renderiza a área de boas-vindas e o acionador do monitoramento."""
        self.content = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.lbl_welcome = ctk.CTkLabel(
            self.content, text="Bem-vindo ao PosturAI", 
            font=("Helvetica", 24, "bold"), text_color="#1f2937"
        )
        self.lbl_welcome.pack(pady=(100, 20))

        # Botão de Ação Principal
        self.btn_monitorar = ctk.CTkButton(
            self.content, text="🚀 Iniciar Monitoramento", 
            width=300, height=80, corner_radius=20,
            font=("Helvetica", 18, "bold"),
            fg_color="#2563eb", hover_color="#1d4ed8",
            command=self._iniciar_visao_computacional
        )
        self.btn_monitorar.pack(pady=20)

        self.lbl_status = ctk.CTkLabel(
            self.content, text="Câmera pronta para detecção", 
            text_color="gray"
        )
        self.lbl_status.pack()

    def _iniciar_visao_computacional(self):
        """
        Orquestra o motor de detecção sem persistência de imagem.
        💡 BACKEND TIP: 
        Como você armazenará apenas o tempo, ao encerrar o monitoramento, 
        o Backend deve calcular a duração total e salvar em uma tabela de 'Sessões'.
        """
        print("Sinalizando ao Backend: Abrindo stream de vídeo em memória...")
        self.lbl_status.configure(text="Monitoramento ATIVO", text_color="#10b981")
        
        # Exemplo de lógica de tempo:
        # self.inicio_sessao = datetime.now()