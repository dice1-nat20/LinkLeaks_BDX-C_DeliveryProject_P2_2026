CREATE DATABASE IF NOT EXISTS fuite;
USE fuite;



CREATE TABLE IF NOT EXISTS utilisateur (
    utilisateur_id INT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    num_tel varchar(20),
    adress_mail varchar(100),
    IP varchar(100)
);



CREATE TABLE IF NOT EXISTS fuite (
    fuite_id INT PRIMARY KEY,
    fuite_latitude varchar(50),
    fuite_longitude varchar(50)
);


CREATE TABLE IF NOT EXISTS signaler (
	commentaire varchar(50),
    statut varchar(50),
    photo varchar(100),
    utilisateur_id int,
    fuite_id int,
    PRIMARY KEY (utilisateur_id, fuite_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(utilisateur_id),
    FOREIGN KEY (fuite_id) REFERENCES fuite(fuite_id)
);


