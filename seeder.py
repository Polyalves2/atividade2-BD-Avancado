import mysql.connector
from datetime import datetime
import random

# Configuração da conexão
config = {
    'host': 'localhost',
    'user': 'root',          # <--- MUDOU PARA root
    'password': '1234',  # <--- COLOQUE SUA SENHA
    'database': 'blog_system'
}

def seed_database():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("🌱 Iniciando população do banco de dados...")
        
        # Limpa as tabelas existentes
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE post_log")
        cursor.execute("TRUNCATE TABLE comments")
        cursor.execute("TRUNCATE TABLE posts")
        cursor.execute("TRUNCATE TABLE users")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Inserindo usuários
        users_data = [
            ('joao123', 'joao@email.com'),
            ('maria_silva', 'maria@email.com'),
            ('pedro_rocha', 'pedro@email.com'),
            ('ana_clara', 'ana@email.com'),
            ('carlos_m', 'carlos@email.com')
        ]
        
        print("📝 Inserindo usuários...")
        for username, email in users_data:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (username, email)
            )
        
        # Inserindo posts
        posts_data = [
            (1, 'Introdução ao Python', 'Python é uma linguagem versátil...'),
            (2, 'Banco de Dados SQL', 'Aprenda SQL do básico ao avançado...'),
            (1, 'Gatilhos em MySQL', 'Triggers são poderosos...'),
            (3, 'Desenvolvimento Web', 'Construindo sites modernos...'),
            (4, 'Data Science', 'Análise de dados com Python...'),
            (2, 'Machine Learning', 'Introdução ao ML...'),
            (5, 'Carreira em TI', 'Dicas para crescer na área...')
        ]
        
        print("📄 Inserindo posts...")
        for user_id, title, content in posts_data:
            cursor.execute(
                "INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)",
                (user_id, title, content)
            )
        
        # Verificando posts inseridos (para ver o log)
        cursor.execute("SELECT * FROM post_log")
        logs = cursor.fetchall()
        print(f"📋 Logs de criação de posts: {len(logs)} registros")
        
        # Inserindo comentários
        comments_data = [
            (1, 2, 'Ótimo post! Muito útil.'),
            (1, 3, 'Gostei da explicação.'),
            (1, 4, 'Poderia aprofundar mais?'),
            (2, 1, 'Excelente conteúdo!'),
            (2, 5, 'Me ajudou muito, obrigado!'),
            (2, 3, 'Quando terá continuação?'),
            (3, 2, 'Triggers são realmente úteis.'),
            (3, 4, 'Exemplo prático muito bom.'),
            (4, 1, 'Web development é demais!'),
            (4, 5, 'Parabéns pelo post.'),
            (5, 2, 'Data science é fascinante.'),
            (5, 3, 'Recomendo livros sobre o assunto.'),
            (6, 1, 'ML é o futuro!'),
            (7, 4, 'Ótimas dicas de carreira.')
        ]
        
        print("💬 Inserindo comentários...")
        for post_id, user_id, content in comments_data:
            cursor.execute(
                "INSERT INTO comments (post_id, user_id, content) VALUES (%s, %s, %s)",
                (post_id, user_id, content)
            )
        
        # Commit das alterações
        conn.commit()
        
        # Verificando resultados dos gatilhos
        print("\n🔍 Verificando resultados dos gatilhos:")
        
        # Verificando contagem de comentários
        cursor.execute("""
            SELECT p.id, p.title, p.comments_count, COUNT(c.id) as actual_comments
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            GROUP BY p.id
        """)
        
        results = cursor.fetchall()
        print("\n📊 Contagem de comentários por post:")
        print("-" * 60)
        for post_id, title, count_trigger, actual_count in results:
            status = "✅" if count_trigger == actual_count else "❌"
            print(f"{status} Post {post_id}: '{title[:30]}...'")
            print(f"   - Contador (trigger): {count_trigger}")
            print(f"   - Comentários reais: {actual_count}")
        
        # Verificando timestamps
        cursor.execute("""
            SELECT p.id, p.title, p.created_at, p.updated_at
            FROM posts p
            ORDER BY p.id
        """)
        
        timestamps = cursor.fetchall()
        print("\n⏰ Timestamps dos posts:")
        print("-" * 60)
        for post_id, title, created, updated in timestamps:
            print(f"Post {post_id}: '{title[:30]}...'")
            print(f"   - Criado: {created}")
            print(f"   - Atualizado: {updated}")
        
        print("\n✨ População concluída com sucesso!")
        
    except mysql.connector.Error as err:
        print(f"❌ Erro: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("🔒 Conexão fechada.")

def test_trigger_deletion():
    """Teste adicional: remover um comentário e verificar o gatilho de deleção"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("\n🧪 Testando gatilho de deleção...")
        
        # Verificar contagem antes da deleção
        cursor.execute("SELECT comments_count FROM posts WHERE id = 1")
        before = cursor.fetchone()[0]
        print(f"Comentários no post 1 antes da deleção: {before}")
        
        # Remover um comentário
        cursor.execute("DELETE FROM comments WHERE id = 1 LIMIT 1")
        conn.commit()
        
        # Verificar contagem depois da deleção
        cursor.execute("SELECT comments_count FROM posts WHERE id = 1")
        after = cursor.fetchone()[0]
        print(f"Comentários no post 1 depois da deleção: {after}")
        
        if after == before - 1:
            print("✅ Gatilho de deleção funcionou corretamente!")
        else:
            print("❌ Gatilho de deleção não funcionou como esperado")
            
    except mysql.connector.Error as err:
        print(f"❌ Erro no teste: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Executar população
    seed_database()
    
    # Executar teste de deleção
    test_trigger_deletion()