import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from criacao_db import Usuario,session

class Perfil:
    """
    Componente visual para exibição e edição do perfil do usuário.
    Implementa o padrão State para alternar entre os modos de leitura e escrita.
    """
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.parent_frame = parent_frame
        self.session = session
        
        self.modo_edicao = False
        

        self.dados_usuario = {
            "nome": "", "nascimento": "", "sexo": "", 
            "profissao": "", "email": ""
        } 
        
        self.entradas_edicao = {}

        self._configurar_grid_principal()
        self._inicializar_sidebar()
        
        self.main_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        
        self.desenhar_conteudo()

    def atualizar(self):
        """Busca os dados do banco de dados toda vez que a tela é aberta."""
        email_atual = self.controller.usuario_logado_email
        
        if email_atual:
            # Busca o usuário (usando o .first() que corrigimos!)
            usuario_db = self.session.query(Usuario).filter_by(email=email_atual).first()
            
            if usuario_db:
                # Atualiza o dicionário com os dados reais
                self.dados_usuario = {
                    "nome": usuario_db.nome,
                    "nascimento": usuario_db.idade,
                    "sexo": usuario_db.sexo,
                    "profissao": usuario_db.profissao,
                    "email": usuario_db.email
                }
                # Redesenha a tela com os novos dados
                self.desenhar_conteudo()

    def _configurar_grid_principal(self):
        self.parent_frame.grid_columnconfigure(1, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

    def _inicializar_sidebar(self):
        """Constrói o menu lateral de navegação com a nova opção Dashboard."""
        self.sidebar = ctk.CTkFrame(self.parent_frame, width=200, corner_radius=0, fg_color="#1e293b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo
        ctk.CTkLabel(self.sidebar, text="PosturAI", font=("Helvetica", 20, "bold"), text_color="white").grid(row=0, column=0, padx=20, pady=30)
        
        # --- BOTÕES DE NAVEGAÇÃO ---
        # Botão Início
        ctk.CTkButton(self.sidebar, text="🏠 Início", fg_color="transparent", anchor="w",
                      command=lambda: self.controller.show_frame("principal")).grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # NOVO: Botão Dashboard
        ctk.CTkButton(self.sidebar, text="📊 Dashboard", fg_color="transparent", anchor="w",
                      command=lambda: self.controller.show_frame("dashboard")).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Botão Perfil (destacado por ser a tela atual)
        ctk.CTkButton(self.sidebar, text="👤 Meu Perfil", fg_color="#334155", anchor="w",
                      command=lambda: self.controller.show_frame("perfil")).grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Espaçador dinâmico
        self.sidebar.grid_rowconfigure(4, weight=1) 
        
        # Botão Sair
        ctk.CTkButton(self.sidebar, text="🚪 Sair", fg_color="#ef4444", 
                      command=lambda: self.controller.show_frame("login")).grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    # --- O restante dos métodos (desenhar_conteudo, renderizar_linha, etc.) permanece igual ---
    def desenhar_conteudo(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        self.content = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=30, pady=30)

        titulo = "Editar Perfil" if self.modo_edicao else "Meu Perfil"
        ctk.CTkLabel(self.content, text=titulo, font=("Helvetica", 26, "bold"), text_color="#1f2937").pack(anchor="w", pady=(0, 20))

        self._renderizar_secao_dados()
        self._renderizar_botoes_controle()

    def _renderizar_secao_dados(self):
        card = ctk.CTkFrame(self.content, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text="Informações do Usuário", font=("Helvetica", 16, "bold"), text_color="#2563eb").pack(anchor="w", padx=20, pady=(15, 10))
        self.renderizar_linha(card, "Nome:", "nome")
        self.renderizar_linha(card, "Nascimento:", "nascimento")
        self.renderizar_linha(card, "Sexo:", "sexo", tipo="combo", opcoes=["Masculino", "Feminino", "Outro"])
        self.renderizar_linha(card, "Profissão:", "profissao")
        self.renderizar_linha(card, "E-mail:", "email")

    def _renderizar_botoes_controle(self):
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.pack(pady=30)
        if not self.modo_edicao:
            ctk.CTkButton(btn_frame, text="✏️ Editar Informações", fg_color="#2563eb", width=200, height=40,
                          command=self.ativar_edicao).pack(side="left", padx=10)
        else:
            ctk.CTkButton(btn_frame, text="✅ Salvar Alterações", fg_color="green", hover_color="darkgreen", width=180, height=40,
                          command=self.salvar_alteracoes).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="❌ Cancelar", fg_color="gray", width=120, height=40,
                          command=self.cancelar_edicao).pack(side="left", padx=10)

    def renderizar_linha(self, master, label_text, chave_dado, tipo="entry", opcoes=None):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(frame, text=label_text, font=("Helvetica", 13, "bold"), text_color="gray", width=120, anchor="w").pack(side="left")
        if self.modo_edicao:
            self._criar_widget_edicao(frame, tipo, chave_dado, opcoes)
        else:
            ctk.CTkLabel(frame, text=self.dados_usuario[chave_dado], font=("Helvetica", 13), text_color="#1f2937").pack(side="left", padx=10)

    def _criar_widget_edicao(self, frame, tipo, chave_dado, opcoes):
        if tipo == "combo":
            widget = ctk.CTkOptionMenu(frame, values=opcoes, width=250)
            widget.set(self.dados_usuario[chave_dado])
        else:
            widget = ctk.CTkEntry(frame, width=250)
            widget.insert(0, self.dados_usuario[chave_dado])
        widget.pack(side="left", padx=10)
        self.entradas_edicao[chave_dado] = widget

    def ativar_edicao(self):
        self.modo_edicao = True
        self.desenhar_conteudo()

    def cancelar_edicao(self):
        self.modo_edicao = False
        self.entradas_edicao.clear()
        self.desenhar_conteudo()

    def salvar_alteracoes(self):
        novos_dados = {}
        for chave in self.dados_usuario.keys():
            if chave in self.entradas_edicao:
                novos_dados[chave] = self.entradas_edicao[chave].get()
        self.dados_usuario.update(novos_dados)
        self.modo_edicao = False
        self.entradas_edicao.clear()
        self.desenhar_conteudo()
        messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")