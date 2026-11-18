import os
import sys
from datetime import datetime

from Clases.Expediente import Expediente

MAX_EXPEDIENTES = 100
if getattr(sys, "frozen", False):
  BASE_DIR = os.path.dirname(sys.executable)
else:
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "expedientes.txt")


codigos = [None] * MAX_EXPEDIENTES
ciudadanos = [None] * MAX_EXPEDIENTES
asuntos = [None] * MAX_EXPEDIENTES
fechas = [None] * MAX_EXPEDIENTES
dnis = [None] * MAX_EXPEDIENTES
telefonos = [None] * MAX_EXPEDIENTES
direcciones = [None] * MAX_EXPEDIENTES
cantidad = 0


def cargar_datos_desde_archivo():
  global cantidad
  if not os.path.exists(FILE_PATH):
    return
  try:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
      cantidad = 0
      for linea in f:
        linea = linea.strip()
        if not linea or cantidad >= MAX_EXPEDIENTES:
          continue
        campos = linea.split(",")
        if len(campos) == 7:
          cod, ciu, asu, fec, dni_val, tel, dir_val = campos
          exp = Expediente(
              cod,
              ciu,
              asu,
              fec,
              dni_val,
              tel,
              dir_val,
          )
          codigos[cantidad] = exp.codigo
          ciudadanos[cantidad] = exp.ciudadano
          asuntos[cantidad] = exp.asunto
          fechas[cantidad] = exp.fecha
          dnis[cantidad] = exp.dni
          telefonos[cantidad] = exp.telefono
          direcciones[cantidad] = exp.direccion
          cantidad += 1
  except Exception as e:
    print(f"Error al cargar archivo: {e}")


def guardar_datos_en_archivo():
  try:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
      for i in range(cantidad):
        f.write(
            f"{codigos[i]},{ciudadanos[i]},{asuntos[i]},{fechas[i]},"
            f"{dnis[i]},{telefonos[i]},{direcciones[i]}\n"
        )
  except Exception as e:
    print(f"Error al guardar archivo: {e}")


def existe_valor(arreglo, valor, ignorar_mayusculas=False):
  for i in range(cantidad):
    if arreglo[i] is not None:
      if ignorar_mayusculas:
        if arreglo[i].lower() == valor.lower():
          return True
      else:
        if arreglo[i] == valor:
          return True
  return False


def registrar_expediente():
  global cantidad
  os.system("cls" if os.name == "nt" else "clear")
  if cantidad >= MAX_EXPEDIENTES:
    print("Error: se alcanzo el limite de expedientes.")
    input("\nPresione Enter para continuar...")
    return

  while True:
    codigo = input("Ingrese el codigo del expediente: ").strip().replace(",", "-")
    if codigo == "":
      print("Error: el codigo no puede estar vacio.")
    elif existe_valor(codigos, codigo):
      print("Error: ese codigo ya existe. Ingrese otro.")
    else:
      break

  while True:
    ciudadano = (
        input("Ingrese el nombre del ciudadano: ").strip().replace(",", "-")
    )
    if ciudadano == "":
      print("Error: el nombre no puede estar vacio.")
    elif existe_valor(ciudadanos, ciudadano, ignorar_mayusculas=True):
      print("Error: ese ciudadano ya esta registrado. Ingrese otro.")
    else:
      break

  while True:
    dni = input("Ingrese el DNI: ").strip()
    if not (dni.isdigit() and len(dni) == 8):
      print("Error: el DNI debe tener exactamente 8 digitos numericos.")
    elif existe_valor(dnis, dni):
      print("Error: ese DNI ya esta registrado. Ingrese otro.")
    else:
      break

  while True:
    telefono = input("Ingrese el telefono : ").strip()
    if not (telefono.isdigit() and len(telefono) == 9):
      print("Error: el telefono debe tener exactamente 9 digitos numericos.")
    elif existe_valor(telefonos, telefono):
      print("Error: ese telefono ya esta registrado. Ingrese otro.")
    else:
      break

  while True:
    direccion = input("Ingrese la direccion: ").strip().replace(",", "-")
    if direccion != "":
      break
    print("Error: la direccion no puede estar vacia.")

  while True:
    asunto = input("Ingrese el asunto: ").strip().replace(",", "-")
    if asunto != "":
      break
    print("Error: el asunto no puede estar vacio.")

  fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
  exp = Expediente(
      codigo,
      ciudadano,
      asunto,
      fecha,
      dni,
      telefono,
      direccion,
  )

  codigos[cantidad] = exp.codigo
  ciudadanos[cantidad] = exp.ciudadano
  asuntos[cantidad] = exp.asunto
  fechas[cantidad] = exp.fecha
  dnis[cantidad] = exp.dni
  telefonos[cantidad] = exp.telefono
  direcciones[cantidad] = exp.direccion
  cantidad += 1

  guardar_datos_en_archivo()
  print("\nExpediente registrado correctamente.")
  input("\nPresione Enter para continuar...")
def gestionar_modificacion(idx):
  print("Asunto actual:", asuntos[idx])
  nuevo_asunto = (
      input("Ingrese el nuevo asunto (o presione Enter para cancelar): ")
      .strip()
      .replace(",", "-")
  )
  if nuevo_asunto != "":
    asuntos[idx] = nuevo_asunto
    guardar_datos_en_archivo()
    print("Asunto actualizado correctamente.")
  else:
    print("Modificacion cancelada.")


def eliminar_expediente(idx):
  global cantidad
  for i in range(idx, cantidad - 1):
    codigos[i] = codigos[i + 1]
    ciudadanos[i] = ciudadanos[i + 1]
    asuntos[i] = asuntos[i + 1]
    fechas[i] = fechas[i + 1]
    dnis[i] = dnis[i + 1]
    telefonos[i] = telefonos[i + 1]
    direcciones[i] = direcciones[i + 1]

  codigos[cantidad - 1] = None
  ciudadanos[cantidad - 1] = None
  asuntos[cantidad - 1] = None
  fechas[cantidad - 1] = None
  dnis[cantidad - 1] = None
  telefonos[cantidad - 1] = None
  direcciones[cantidad - 1] = None
  cantidad -= 1

  guardar_datos_en_archivo()
  print("Expediente eliminado.")


def buscar_binario_recursivo(izq, der, codigo_buscado):
  if izq > der:
    return -1
  medio = (izq + der) // 2
  if codigos[medio] == codigo_buscado:
    return medio
  elif codigos[medio] > codigo_buscado:
    return buscar_binario_recursivo(izq, medio - 1, codigo_buscado)
  else:
    return buscar_binario_recursivo(medio + 1, der, codigo_buscado)


def mostrar_detalle_y_opciones(idx):
  print("\n--------------------------")
  print("Codigo:", codigos[idx])
  print("Ciudadano:", ciudadanos[idx])
  print("DNI:", dnis[idx])
  print("Telefono:", telefonos[idx])
  print("Direccion:", direcciones[idx])
  print("Asunto:", asuntos[idx])
  print("Fecha:", fechas[idx])
  print("--------------------------")

  while True:
    print("\n1. Modificar asunto")
    print("2. Eliminar expediente")
    print("0. Regresar")
    op = input("Ingrese una opcion: ").strip()
    if op == "1":
      gestionar_modificacion(idx)
      break
    elif op == "2":
      confirmar = (
          input("Esta seguro de eliminar este expediente? (s/n): ")
          .strip()
          .lower()
      )
      if confirmar == "s":
        eliminar_expediente(idx)
      else:
        print("Eliminacion cancelada.")
      break
    elif op == "0":
      break
    else:
      print("Opcion no valida.")


def buscar_expediente():
  os.system("cls" if os.name == "nt" else "clear")
  if cantidad == 0:
    print("No hay expedientes registrados.")
    input("\nPresione Enter para continuar...")
    return

  print("::: BUSCAR EXPEDIENTE :::")
  print("1. Buscar por Codigo")
  print("2. Buscar por DNI")
  print("0. Regresar")
  tipo = input("Seleccione el metodo de busqueda: ").strip()

  if tipo == "1":
    if cantidad > 1:
      for i in range(cantidad - 1):
        for j in range(i + 1, cantidad):
          if codigos[i] > codigos[j]:
            codigos[i], codigos[j] = codigos[j], codigos[i]
            ciudadanos[i], ciudadanos[j] = ciudadanos[j], ciudadanos[i]
            asuntos[i], asuntos[j] = asuntos[j], asuntos[i]
            fechas[i], fechas[j] = fechas[j], fechas[i]
            dnis[i], dnis[j] = dnis[j], dnis[i]
            telefonos[i], telefonos[j] = telefonos[j], telefonos[i]
            direcciones[i], direcciones[j] = direcciones[j], direcciones[i]
      guardar_datos_en_archivo()

    codigo = input("Ingrese el codigo que desea buscar: ").strip()
    idx = buscar_binario_recursivo(0, cantidad - 1, codigo)
    if idx != -1:
      mostrar_detalle_y_opciones(idx)
    else:
      print("No se encontro el expediente.")

  elif tipo == "2":
    while True:
      dni_buscado = input("Ingrese el DNI que desea buscar (8 digitos): ").strip()
      if dni_buscado.isdigit() and len(dni_buscado) == 8:
        break
      print("Error: el DNI debe tener exactamente 8 digitos numericos.")

    idx_encontrado = -1
    for i in range(cantidad):
      if dnis[i] == dni_buscado:
        idx_encontrado = i
        break

    if idx_encontrado != -1:
      mostrar_detalle_y_opciones(idx_encontrado)
    else:
      print("No se encontro ningun expediente con ese DNI.")

  elif tipo == "0":
    return
  else:
    print("Opcion no valida.")

  input("\nPresione Enter para continuar...")


def ordenar_expedientes():
  os.system("cls" if os.name == "nt" else "clear")
  if cantidad > 1:
    for i in range(cantidad - 1):
      for j in range(i + 1, cantidad):
        if codigos[i] > codigos[j]:
          codigos[i], codigos[j] = codigos[j], codigos[i]
          ciudadanos[i], ciudadanos[j] = ciudadanos[j], ciudadanos[i]
          asuntos[i], asuntos[j] = asuntos[j], asuntos[i]
          fechas[i], fechas[j] = fechas[j], fechas[i]
          dnis[i], dnis[j] = dnis[j], dnis[i]
          telefonos[i], telefonos[j] = telefonos[j], telefonos[i]
          direcciones[i], direcciones[j] = direcciones[j], direcciones[i]
    guardar_datos_en_archivo()
    print("Expedientes ordenados por codigo.")
  else:
    print("No hay suficientes expedientes para ordenar.")
  input("\nPresione Enter para continuar...")


def conteo_recursivo_urgentes(n):
  if n <= 0:
    return 0
  actual_es_urgente = (
      1 if asuntos[n - 1] and "URGENTE" in str(asuntos[n - 1]).upper() else 0
  )
  return actual_es_urgente + conteo_recursivo_urgentes(n - 1)


def mostrar_expedientes():
  os.system("cls" if os.name == "nt" else "clear")
  if cantidad == 0:
    print("No hay expedientes registrados.")
  else:
    for i in range(cantidad):
      print("--------------------------")
      print(f"EXPEDIENTE {i + 1}")
      print("Codigo:", codigos[i])
      print("Ciudadano:", ciudadanos[i])
      print("Telefono:", telefonos[i])
      print("Direccion:", direcciones[i])
      print("Fecha:", fechas[i])
    print("--------------------------")
    print("Total marcados como URGENTE:", conteo_recursivo_urgentes(cantidad))
  input("\nPresione Enter para continuar...")
