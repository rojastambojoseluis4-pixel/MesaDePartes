import os
from datetime import datetime


class Expediente:

  def __init__(
      self, codigo, ciudadano, asunto, fecha, dni, telefono, direccion
  ):
    self.codigo = codigo
    self.ciudadano = ciudadano
    self.asunto = asunto
    self.fecha = fecha
    self.dni = dni
    self.telefono = telefono
    self.direccion = direccion


MAX_EXPEDIENTES = 100
FILE_PATH = "expedientes_banos.txt"

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
          exp = Expediente(
              campos,
              campos,
              campos,
              campos,
              campos,
              campos,
              campos,
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
