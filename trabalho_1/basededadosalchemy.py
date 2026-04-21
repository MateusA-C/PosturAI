from criacao_db import session,Usuario,Registro
import pandas as pd
from sqlalchemy.exc import IntegrityError

class GerenciadorBanco:
    """
    Gerencia a conexão e as operações (CRUD) no banco de dados utilizando SQLAlchemy.
    Fornece métodos encapsulados para integrar o banco de dados com a Visão Computacional e o Frontend.
    """

    def __init__(self):
        """
        Inicializa a engine do banco de dados, cria as tabelas caso não existam
        e configura a fábrica de sessões.
        """
        self.session = session

    def inserir_usuario(self, nome, idade, profissao, email, senha,sexo):
        """
        Instancia um novo objeto Usuario e o insere no banco de dados.
        Retorna True em caso de sucesso ou False caso o login já exista.
        """
        try:
            novo_usuario = Usuario(
                nome=nome, 
                idade=idade, 
                profissao=profissao, 
                email=email, 
                senha=senha,
                sexo=sexo
            )
            self.session.add(novo_usuario)
            self.session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

    def autenticar_login(self, email_digitado):
        """
        Busca o usuário pelo login e valida a senha correspondente.
        Retorna a instância do Usuario em caso de sucesso ou False em caso de falha.
        """
        
        try:
            usuario = session.query(Usuario).filter_by(email=email_digitado).first()
            return usuario
        except:
            return False          
        

    def registrar_fadiga(self, usuario_id):
        """
        Grava um novo evento de fadiga no banco de dados, atrelando-o ao ID do usuário.
        Retorna True em caso de sucesso ou False em caso de erro.
        """
        
        try:
            novo_registro = Registro(usuario_id=usuario_id)
            self.session.add(novo_registro)
            self.session.commit()
            return novo_registro
        except Exception:
            self.session.rollback()
            return None

    def gerar_relatorio_completo(self):
        """
        Realiza uma consulta unindo as tabelas de usuários e registros.
        Retorna o histórico completo de detecções ordenado da mais recente para a mais antiga.
        """

        try:
            resultados = self.session.query(
                Usuario.nome,
                Registro.QAF,
                Registro.QAT
            ).join(Registro).order_by(Registro.data.desc()).all()
            return resultados
        
        except:
            return None


    def exportar_para_rh(self):
        """
        Extrai os dados do banco e gera arquivos de relatório (CSV e JSON) 
        formatados para o setor de RH.
        """
        
        try:
            query = self.session.query(
                Usuario.nome,
                Usuario.profissao,
                Registro.QAF.label('QAF'),
                Registro.data.label('momento')
            ).join(Registro).statement
            
            df = pd.read_sql(query, self.session.bind)
            
            df.to_csv("relatorio_rh.csv", index=False, sep=";", encoding="utf-8-sig")
            df.to_json("relatorio_rh.json", orient="records", indent=4, force_ascii=False)
            
        except:
            return None