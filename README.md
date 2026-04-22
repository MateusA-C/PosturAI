# PosturAI - Monitoramento de Foco e Postura 👁️

Uma aplicação inteligente que monitora o foco, postura e cansaço do usuário em tempo real, utilizando visão computacional e inteligência artificial.

## 📋 Descrição

**PosturAI** é um sistema de monitoramento que utiliza a câmera do seu computador para detectar:
- **Cansaço**: Monitora o piscar dos olhos e fechamento dos olhos para detectar quando o usuário está cansado
- **Postura**: Detecta a posição da cabeça e alerta sobre possíveis problemas posturais
- **Foco**: Acompanha o nível de concentração e atenção durante o trabalho

A aplicação fornece notificações em tempo real para manter o usuário alertado sobre sua condição física durante o trabalho.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **CustomTkinter**: Interface gráfica moderna e responsiva
- **MediaPipe**: Detecção de face landmarks e postura
- **OpenCV (cv2)**: Processamento de vídeo em tempo real
- **SQLAlchemy**: ORM para gerenciamento de banco de dados
- **SQLite**: Banco de dados local
- **SciPy**: Cálculos de distância euclidiana
- **NumPy**: Operações com arrays
- **Pandas**: Análise e manipulação de dados
- **WinNotify**: Notificações do Windows

## 📁 Estrutura do Projeto

```
trabalho_1/
├── main.py                      # Arquivo principal - Controlador da aplicação
├── basededadosalchemy.py        # Gerenciador de banco de dados
├── criacao_db.py               # Definição dos modelos (Usuario, Registro)
├── criptografa.py              # Funções de criptografia de senhas
├── detecator_facial.py          # Detecção de pontos faciais com MediaPipe
├── detector_cansaco.py          # Detector de cansaço baseado em olhos
├── detector_olhos_e_boca.py     # Detector de características dos olhos e boca
├── Notificacao.py              # Sistema de notificações
├── posturai.db                 # Banco de dados SQLite
├── face_landmarker.task        # Modelo pré-treinado do MediaPipe
├── views/                       # Módulo com interfaces da aplicação
│   ├── login.py                # Tela de login
│   ├── cadastro.py             # Tela de cadastro
│   ├── principal.py            # Tela principal com monitoramento
│   ├── perfil.py               # Tela de perfil do usuário
│   └── dashboard.py            # Dashboard com estatísticas
├── PosturAI/                   # Pacote da aplicação
└── teste1.py                   # Arquivo de testes
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Webcam conectada
- Permissão de acesso à câmera

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install customtkinter
pip install mediapipe
pip install opencv-python
pip install sqlalchemy
pip install scipy
pip install numpy
pip install pandas
pip install winotify
pip install calendar
pip install sys
pip install bcrypt
pip install datetime
pip install numpy

```

### Execução

```bash
python main.py
```

## 📱 Funcionalidades Principais

### 1. **Autenticação de Usuário**
   - Cadastro de novo usuário
   - Login seguro com criptografia de senha
   - Gerenciamento de perfil

### 2. **Monitoramento em Tempo Real**
   - Detecção de landmarks faciais
   - Análise de cansaço através do piscar dos olhos
   - Avaliação de postura

### 3. **Notificações**
   - Alertas quando o usuário está cansado
   - Alertas de postura inadequada
   - Avisos de distração

### 4. **Dashboard**
   - Visualização de estatísticas de foco
   - Histórico de sessões
   - Relatórios de postura

### 5. **Perfil do Usuário**
   - Gerenciamento de informações pessoais
   - Ajustes de sensibilidade
   - Preferências de notificação

## 🔧 Componentes Principais

### `main.py`
Controlador principal da aplicação. Gerencia:
- Estado da aplicação
- Navegação entre telas
- Sessão do usuário
- Centralização de dados

### `DetectorCansaco`
Herda de `DetectorOlhosEBoca` e implementa:
- Detecção de piscar dos olhos
- Cálculo de EAR (Eye Aspect Ratio)
- Classificação de níveis de cansaço
- Armazenamento de dados no banco

### `DetectorFacial`
Utiliza MediaPipe para:
- Capturar vídeo da webcam
- Detectar 468 pontos faciais
- Desenhar landmarks em tempo real

### Banco de Dados
**Modelo Usuario**:
- id, nome, email, senha, profissao, idade, sexo

**Modelo Registro**:
- Armazena dados de cada sessão de monitoramento
- Relacionado com Usuario (Foreign Key)

## ⚙️ Configuração

### Calibração da Câmera
O sistema inclui calibração automática:
```python
self.FOCAL_LENGHT = 793  # Valor médio para webcams 720p
```

Ajuste conforme necessário para sua câmera.

## 🔐 Segurança

- Senhas são criptografadas no banco de dados
- Sessões de usuário gerenciadas em memória
- Banco de dados SQLite com validação

## 📊 Dados Coletados

- Timestamp das sessões
- Nível de cansaço
- Avaliação de postura
- Duração das sessões
- Métricas de foco

## 🐛 Solução de Problemas

**Problema**: Câmera não funciona
- Verifique as permissões de câmera do sistema
- Teste com outra aplicação
- Reinicie a aplicação

**Problema**: Detecção imprecisa
- Melhore a iluminação
- Posicione a câmera de frente
- Limpe a lente da câmera

**Problema**: Banco de dados corrompido
- Delete `posturai.db`
- A aplicação criará um novo banco automaticamente
  ## 📂 Download do Modelo

Para que a detecção facial funcione, você precisa baixar o arquivo do modelo `face_landmarker.task`.

1. Acesse a [Documentação do MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/index?hl=pt-br#models).
2. Na seção **Models**, escolha e baixe o modelo desejado.
3. Coloque o arquivo `.task` na pasta raiz do projeto (ou na pasta que você definiu no código).

## 📝 Licença

Este projeto é desenvolvido como trabalho acadêmico.

## 👥 Autores

Desenvolvido como projeto educacional em Python.

## 📞 Suporte

Para problemas ou sugestões, verifique os arquivos de configuração e logs da aplicação.

---

**Última atualização**: Abril de 2026
