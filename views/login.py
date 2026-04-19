import customtkinter as ctk
from tkinter import messagebox

class Login:
    def __init__(self, parent_frame, controller):
        self.controller = controller

        # Container central (CARD)
        self.card = ctk.CTkFrame(parent_frame, corner_radius=15, fg_color="white")
        self.card.pack(pady=60, padx=300, fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.card, text="Login PosturAI", font=("Helvetica", 24, "bold"), text_color="#1f2937").pack(pady=(40, 20))

        # Campos
        self.ent_email = ctk.CTkEntry(self.card, placeholder_text="E-mail", height=45)
        self.ent_email.pack(padx=40, pady=10, fill="x")

        self.ent_senha = ctk.CTkEntry(self.card, placeholder_text="Senha", show="*", height=45)
        self.ent_senha.pack(padx=40, pady=10, fill="x")

        # Botão Entrar
        self.btn_entrar = ctk.CTkButton(
            self.card, text="Entrar", height=45, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Helvetica", 14, "bold"),
            command=self.executar_login
        )
        self.btn_entrar.pack(pady=20, padx=40, fill="x")

        # Link para Cadastro
        self.btn_ir_cadastro = ctk.CTkButton(
            self.card, text="Não possui conta? Cadastre-se",
            fg_color="transparent", text_color="#2563eb", hover=False,
            font=("Helvetica", 12, "underline"),
            command=lambda: self.controller.show_frame("cadastro") # Comando para trocar de tela
        )
        self.btn_ir_cadastro.pack(pady=10)

    def executar_login(self):
        email = self.ent_email.get()
        senha = self.ent_senha.get()
        
        if email == "" or senha == "":
            messagebox.showwarning("Erro", "Preencha todos os campos!")
        self.controller.show_frame("principal")