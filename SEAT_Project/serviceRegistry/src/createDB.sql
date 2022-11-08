
CREATE TABLE IF NOT EXISTS serviceRegistry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serviceName VARCHAR(32) NOT NULL,
    ip_Addr VARCHAR(12) NOT NULL,
    port CHAR (5) NOT NULL,
   
   UNIQUE(serviceName)
);