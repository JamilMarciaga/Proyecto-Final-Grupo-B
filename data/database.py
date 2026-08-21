import sqlite3

def get_connection():
    conn = sqlite3.connect('sistema.db')
    return conn

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (usuario, contraseña) 
        VALUES ('admin', '1234')
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos creada con usuario admin/1234.")