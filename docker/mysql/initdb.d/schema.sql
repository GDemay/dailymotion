CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);


CREATE TABLE token (
    id INT NOT NULL AUTO_INCREMENT,
    id_user INT NOT NULL,
    expires_in DATETIME NOT NULL,
    token_code VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
