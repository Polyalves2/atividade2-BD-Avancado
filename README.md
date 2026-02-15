# Sistema de Blog com MySQL
Projeto de um sistema simples de blog desenvolvido para demonstrar o uso de **gatilhos (triggers)** em MySQL. O sistema possui usuários, posts, comentários e utiliza gatilhos para automatizar tarefas como atualização de timestamps e contagem de comentários.

## 📋 Estrutura do Banco de Dados

### Tabelas

- **users** - Armazena os usuários do blog
  - `id`: Identificador único
  - `username`: Nome de usuário (único)
  - `email`: Email do usuário (único)
  - `created_at`: Data de criação
  - `updated_at`: Data da última atualização

- **posts** - Armazena as postagens do blog
  - `id`: Identificador único
  - `user_id`: ID do autor (chave estrangeira)
  - `title`: Título do post
  - `content`: Conteúdo do post
  - `created_at`: Data de criação
  - `updated_at`: Data da última atualização
  - `comments_count`: Contador de comentários (atualizado por trigger)

- **comments** - Armazena os comentários dos posts
  - `id`: Identificador único
  - `post_id`: ID do post comentado
  - `user_id`: ID do autor do comentário
  - `content`: Conteúdo do comentário
  - `created_at`: Data de criação
  - `updated_at`: Data da última atualização

- **post_log** - Registra eventos relacionados aos posts
  - `id`: Identificador único
  - `post_id`: ID do post
  - `action`: Ação realizada (ex: 'POST_CREATED')
  - `log_time`: Data e hora do log

## ⚡ Gatilhos (Triggers)

O sistema possui 4 gatilhos automatizados:

| Gatilho | Evento | Descrição |

|---------|--------|-----------|

| `update_post_timestamp_on_comment` | AFTER INSERT ON comments | Atualiza o `updated_at` do post quando recebe um novo comentário |

| `increment_comments_count` | AFTER INSERT ON comments | Incrementa o contador de comentários no post |

| `decrement_comments_count` | AFTER DELETE ON comments | Decrementa o contador de comentários quando um comentário é removido |

| `log_post_insert` | AFTER INSERT ON posts | Registra a criação de um novo post na tabela `post_log` |

## 🚀 Como executar o projeto

### Pré-requisitos

- MySQL Server 8.0+
- Python 3.9+
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**

git clone https://github.com/Polyalves2/atividade2-BD-Avancado.git

2. **Crie o banco de dados e os gatilhos**
   
mysql -u root -p 

3. **Instale o conector MySQL para Python**
   
pip install mysql-connector-python

4. **Configure a senha no seeder.py**

python
# No arquivo seeder.py, altere para sua senha do MySQL

config = {

    'host': 'localhost',
    
    'user': 'root',
    
    'password': 'SUA_SENHA_AQUI',
    
    'database': 'blog_system'
    
}

5. **Execute o script de população**
   
python seeder.py

📁 Estrutura de Arquivos

text

/

├── scheme.sql          # Script de criação do banco e gatilhos

├── seeder.py           # Script para popular o banco com dados de exemplo

├── README.md           # Documentação do projeto

└── mysql-reset.sql     # (opcional) Script para resetar senha do MySQL

🎯 Objetivo do Projeto

Este projeto foi desenvolvido para demonstrar:

Criação de gatilhos no MySQL

Automação de tarefas no banco de dados

Integração entre Python e MySQL

Boas práticas de modelagem de dados
