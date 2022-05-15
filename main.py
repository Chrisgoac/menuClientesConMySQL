import mysql.connector as sql

# Configuración para conectar la base de datos.
db = sql.connect(
    host="localhost",
    user="admin",
    passwd="admin",
    database="test"
)

cursor = db.cursor()

# Borrar
# cursor.execute("DELETE FROM test")
# db.commit()

# AGREGAR VALOR:
# cursor.execute("INSERT INTO test VALUES (nombre, apellido, dni)")

# Guardar cambios
# db.commit()

# Seleccionar datos (Se puede añadir "WHERE (condicion)")
# cursor.execute("SELECT * FROM test")

# Ver el resultado de una selección
# r = cursor.fetchall()
# print(r)


def showClientes():
    cursor.execute("SELECT * FROM test")
    r = cursor.fetchall()

    for i in r:
        print(f"{i[0]} {i[1]} con DNI {i[2]}{getLetra(i[2])}.")


def showDNI(dni):
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    for i in r:
        print(f"Se ha encontrado al siguiente cliente: {i[0]} {i[1]} con DNI {i[2]}{getLetra(i[2])}.")
        return True
    return False


def getLetra(dni):
    resto = dni % 23
    if resto == 0:
        return "T"
    elif resto == 1:
        return "R"
    elif resto == 2:
        return "W"
    elif resto == 3:
        return "A"
    elif resto == 4:
        return "G"
    elif resto == 5:
        return "M"
    elif resto == 6:
        return "Y"
    elif resto == 7:
        return "F"
    elif resto == 8:
        return "P"
    elif resto == 9:
        return "D"
    elif resto == 10:
        return "X"
    elif resto == 11:
        return "B"
    elif resto == 12:
        return "N"
    elif resto == 13:
        return "J"
    elif resto == 14:
        return "Z"
    elif resto == 15:
        return "S"
    elif resto == 16:
        return "Q"
    elif resto == 17:
        return "V"
    elif resto == 18:
        return "H"
    elif resto == 19:
        return "L"
    elif resto == 20:
        return "C"
    elif resto == 21:
        return "K"
    elif resto == 22:
        return "E"
    else:
        print("Error, el número de DNi que has especificado no es correcto.")


def eraseDNI(dni):
    if comprobarDNI(dni):
        cursor.execute(f"DELETE FROM test WHERE DNI={dni}")
        db.commit()
        print("El cliente ha sido eliminado correctamente.")
    else:
        print(f"No existe un cliente con DNI: {dni}{getLetra(dni)}")

    # Método antiguo
    # cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    # r = cursor.fetchall()
    #
    # for i in r:
    #     if i[2] == dni:
    #         print(f"Se ha encontrado al siguiente cliente: {i[0]} {i[1]} con DNI {i[2]} y ha sido "
    #               f"eliminado correctamente.")
    #         # TODO Eliminar cliente
    #         return True
    # return False


def comprobarDNI(dni):
    # Comprobar si existe el DNI
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    for i in r:
        print(f"Existe un usuario con ese DNI: {i[0]} {i[1]}.")
        return True
    return False


def addCliente(nombre, apellido, dni):
    # Comprobar si existen los datos
    if not comprobarDNI(dni):
        # Agregar el usuario a la base de datos
        cursor.execute(f"INSERT INTO test VALUES ('{nombre}', '{apellido}', '{dni}')")
        db.commit()


def menuCliente():
    print("""
        \tMenu clientela
        1 - Agregar nuevo cliente.
        2 - Mostrar todos los clientes.
        3 - Mostrar ciente por DNI.
        4 - Eliminar ciente.
        5 - Salir.
        """)

    opcion = int(input("Elegir la opción a ejecutar: "))

    if opcion == 1:
        # Agregar cliente
        nombre = input("Nombre del cliente: ")
        apellido = input("Apellido del cliente: ")
        dni = int(input("DNI del cliente: "))

        addCliente(nombre, apellido, dni)
        menuCliente()
    elif opcion == 2:
        # Mostrar todos los clientes
        showClientes()
        menuCliente()
    elif opcion == 3:
        # Mostrar cliente por DNI
        dni = int(input("DNI del cliente: "))
        if not showDNI(dni):
            print(f"No se ha encontrado ningún cliente con DNI {dni}")
        menuCliente()
    elif opcion == 4:
        # Eliminar cliente
        dni = int(input("DNI del cliente que desea eliminar: "))
        eraseDNI(dni)
        menuCliente()
    elif opcion == 5:
        # Salir del programa
        print("Ha salido del programa correctamente.")
    else:
        # Opción incorrecta
        print("La opción no es correcta, por favor elige una opción válida.")
        menuCliente()


menuCliente()
