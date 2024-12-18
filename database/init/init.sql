CREATE TABLE users (
    username VARCHAR2(50) PRIMARY KEY,
    password VARCHAR2(100) NOT NULL
);

CREATE TABLE videos (
    id NUMBER PRIMARY KEY,
    title VARCHAR2(100) NOT NULL,
    minio_location VARCHAR2(200) NOT NULL
);

INSERT INTO videos (id, title, minio_location) 
VALUES (1, 'Dogo Video', 'dogo.mp4');

INSERT INTO videos (id, title, minio_location) 
VALUES (2, 'Kitty Video', 'kitty.mp4');

INSERT INTO videos (id, title, minio_location) 
VALUES (3, 'Soso Video', 'soso.mp4');