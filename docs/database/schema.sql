-- Tabela de Tutores
CREATE TABLE IF NOT EXISTS TUTOR (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL
);

-- Tabela de Pets
CREATE TABLE IF NOT EXISTS PET (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    raca TEXT,
    data_nascimento TEXT,
    peso_atual_kg REAL,
    FOREIGN KEY (tutor_id) REFERENCES TUTOR (id) ON DELETE CASCADE
);

-- Tabela de Registros Médicos
CREATE TABLE IF NOT EXISTS REGISTRO_MEDICO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    tipo_registro TEXT NOT NULL,
    nome_evento TEXT NOT NULL,
    data_evento TEXT NOT NULL,
    data_proxima_dose TEXT,
    nome_veterinario TEXT,
    observacoes TEXT,
    FOREIGN KEY (pet_id) REFERENCES PET (id) ON DELETE CASCADE
);