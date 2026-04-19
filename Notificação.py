from winotify import Notification, audio

class NotificacaoPosturAI:
    def __init__(self, app_id="PosturAI"):
            self.app_id = app_id
        # mensagem (titulo, remetente, conteúdo, imagem e duração)

    def enviar_alerta(self, titulo, mensagem, duracao = "long", som = audio.LoopingAlarm2, loop = True):
    
        notificacao = Notification(app_id=self.app_id, title = titulo, msg = mensagem, duration = duracao)

        # seleciona som de notificação

        notificacao.set_audio(som, loop = loop)

        notificacao.add_actions(label="AVISO", launch = "Está ACORDADO?")

        notificacao.show()

if __name__ == "__main__":
     notifier = NotificacaoPosturAI()

     notifier.enviar_alerta(
          titulo = "Lembrete de Postura",
          mensagem = "Postura Inadequada"

     )