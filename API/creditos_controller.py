from db import get_db


def insertar(cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO creditos (cliente, monto, tasa_interes, plazo, fecha_otorgamiento) VALUES (?,?,?,?,?)"
    cursor.execute(statement, [cliente, monto, tasa_interes, plazo, fecha_otorgamiento])
    db.commit()
    return True

def editar(id, cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE creditos SET cliente = ?, monto = ?, tasa_interes = ?, plazo = ?, fecha_otorgamiento = ? WHERE id = ?"
    cursor.execute(statement, [cliente, monto, tasa_interes, plazo, fecha_otorgamiento, id])
    db.commit()
    return True

def eliminar(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM creditos WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True

def ver_credito(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM creditos WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

def obtener_creditos():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM creditos"
    cursor.execute(statement)
    return cursor.fetchall()
