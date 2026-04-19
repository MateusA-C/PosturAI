import threading
import plyer


class AlertaErgonomico:

    def __init__(self):

        self.alerta_ativo  = False

    def _executar_notificacao(self,titulo,mensagem):

        plyer.notification.notify(
            title = titulo,
            message = mensagem,
            app_name = 'ErgiShield',
            timeout=5
        )
        self.alerta_ativo = False

    def emitir(self,titulo,mensagem):

        if not self.alerta_ativo:

            self.alerta_ativo = True
            threading.Thread(target=self._executar_notificacao,args=(titulo,mensagem)).start()


if __name__ == '__main__':
    
    meu_notificador = AlertaErgonomico()
    meu_notificador.emitir("TESTE","Esse é o meu primeiro teste, tentando emitir um alerta pelo plyer")