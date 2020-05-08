DROP TABLE IF EXISTS Actas
DROP TABLE IF EXISTS Votos
DROP TABLE IF EXISTS Diputados
DROP TABLE IF EXISTS Bloques
DROP TABLE IF EXISTS Provincias

CREATE TABLE Actas (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    idActas INTEGER,
    fecha DATE,
    periodo INTEGER,
    reunion INTEGER,
    numeroActa,
    title TEXT,
    presidente TEXT /*idDiputado*/
    resolucion INTEGER /* 0 NEGATIVO 1 POSITIVO NONE NEUTRAL */
    urlActa TEXT,
    idUrl INTEGER
);
CREATE TABLE Votos (
    idVoto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE
    idActa INTEGER,
    voto INTEGER,
    numeroActa /* esto viene de la tabla actas */
    idDiputado INTEGER,
    descripcion TEXT
);

CREATE TABLE Diputados (
    idDiputado INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY UNIQUE,
    fullName TEXT,
    urlProfile TEXT,
    estado INTEGER,
    idBloque INTEGER,
    idProvincia INTEGER
);

CREATE TABLE Bloques (
    idBloque INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY UNIQUE,
    name
);

CREATE TABLE  Provincias (
    idProvincia INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY UNIQUE,
    name TEXT
);




