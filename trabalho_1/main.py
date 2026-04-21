import customtkinter as ctk
from views.login import Login
from views.cadastro import Cadastro
from views.principal import Principal
from views.perfil import Perfil
from views.dashboard import Dashboard
# 💡 BACKEND TIP: Importe seu gerenciador de banco aqui futuramente
# from models.database import DatabaseManager

class App(ctk.CTk):
    """
    Controlador Principal (Maestro): Gerencia o estado da aplicação, 
    a navegação entre telas e a sessão do usuário.
    """
    def __init__(self):
        super().__init__()

        self.usuario_logado_email = None

        # Configurações de Janela
        self.title("PosturAI - Monitoramento de Foco")
        self.geometry("1100x700")
        self.configure(fg_color="#f2f4f7")

        # 💡 BACKEND TIP (Sessão): 
        # Este atributo armazenará os dados do usuário logado (ex: ID, Nome).
        # Inicialmente None, será preenchido após a validação no Login.
        self.usuario_logado = None

        # 💡 BACKEND TIP (Persistência):
        # Instancie o banco de dados aqui para que todas as Views compartilhem 
        # a mesma conexão através do 'self.controller.db'.
        # self.db = DatabaseManager()

        self._preparar_container_principal()
        self._inicializar_navegação()

        # Inicia o fluxo na tela de acesso
        self.show_frame("login")

    def _preparar_container_principal(self):
        """Cria o frame pai onde todas as páginas serão 'empilhadas'."""
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        # Faz com que o grid ocupe todo o espaço do container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _inicializar_navegação(self):
        """Instancia todas as views e as organiza no dicionário de frames."""
        self.frames = {}
        self.paginas_objetos = {} # Criamos um dicionário novo para guardar os objetos (Perfil, Login, etc)

        # Lista de Views para registro automático
        paginas = (Login, Cadastro, Principal, Perfil, Dashboard)

        for PageClass in paginas:
            page_name = PageClass.__name__.lower()
            
            # Criamos um frame para cada página no grid (0,0)
            frame_pai = ctk.CTkFrame(self.container, fg_color="transparent")
            frame_pai.grid(row=0, column=0, sticky="nsew")
            
            # 💡 BACKEND TIP: Passamos 'self' (o App) como controller para que
            # as views possam acessar 'self.controller.usuario_logado'.
            self.frames[page_name] = frame_pai
            self.paginas_objetos[page_name] = PageClass(frame_pai, self)

    def show_frame(self, page_name):
        """
        Eleva a tela selecionada para o topo da pilha visual.
        💡 BACKEND TIP: Antes de dar o tkraise, você pode disparar funções de
        atualização (ex: se page_name == 'perfil', mande a tela recarregar os dados).
        """
        # Pega o objeto da página (ex: a instância da classe Perfil)
        pagina = self.paginas_objetos.get(page_name)
    
    # Se ele tiver o método atualizar, chama direto nele!
        if pagina and hasattr(pagina, "atualizar"):
            pagina.atualizar()

    # Depois mostra o frame visual correspondente
        frame = self.frames[page_name]
        frame.tkraise()

    # 💡 BACKEND TIP: Centralize funções de segurança aqui
    def realizar_logout(self):
        """Limpa a sessão e retorna ao login."""
        self.usuario_logado = None
        self.usuario_logado_email = None
        self.show_frame("login")

if __name__ == "__main__":
    app = App()
    app.mainloop()