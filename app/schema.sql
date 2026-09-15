-- Ativa o suporte a chaves estrangeiras no SQLite
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS registro_medico;
DROP TABLE IF EXISTS pet;
DROP TABLE IF EXISTS tutor;

-- Tabela TUTOR: Armazena os donos dos pets
CREATE TABLE tutor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL, -- UNIQUE garante que não existam dois tutores com o mesmo email
    senha_hash TEXT NOT NULL    -- Senhas nunca devem ser salvas em texto plano
);

-- Tabela PET: Armazena os animais, vinculados a um tutor
CREATE TABLE pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,      -- Ex: Cão, Gato
    raca TEXT,
    data_nascimento DATE,
    peso_atual_kg REAL,
    numero_microchip TEXT UNIQUE, -- Opcional, UNIQUE garante que dois pets não tenham o mesmo chip
    -- Chave Estrangeira: Conecta o Pet ao seu Tutor correspondente
    FOREIGN KEY (tutor_id) REFERENCES tutor(id)
);

-- Tabela REGISTRO_MEDICO: Armazena o prontuário, vinculado a um pet
CREATE TABLE registro_medico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    tipo_registro TEXT NOT NULL, -- Ex: Vacina, Consulta, Vermífugo
    nome_evento TEXT NOT NULL,
    data_evento DATE NOT NULL,
    data_proxima_dose DATE,      -- Opcional, sem restrição NOT NULL
    nome_veterinario TEXT,
    observacoes TEXT,
    -- Chave Estrangeira: Conecta o prontuário ao respectivo Pet
    FOREIGN KEY (pet_id) REFERENCES pet(id)
);