import hashlib as hl

import mysql.connector as sql

activeUser = 0

# Configuración para conectar la base de datos.
db = sql.connect(
    host="localhost",
    user="admin",
    passwd="admin",
    database="test"
)

cursor = db.cursor()


# Idea del proyecto
# Base de datos: Nombre, apellido, DNI, contraseña, dinero en el banco, efectivo.
# Menu admin:
# 1 - Agregar nuevo cliente.
#     - Nombre, apellido, DNI, contraseña, dinero en el banco, dinero en efectivo.
# 2 - Mostrar todos los clientes.
# 3 - Mostrar ciente por DNI.
# 4 - Eliminar cliente.
# 5 - Añadir dinero a cliente
#     - En el banco
#     - En efectivo
# 6 - Retirar dinero de un cliente
#     - En el banco
#     - En efectivo
# 7 - Cerrar sesión

# Menu user:
# 1 - Información de la cuenta.
#     - Nombre, apellido, DNI, contraseña, dinero en el banco, dinero en efectivo.
# 2 - Ingresar dinero.
#      - Propia cuenta.
#      - Otro cliente
# 3 - Retirar dinero
# 4 - Cambio de contraseña.
# 5 - Cerrar sesión.

# El usuario se identificará y se guardará una variable con active user | def para sacar/meter dinero y con ella la de un propio usuario

def adminRemoveMoney(efectivobanco, dni, money):
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    if efectivobanco == "efectivo":
        for i in r:
            actualMoney = i[5]
    elif efectivobanco == "banco":
        for i in r:
            actualMoney = i[4]
    else:
        print("ERROR (MENSAJE INTERNO): Se debe especificar efectivo o banco.")

    if actualMoney > money:
        newMoney = actualMoney - money
    cursor.execute(f"UPDATE test SET {efectivobanco} = {newMoney} WHERE DNI = {dni}")
    db.commit()


def showClientes():
    cursor.execute("SELECT * FROM test")
    r = cursor.fetchall()

    for i in r:
        print("------------------------------------------")
        print(f"{getClienteByDNI(i[2])}\nDinero en el banco: {i[4]} \nDinero en efectivo: {i[5]}")


def showDNI(dni):
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    for i in r:
        print("------------------------------------------")
        print(f"{getClienteByDNI(i[2])}\nDinero en el banco: {i[4]} \nDinero en efectivo: {i[5]}")
        print("------------------------------------------")
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
        return True
    else:
        return False


def getClienteByDNI(dni):
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    for i in r:
        return f"{i[0]} {i[1]} con DNI {dni}{getLetra(dni)}"


def comprobarDNI(dni):
    # Comprobar si existe el DNI
    cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
    r = cursor.fetchall()

    for i in r:
        return True
    return False


def addClienteNew(nombre, apellido, dni, password, cPassword, banco, efectivo):
    # Comprobar si existen los datos
    if not comprobarDNI(dni):
        # Agregar el usuario a la base de datos
        if password == cPassword:
            cursor.execute(
                f"INSERT INTO test VALUES ('{nombre}', '{apellido}', '{dni}', '{password}', '{banco}', '{efectivo}')")
            db.commit()
        else:
            print("ERROR: Las contraseñas no coinciden.")
    else:
        cursor.execute(f"SELECT * FROM test WHERE DNI = {dni}")
        r = cursor.fetchall()

        for i in r:
            print(f"Se ha encontrado al usuario: {getClienteByDNI(dni)}.")


def menuCliente():
    print("""
        \tMenu cliente
        1 - Información de la cuenta.
        2 - Ingresar dinero
        3 - Retirar dinero.
        4 - Cambio de contraseña
        5 - Cerrar sesión
        """)

    opcion = int(input("Elegir la opción a ejecutar: "))

    if opcion == 1:
        # INFO de la cuenta
        if not showDNI(activeUser):
            print(f"No se ha encontrado ningún cliente con DNI {activeUser}")
        menuCliente()
    elif opcion == 2:
        # Ingresar dinero
        menuCliente()
    elif opcion == 3:
        # Retirar dinero
        print("RETIRAR DINERO")
        menuCliente()
    elif opcion == 4:
        # Eliminar cliente
        dni = int(input("DNI del cliente que desea eliminar: "))
        if not eraseDNI(dni):
            print(f"No existe un cliente con DNI: {dni}{getLetra(dni)}")
        else:
            print("El cliente ha sido eliminado correctamente.")
        menuCliente()
    elif opcion == 5:
        # Remove money
        menuCliente()
    elif opcion == 6:
        # Add money
        menuCliente()
    elif opcion == 7:
        # Cerrar sesión
        print("Ha salido del programa correctamente.")
    else:
        # Opción incorrecta
        print("La opción no es correcta, por favor elige una opción válida.")
        menuCliente()


def menuAdmin():
    print("""
            \tMenu administrador
            1 - Agregar nuevo cliente.
            2 - Mostrar todos los clientes.
            3 - Mostrar ciente por DNI.
            4 - Eliminar ciente.
            5 - Add money
            6 - Remove money
            7 - Cerrar sesión.
            """)

    opcion = int(input("Elegir la opción a ejecutar: "))

    if opcion == 1:
        # Agregar cliente
        nombre = input("Nombre del cliente: ")
        apellido = input("Apellido del cliente: ")
        dni = int(input("DNI del cliente: "))

        passwd = hl.md5(input("Insertar la contraseña: ").encode("utf-8")).hexdigest()
        cPasswd = hl.md5(input("Repetir la contraseña: ").encode("utf-8")).hexdigest()

        banco = int(input("Dinero en el banco: "))
        efectivo = int(input("Dinero en efectivo: "))

        addClienteNew(nombre, apellido, dni, passwd, cPasswd, banco, efectivo)

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
        if not eraseDNI(dni):
            print(f"No existe un cliente con DNI: {dni}{getLetra(dni)}")
        else:
            print("El cliente ha sido eliminado correctamente.")
        menuCliente()
    elif opcion == 5:
        # Remove money
        menuCliente()
    elif opcion == 6:
        # Add money
        menuCliente()
    elif opcion == 7:
        # Cerrar sesión
        print("Ha salido del programa correctamente.")
    else:
        # Opción incorrecta
        print("La opción no es correcta, por favor elige una opción válida.")
        menuCliente()


def logIn():
    usuario = int(input("DNI para iniciar esión: "))
    if comprobarDNI(usuario):
        passwd = hl.md5(input("Contraseña: ").encode("utf-8")).hexdigest()
        cursor.execute(f"SELECT * FROM test WHERE DNI = {usuario}")
        r = cursor.fetchall()

        for i in r:
            if i[3] == passwd:
                print("Contraseña correcta.")
                global activeUser
                activeUser = usuario
                if usuario == 000:
                    menuAdmin()
                else:
                    menuCliente()
            else:
                print("Contraseá INCORRECTA")
                logIn()
    else:
        print("El usuario introducido no existe.")

logIn()

