

# =====================================================
# SISTEMA DE CONTROL ESCOLAR
# BASE DE DATOS NoSQL - TIPO CLAVE VALOR
# Python + PickleDB
# =====================================================

from pickledb import PickleDB

# =====================================================
# CONEXION CON LA BASE DE DATOS
# =====================================================

db = PickleDB("alumnos.json").load()


# =====================================================
# FUNCION PARA CAPTURAR LOS DATOS DEL ALUMNO
# =====================================================

def capturar_alumno():

    alumno = {
        "matricula": input("Matricula: ").strip(),
        "nombre": input("Nombre: ").strip(),
        "apellido": input("Apellido: ").strip(),
        "telefono": input("Telefono: ").strip(),
        "nombre_padre": input("Nombre del padre o tutor: ").strip(),
        "calle": input("Calle: ").strip(),
        "colonia": input("Colonia: ").strip(),
        "inscripcion": input("Pago de inscripcion ($): ").strip()
    }

    return alumno


# =====================================================
# FUNCION PARA MOSTRAR LOS DATOS DEL ALUMNO
# =====================================================

def mostrar_alumno(alumno):

    print("\n======================================")
    print("         INFORMACION DEL ALUMNO")
    print("======================================")

    print("Matricula:       ", alumno["matricula"])
    print("Nombre:          ", alumno["nombre"])
    print("Apellido:        ", alumno["apellido"])
    print("Telefono:        ", alumno["telefono"])
    print("Padre o tutor:   ", alumno["nombre_padre"])
    print("Calle:           ", alumno["calle"])
    print("Colonia:         ", alumno["colonia"])
    print("Inscripcion:     $", alumno.get("inscripcion", "No registrado"))

    print("======================================")


# =====================================================
# 1. ALTAS DE ALUMNOS
# =====================================================

def altas():

    print("\n========= ALTA DE ALUMNOS =========")

    alumno = capturar_alumno()

    matricula = alumno["matricula"]

    if matricula == "":
        print("\nERROR: La matricula es obligatoria.")
        return

    clave = "alumno:" + matricula

    if db.get(clave) is not None:

        print("\nERROR: El alumno ya esta registrado.")

    else:

        try:
            pago = float(alumno["inscripcion"])

            if pago < 0:
                print("ERROR: El pago no puede ser negativo.")
                return

            alumno["inscripcion"] = pago

        except ValueError:
            print("ERROR: Ingresa una cantidad numerica valida.")
            return

        db.set(clave, alumno)
        db.save()

        print("\nAlumno registrado correctamente.")


# =====================================================
# 2. BAJAS DE ALUMNOS
# =====================================================

def bajas():

    print("\n========= BAJA DE ALUMNOS =========")

    matricula = input("Ingresa la matricula: ").strip()

    clave = "alumno:" + matricula

    alumno = db.get(clave)

    if alumno is not None:

        mostrar_alumno(alumno)

        confirmar = input(
            "\n¿Deseas eliminar este alumno? (S/N): "
        ).strip().upper()

        if confirmar == "S":

            db.remove(clave)
            db.save()

            print("\nAlumno eliminado correctamente.")

        else:

            print("\nOperacion cancelada.")

    else:

        print("\nNo existe un alumno con esa matricula.")


# =====================================================
# 3. CONSULTA GENERAL DE ALUMNOS
# =====================================================

def consulta_general():

    print("\n========= CONSULTA GENERAL =========")

    claves = db.all()

    if len(claves) == 0:

        print("\nNo existen alumnos registrados.")
        return

    print("\nTotal de alumnos registrados:", len(claves))

    for clave in claves:

        alumno = db.get(clave)

        if alumno is not None:

            mostrar_alumno(alumno)


# =====================================================
# 4. CONSULTA POR MATRICULA
# =====================================================

def consulta_matricula():

    print("\n====== CONSULTA POR MATRICULA ======")

    matricula = input("Ingresa la matricula: ").strip()

    clave = "alumno:" + matricula

    alumno = db.get(clave)

    if alumno is not None:

        mostrar_alumno(alumno)

    else:

        print("\nAlumno no encontrado.")


# =====================================================
# 5. MODIFICACIONES DE ALUMNOS
# =====================================================

def modificaciones():

    print("\n========= MODIFICACION =========")

    matricula = input("Ingresa la matricula: ").strip()

    clave = "alumno:" + matricula

    alumno = db.get(clave)

    if alumno is None:

        print("\nNo existe un alumno con esa matricula.")
        return

    print("\nDatos actuales del alumno:")

    mostrar_alumno(alumno)

    print("\nIngresa los nuevos datos.")
    print("Presiona ENTER para conservar el dato actual.")

    campos = [
        "nombre",
        "apellido",
        "telefono",
        "nombre_padre",
        "calle",
        "colonia",
        "inscripcion"
    ]

    for campo in campos:

        nuevo = input(
            f"{campo} ({alumno.get(campo, 'No registrado')}): "
        ).strip()

        if nuevo != "":

            if campo == "inscripcion":

                try:
                    pago = float(nuevo)

                    if pago < 0:
                        print("El pago no puede ser negativo.")
                        continue

                    alumno[campo] = pago

                except ValueError:
                    print("Cantidad incorrecta. Se conserva el valor anterior.")

            else:

                alumno[campo] = nuevo

    db.set(clave, alumno)
    db.save()

    print("\nAlumno modificado correctamente.")

    mostrar_alumno(alumno)


# =====================================================
# MENU PRINCIPAL
# =====================================================

def menu():

    while True:

        print("\n")
        print("==========================================")
        print("          SISTEMA DE CONTROL ESCOLAR")
        print("==========================================")
        print("          BASE DE DATOS NoSQL")
        print("              CLAVE - VALOR")
        print("==========================================")
        print(" 1. ALTAS")
        print(" 2. BAJAS")
        print(" 3. CONSULTA GENERAL")
        print(" 4. CONSULTA POR MATRICULA")
        print(" 5. MODIFICACIONES")
        print(" 6. SALIR")
        print("==========================================")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":

            altas()

        elif opcion == "2":

            bajas()

        elif opcion == "3":

            consulta_general()

        elif opcion == "4":

            consulta_matricula()

        elif opcion == "5":

            modificaciones()

        elif opcion == "6":

            print("\n================================")
            print("Gracias por utilizar el sistema.")
            print("Base de datos guardada correctamente.")
            print("================================")

            break

        else:

            print("\nOpcion incorrecta. Intenta nuevamente.")


# =====================================================
# EJECUCION DEL PROGRAMA
# =====================================================

if __name__ == "__main__":

    menu()
