# 👁️ PosturAI - Monitor de Foco e Tempo de Tela

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Visão%20Computacional-green?style=for-the-badge&logo=opencv&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Banco%20de%20Dados-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white)

## 📌 Sobre o Projeto
O **PosturAI** é uma aplicação Desktop desenvolvida em Python para monitorar o tempo de tela e o foco dos usuários. Utilizando visão computacional através da webcam, o sistema detecta se o usuário está presente e focado, contabilizando o tempo real de produtividade e salvando o histórico de sessões em um banco de dados local.

## ✨ Funcionalidades
* **Cadastro de Usuários:** Interface moderna para registrar novos perfis com nome, idade, sexo, data de nascimento e profissão.
* **Monitoramento via Webcam:** Utiliza o modelo Haar Cascade do OpenCV para detecção facial. O cronômetro só avança enquanto o rosto do usuário é detectado.
* **Persistência de Dados:** Todo o histórico de sessões e tempo total de foco é salvo automaticamente usando SQLite, garantindo que os dados não sejam perdidos ao fechar o app.


## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Interface Gráfica (GUI):** CustomTkinter
* **Visão Computacional:** OpenCV (`cv2`)
* **Manipulação de Imagens:** Pillow (`PIL`)
* **Banco de Dados:** SQLite3 (Embutido)


## 🚀 Como Executar o Projeto (Modo Desenvolvedor)

Se você tem o Python instalado e deseja rodar o código-fonte diretamente (ideal para testar ou modificar o código):

1. Abra o terminal na pasta raiz do projeto.
2. Certifique-se de ter instalado as dependências (`pip install customtkinter opencv-python Pillow` e `pip install matplotlib`).
3. Inicie a aplicação com o comando:
   ```bash
   python main.py