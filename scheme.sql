-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS blog_system;
USE blog_system;

-- Tabela de usuários
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de posts
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    comments_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de comentários
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Gatilho 1: Atualiza updated_at do post quando recebe um novo comentário
DELIMITER $$
CREATE TRIGGER update_post_timestamp_on_comment
AFTER INSERT ON comments
FOR EACH ROW
BEGIN
    UPDATE posts 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.post_id;
END$$
DELIMITER ;

-- Gatilho 2: Incrementa contador de comentários no post
DELIMITER $$
CREATE TRIGGER increment_comments_count
AFTER INSERT ON comments
FOR EACH ROW
BEGIN
    UPDATE posts 
    SET comments_count = comments_count + 1 
    WHERE id = NEW.post_id;
END$$
DELIMITER ;

-- Gatilho 3: Decrementa contador de comentários quando um comentário é removido
DELIMITER $$
CREATE TRIGGER decrement_comments_count
AFTER DELETE ON comments
FOR EACH ROW
BEGIN
    UPDATE posts 
    SET comments_count = comments_count - 1 
    WHERE id = OLD.post_id;
END$$
DELIMITER ;

-- Gatilho 4: Log de inserção de posts (exemplo de trigger com INSERT)
CREATE TABLE post_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT,
    action VARCHAR(50),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER log_post_insert
AFTER INSERT ON posts
FOR EACH ROW
BEGIN
    INSERT INTO post_log (post_id, action) 
    VALUES (NEW.id, 'POST_CREATED');
END$$
DELIMITER ;