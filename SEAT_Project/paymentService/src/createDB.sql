
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(32) NOT NULL,
    cardId CHAR(16) NOT NULL,
    cvc CHAR(3) NOT NULL,
    Credito INTEGER,
   
   UNIQUE(username,cardId)
);