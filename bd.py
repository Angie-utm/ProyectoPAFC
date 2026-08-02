import mysql.connector

def iniciar_bd():
    # Conexión con la base de datos MySQL
    db = mysql.connector.connect(
        host="localhost",
        port=3306,  # El puerto que estás utilizando
        user="root",
        password="",
        database="rentas"
    )
    
    return db

# Función para realizar una consulta
def obtener_datos():
    db = iniciar_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")  # Aquí puedes hacer cualquier consulta
    datos = cursor.fetchall()
    cursor.close()
    db.close()
    return datos

# Ejemplo de uso
if __name__ == "__main__":
    datos = obtener_datos()
    for usuario in datos:
        print(usuario)
