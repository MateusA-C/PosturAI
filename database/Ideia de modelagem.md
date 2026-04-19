## 📊 Estrutura das Tabelas

### 1. Tabela: `usuarios`
Armazena os dados cadastrais e credenciais de acesso.

| Campo | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | Identificador único do usuário. |
| `nome` | TEXT | NOT NULL | Nome completo. |
| `nascimento` | DATE | - | Data de nascimento (ISO: YYYY-MM-DD). |
| `sexo` | TEXT | - | Gênero informado. |
| `profissao` | TEXT | - | Cargo ou ocupação. |
| `email` | TEXT | UNIQUE NOT NULL | E-mail usado para login. |
| `senha` | TEXT | NOT NULL | Hash da senha (Bcrypt/Argon2). |

### 2. Tabela: `sessoes`
Registra cada período de uso do monitoramento.

| Campo | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | Identificador da sessão. |
| `usuario_id` | INTEGER | FK (usuarios) | Dono da sessão. |
| `data` | DATE | DEFAULT CURRENT_DATE | Dia da realização. |
| `inicio` | DATETIME | NOT NULL | Timestamp de início do monitoramento. |
| `fim` | DATETIME | - | Timestamp de encerramento. |
| `duracao_seg` | INTEGER | - | Duração total calculada em segundos. |

### 3. Tabela: `alertas`
Logs de eventos de má postura detectados pela Visão Computacional.

| Campo | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | ID do alerta. |
| `sessao_id` | INTEGER | FK (sessoes) | Sessão vinculada. |
| `usuario_id` | INTEGER | FK (usuarios) | Usuário vinculado (atalho para busca). |
| `timestamp` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Momento exato do erro detectado. |
| `tipo` | TEXT | - | Ex: "Cabeça Baixa", "Ombro Desalinhado". |

