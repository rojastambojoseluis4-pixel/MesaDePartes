import os
from Clases.ListasExpedientes import (
    cargar_datos_desde_archivo,
    registrar_expediente,
    buscar_expediente,
    ordenar_expedientes,
    mostrar_expedientes,
)


def main():
  cargar_datos_desde_archivo()
  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(":::SISTEMA DE MESA DE PARTES:::")
    print("1. Registrar expediente")
    print("2. Buscar expediente")
    print("3. Ordenar expedientes")
    print("4. Mostrar expedientes")
    print("0. Salir")
    opcion = input("Ingrese una opcion: ").strip()

    if opcion == "1":
      registrar_expediente()
    elif opcion == "2":
      buscar_expediente()
    elif opcion == "3":
      ordenar_expedientes()
    elif opcion == "4":
      mostrar_expedientes()
    elif opcion == "0":
      print("Saliendo del sistema...")
      break
    else:
      print("Opcion no valida. Intente nuevamente.")
      input("\nPresione Enter para continuar...")


if __name__ == "__main__":
  main()