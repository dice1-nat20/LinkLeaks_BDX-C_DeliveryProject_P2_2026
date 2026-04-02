CREATE DATABASE IF NOT EXISTS fuite;
USE fuite;



CREATE TABLE utilisateur (
    utilisateur_id int AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    num_tel varchar(20),
    email varchar(100) UNIQUE,
    IP varchar(100)
);



CREATE TABLE fuite (
    fuite_id INT AUTO_INCREMENT PRIMARY KEY,
    fuite_latitude decimal(9,6),
    fuite_longitude decimal(9,6)
);


CREATE TABLE signaler (
	id int AUTO_INCREMENT PRIMARY KEY,
	commentaire varchar(100),
    statut varchar(50),
    photo varchar(100),
    utilisateur_id int,
    fuite_id int,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(utilisateur_id),
    FOREIGN KEY (fuite_id) REFERENCES fuite(fuite_id)
);


