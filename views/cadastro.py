import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class Cadastro:
    """
    Interface de Cadastro: Coleta e valida dados do usuário antes de 
    enviar para persistência no Banco de Dados.
    """
    def __init__(self, parent_frame, controller):
        self.controller = controller
        parent_frame.configure(fg_color="#f2f4f7")

        # Container Central (Card)
        # BACKEND TIP: Use um identificador único para o card se precisar 
        # referenciar temas dinâmicos vindos de uma tabela de configurações.
        self.card = ctk.CTkFrame(parent_frame, corner_radius=15, fg_color="white")
        self.card.pack(pady=50, padx=300, fill="both", expand=True)

        self._setup_ui()

    def _setup_ui(self):
        """Organiza a hierarquia visual dos elementos da interface."""
        # Título Principal
        ctk.CTkLabel(
            self.card, text="Cadastro de Usuário", 
            font=("Helvetica", 22, "bold"), text_color="#1f2937"
        ).pack(pady=(20, 10))

        # --- SEÇÃO: DADOS PESSOAIS ---
        self._render_section_label("Dados Pessoais")
        
        self.ent_nome = self._create_input("Nome Completo")
        
        self.ent_nascimento = self._create_input("Data de Nascimento (DD/MM/AAAA)")
        self.ent_nascimento.bind("<KeyRelease>", self.formatar_data)

        self.combo_sexo = ctk.CTkOptionMenu(
            self.card, values=["Masculino", "Feminino", "Prefiro não informar"]
        )
        self.combo_sexo.set("Selecione o Sexo")
        self.combo_sexo.pack(padx=30, pady=6, fill="x")

        # --- SEÇÃO: PROFISSÃO ---
        profissoes = ["Estudante", "Engenheiro", "Programador", "Médico", "Administrador", "Outro"]
        self.combo_profissao = ctk.CTkOptionMenu(
            self.card, values=profissoes, command=self.verificar_profissao
        )
        self.combo_profissao.set("Selecione a Profissão")
        self.combo_profissao.pack(padx=30, pady=6, fill="x")

        self.ent_profissao_outro = self._create_input("Qual a sua profissão?")
        self.ent_profissao_outro.pack_forget() # Inicia oculto

        # --- SEÇÃO: ACESSO ---
        self.lbl_acesso = self._render_section_label("Dados de Acesso")
        
        self.ent_email = self._create_input("E-mail")
        self.ent_senha = self._create_input("Senha", show_char="*")

        # --- BOTÕES DE AÇÃO ---
        self.btn_salvar = ctk.CTkButton(
            self.card, text="Finalizar Cadastro", height=45, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Helvetica", 14, "bold"),
            command=self.validar_e_salvar
        )
        self.btn_salvar.pack(pady=30, padx=30, fill="x")
    
        self.btn_ir_login = ctk.CTkButton(
            self.card, text="Já possui uma conta? Faça login",
            fg_color="transparent", text_color="#2563eb", hover=False,
            font=("Helvetica", 12, "underline"),
            command=lambda: self.controller.show_frame("login")
        )
        self.btn_ir_login.pack(pady=5)

    # --- MÉTODOS AUXILIARES DE UI ---

    def _create_input(self, placeholder, show_char=""):
        """Factory para padronização de campos de entrada."""
        entry = ctk.CTkEntry(self.card, placeholder_text=placeholder, height=40, show=show_char)
        entry.pack(padx=30, pady=6, fill="x")
        return entry

    def _render_section_label(self, text):
        label = ctk.CTkLabel(self.card, text=text, font=("Helvetica", 14, "bold"))
        label.pack(anchor="w", padx=30, pady=(15, 5))
        return label

    # --- LÓGICA DE NEGÓCIO / INTERAÇÃO ---

    def formatar_data(self, event=None):
        """Aplica máscara de data DD/MM/AAAA em tempo real."""
        if event and event.keysym in ['BackSpace', 'Delete', 'Left', 'Right']:
            return

        digits = "".join(filter(str.isdigit, self.ent_nascimento.get()))[:8]
        formatted = ""
        for i, char in enumerate(digits):
            if i in [2, 4]: formatted += "/"
            formatted += char

        if self.ent_nascimento.get() != formatted:
            self.ent_nascimento.delete(0, 'end')
            self.ent_nascimento.insert(0, formatted)

    def verificar_profissao(self, escolha):
        """Toggle dinâmico para o campo de profissão personalizada."""
        if escolha == "Outro":
            self.ent_profissao_outro.pack(padx=30, pady=6, fill="x", before=self.lbl_acesso)
        else:
            self.ent_profissao_outro.pack_forget()

    def calcular_idade(self, data_nasc_str):
        """Valida a cronologia da data e retorna a idade inteira."""
        try:
            data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
            hoje = datetime.now()

            if data_nasc > hoje:
                return "futuro"

            return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except ValueError:
            return None

    def validar_e_salvar(self):
        """
        Orquestra a validação da UI e a ponte para o serviço de Backend.
        """
        # Extração de dados
        # BACKEND TIP: Considere criar um objeto ou dicionário 'UserDTO' aqui
        # para passar todos os dados de uma vez para a função de salvar.
        nome = self.ent_nome.get().strip()
        data_nasc = self.ent_nascimento.get().strip()
        sexo = self.combo_sexo.get()
        email = self.ent_email.get().strip()
        senha = self.ent_senha.get()

        # Validações Básicas (Interface)
        if not all([nome, email, senha]):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
            return

        idade = self.calcular_idade(data_nasc)
        if not self._validar_regras_idade(idade):
            return

        # Lógica de Profissão
        profissao = self.combo_profissao.get()
        if profissao == "Outro":
            profissao = self.ent_profissao_outro.get().strip()
            if not profissao:
                messagebox.showwarning("Atenção", "Especifique sua profissão.")
                return

        # --- INTEGRAÇÃO COM BACKEND ---
        # BACKEND TIP 1: Aqui você chamaria algo como: 
        # resposta = self.controller.db.registrar_usuario(nome, email, senha, ...)
        
        # BACKEND TIP 2: Use blocos try/except aqui para capturar erros do banco 
        # (ex: Email já cadastrado) e exibir para o usuário sem travar o app.
        
        messagebox.showinfo("Sucesso", "Cadastro validado com sucesso!")
        self.controller.show_frame("principal")

    def _validar_regras_idade(self, idade):
        """Encapsula as regras de negócio relacionadas à idade."""
        if idade is None:
            messagebox.showerror("Erro", "Formato de data inválido!")
            return False
        if idade == "futuro":
            messagebox.showerror("Erro", "A data não pode ser no futuro!")
            return False
        if idade < 18:
            messagebox.showwarning("Acesso Negado", "Você precisa ter mais de 18 anos.")
            return False
        return True