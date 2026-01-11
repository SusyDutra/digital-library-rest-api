-- SQL script to initialize the database schema for a library management system

CREATE TABLE IF NOT EXISTS author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT,
    nationality VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS book (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    pages INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id)
);

CREATE TABLE IF NOT EXISTS loan (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    fine_amount DECIMAL(10,2) DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (book_id) REFERENCES book(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE INDEX IF NOT EXISTS idx_book_author_id ON book(author_id);
CREATE INDEX IF NOT EXISTS idx_loan_book_id ON loan(book_id);
CREATE INDEX IF NOT EXISTS idx_loan_user_id ON loan(user_id);
CREATE INDEX IF NOT EXISTS idx_loan_status ON loan(status);

INSERT INTO author (name, biography, nationality) VALUES 
('Machado de Assis', 'Escritor brasileiro, considerado um dos maiores da literatura nacional', 'Brasileira'),
('Clarice Lispector', 'Escritora brasileira nascida na Ucrânia', 'Brasileira'),
('José Saramago', 'Escritor português, Prêmio Nobel de Literatura', 'Portuguesa'),
('Gabriel García Márquez', 'Escritor colombiano, mestre do realismo mágico', 'Colombiana'),
('George Orwell', 'Escritor britânico, autor de distopias clássicas', 'Britânica'),
('J.K. Rowling', 'Escritora britânica, criadora de Harry Potter', 'Britânica'),
('Stephen King', 'Escritor americano, mestre do terror', 'Americana'),
('Agatha Christie', 'Escritora britânica, rainha do crime', 'Britânica')
ON CONFLICT DO NOTHING;

INSERT INTO "user" (name, email) VALUES 
('João Silva', 'joao@email.com'),
('Maria Santos', 'maria@email.com'),
('Pedro Oliveira', 'pedro@email.com'),
('Ana Costa', 'ana@email.com'),
('Carlos Ferreira', 'carlos@email.com')
ON CONFLICT DO NOTHING;

INSERT INTO book (name, description, pages, author_id) VALUES 
('Dom Casmurro', 'Romance clássico da literatura brasileira', 256, 1),
('A Hora da Estrela', 'Romance sobre Macabéa', 87, 2),
('Memorial do Convento', 'Romance histórico sobre a construção do Convento de Mafra', 358, 3),
('Cem Anos de Solidão', 'Obra-prima do realismo mágico', 432, 4),
('1984', 'Distopia sobre totalitarismo e vigilância', 328, 5),
('Harry Potter e a Pedra Filosofal', 'Primeiro livro da saga do bruxinho', 223, 6),
('O Iluminado', 'Terror psicológico no Hotel Overlook', 447, 7),
('Assassinato no Expresso do Oriente', 'Mistério clássico de Hercule Poirot', 256, 8),
('Quincas Borba', 'Romance realista brasileiro', 312, 1),
('Água Viva', 'Narrativa experimental e poética', 96, 2),
('Ensaio sobre a Cegueira', 'Alegoria sobre a condição humana', 310, 3),
('O Amor nos Tempos do Cólera', 'Romance sobre amor e tempo', 368, 4),
('A Revolução dos Bichos', 'Fábula política sobre poder', 112, 5),
('Harry Potter e a Câmara Secreta', 'Segunda aventura de Harry Potter', 251, 6),
('Carrie', 'Primeiro romance publicado de Stephen King', 199, 7),
('Morte no Nilo', 'Mistério ambientado no Egito', 288, 8)
ON CONFLICT DO NOTHING;