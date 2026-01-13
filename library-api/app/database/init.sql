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
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
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

INSERT INTO "user" (name, email, hashed_password) VALUES 
('João Silva', 'joao@email.com', '$2b$12$hashedpassword1'),
('Maria Santos', 'maria@email.com', '$2b$12$hashedpassword2'),
('Pedro Oliveira', 'pedro@email.com', '$2b$12$hashedpassword3'),
('Ana Costa', 'ana@email.com', '$2b$12$hashedpassword4'),
('Carlos Ferreira', 'carlos@email.com', '$2b$12$hashedpassword5')
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

-- Sample loan data
INSERT INTO loan (book_id, user_id, loan_date, due_date, return_date, fine_amount, status) VALUES 
-- Active loans
(1, 1, '2024-01-15 10:00:00', '2024-02-15 23:59:59', NULL, 0.0, 'active'),
(3, 2, '2024-01-20 14:30:00', '2024-02-20 23:59:59', NULL, 0.0, 'active'),
(5, 3, '2024-01-25 09:15:00', '2024-02-25 23:59:59', NULL, 0.0, 'active'),

-- Overdue loans (not returned)
(7, 4, '2023-12-01 11:00:00', '2024-01-01 23:59:59', NULL, 0.0, 'active'),
(9, 5, '2023-11-15 16:45:00', '2023-12-15 23:59:59', NULL, 0.0, 'active'),

-- Loans returned on time
(2, 1, '2023-12-01 10:00:00', '2024-01-01 23:59:59', '2023-12-28 15:30:00', 0.0, 'returned'),
(4, 2, '2023-11-10 14:00:00', '2023-12-10 23:59:59', '2023-12-05 10:20:00', 0.0, 'returned'),
(6, 3, '2023-10-15 09:30:00', '2023-11-15 23:59:59', '2023-11-10 14:45:00', 0.0, 'returned'),

-- Loans returned late (with fine)
(8, 4, '2023-10-01 12:00:00', '2023-11-01 23:59:59', '2023-11-08 16:30:00', 14.0, 'returned'),
(10, 5, '2023-09-15 11:30:00', '2023-10-15 23:59:59', '2023-10-25 09:15:00', 20.0, 'returned'),

-- Additional loan history
(11, 1, '2023-08-01 10:15:00', '2023-09-01 23:59:59', '2023-08-28 14:20:00', 0.0, 'returned'),
(12, 2, '2023-07-10 15:45:00', '2023-08-10 23:59:59', '2023-08-15 11:30:00', 10.0, 'returned')
ON CONFLICT DO NOTHING;