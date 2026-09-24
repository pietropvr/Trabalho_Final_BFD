-- Ativa o suporte a chaves estrangeiras no SQLite
PRAGMA foreign_keys = ON;

-- Apaga as tabelas antigas na ordem correta (filhos primeiro, depois pais)
DROP TABLE IF EXISTS registro_medico;
DROP TABLE IF EXISTS pet;
DROP TABLE IF EXISTS tutor;

-- Tabela TUTOR: Armazena os donos dos pets (com suporte a ambos os nomes de coluna de senha)
CREATE TABLE tutor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL, 
    senha TEXT, 
    senha_hash TEXT
);

-- Tabela PET: Armazena os animais, vinculados a um tutor
CREATE TABLE pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    raca TEXT,
    data_nascimento DATE,
    peso REAL,            
    microchip TEXT UNIQUE, 
    
    FOREIGN KEY (tutor_id) REFERENCES tutor(id) ON DELETE CASCADE
);

-- Tabela REGISTRO_MEDICO: Armazena o prontuário, vinculado a um pet
CREATE TABLE registro_medico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_registro DATE NOT NULL,
    data_retorno DATE,
    
    FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE
);