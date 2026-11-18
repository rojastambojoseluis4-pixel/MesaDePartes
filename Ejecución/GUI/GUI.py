import os
import sys
from datetime import datetime
from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem

RUTA_GUI = os.path.dirname(os.path.abspath(__file__))
RUTA_RAIZ = os.path.abspath(os.path.join(RUTA_GUI, ".."))
if RUTA_RAIZ not in sys.path:
  sys.path.insert(0, RUTA_RAIZ)

from Clases.Expediente import Expediente
import Clases.ListasExpedientes as datos


def actualizar_tabla():
  ventana.tablaExpedientes.setRowCount(0)
  ventana.tablaExpedientes.setColumnCount(7)
  ventana.tablaExpedientes.setHorizontalHeaderLabels(
      ["Código", "Ciudadano", "DNI", "Teléfono", "Dirección", "Asunto", "Fecha"]
  )

  for i in range(datos.cantidad):
    ventana.tablaExpedientes.insertRow(i)
    ventana.tablaExpedientes.setItem(
        i, 0, QTableWidgetItem(str(datos.codigos[i]))
    )
    ventana.tablaExpedientes.setItem(
        i, 1, QTableWidgetItem(str(datos.ciudadanos[i]))
    )
    ventana.tablaExpedientes.setItem(i, 2, QTableWidgetItem(str(datos.dnis[i])))
    ventana.tablaExpedientes.setItem(
        i, 3, QTableWidgetItem(str(datos.telefonos[i]))
    )
    ventana.tablaExpedientes.setItem(
        i, 4, QTableWidgetItem(str(datos.direcciones[i]))
    )
    ventana.tablaExpedientes.setItem(
        i, 5, QTableWidgetItem(str(datos.asuntos[i]))
    )
    ventana.tablaExpedientes.setItem(
        i, 6, QTableWidgetItem(str(datos.fechas[i]))
    )


def limpiar_cajas():
  ventana.txtCodigo.clear()
  ventana.txtCiudadano.clear()
  ventana.txtDNI.clear()
  ventana.txtTelefono.clear()
  ventana.txtDireccin.clear()
  ventana.txtAsunto.clear()


def registrar():
  codigo = ventana.txtCodigo.text().strip().replace(",", "-")
  ciudadano = ventana.txtCiudadano.text().strip().replace(",", "-")
  dni = ventana.txtDNI.text().strip()
  telefono = ventana.txtTelefono.text().strip()
  direccion = ventana.txtDireccin.text().strip().replace(",", "-")
  asunto = ventana.txtAsunto.text().strip().replace(",", "-")

  if not codigo or datos.existe_valor(datos.codigos, codigo):
    QMessageBox.warning(ventana, "Error", "Código vacío o ya existente.")
    return
  if not ciudadano or datos.existe_valor(
      datos.ciudadanos, ciudadano, ignorar_mayusculas=True
  ):
    QMessageBox.warning(ventana, "Error", "Ciudadano vacío o ya registrado.")
    return
  if not (dni.isdigit() and len(dni) == 8) or datos.existe_valor(
      datos.dnis, dni
  ):
    QMessageBox.warning(
        ventana, "Error", "DNI inválido (8 dígitos) o ya registrado."
    )
    return
  if not (telefono.isdigit() and len(telefono) == 9) or datos.existe_valor(
      datos.telefonos, telefono
  ):
    QMessageBox.warning(
        ventana, "Error", "Teléfono inválido (9 dígitos) o ya registrado."
    )
    return
  if not direccion or not asunto:
    QMessageBox.warning(
        ventana, "Error", "Dirección y asunto no pueden estar vacíos."
    )
    return

  fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
  exp = Expediente(codigo, ciudadano, asunto, fecha, dni, telefono, direccion)

  idx = datos.cantidad
  datos.codigos[idx] = exp.codigo
  datos.ciudadanos[idx] = exp.ciudadano
  datos.asuntos[idx] = exp.asunto
  datos.fechas[idx] = exp.fecha
  datos.dnis[idx] = exp.dni
  datos.telefonos[idx] = exp.telefono
  datos.direcciones[idx] = exp.direccion
  datos.cantidad += 1

  datos.guardar_datos_en_archivo()
  actualizar_tabla()
  limpiar_cajas()
  QMessageBox.information(ventana, "Éxito", "Expediente registrado.")


def eliminar():
  fila = ventana.tablaExpedientes.currentRow()
  if fila >= 0:
    confirmar = QMessageBox.question(
        ventana,
        "Confirmar",
        "¿Está seguro de eliminar el expediente seleccionado?",
        QMessageBox.Yes | QMessageBox.No,
    )
    if confirmar == QMessageBox.Yes:
      datos.eliminar_expediente(fila)
      actualizar_tabla()
  else:
    QMessageBox.warning(
        ventana, "Aviso", "Seleccione una fila de la tabla primero."
    )


def ordenar():
  if datos.cantidad > 1:
    for i in range(datos.cantidad - 1):
      for j in range(i + 1, datos.cantidad):
        if datos.codigos[i] > datos.codigos[j]:
          datos.codigos[i], datos.codigos[j] = (
              datos.codigos[j],
              datos.codigos[i],
          )
          datos.ciudadanos[i], datos.ciudadanos[j] = (
              datos.ciudadanos[j],
              datos.ciudadanos[i],
          )
          datos.asuntos[i], datos.asuntos[j] = (
              datos.asuntos[j],
              datos.asuntos[i],
          )
          datos.fechas[i], datos.fechas[j] = datos.fechas[j], datos.fechas[i]
          datos.dnis[i], datos.dnis[j] = datos.dnis[j], datos.dnis[i]
          datos.telefonos[i], datos.telefonos[j] = (
              datos.telefonos[j],
              datos.telefonos[i],
          )
          datos.direcciones[i], datos.direcciones[j] = (
              datos.direcciones[j],
              datos.direcciones[i],
          )
    datos.guardar_datos_en_archivo()
    actualizar_tabla()
    QMessageBox.information(ventana, "Ordenado", "Expedientes ordenados.")
  else:
    QMessageBox.information(
        ventana, "Aviso", "No hay suficientes expedientes para ordenar."
    )


def buscar():
  criterio = ventana.txtBuscar.text().strip()
  if not criterio:
    actualizar_tabla()
    return
  ventana.tablaExpedientes.setRowCount(0)
  encontrados = 0
  for i in range(datos.cantidad):
    if datos.codigos[i] == criterio or datos.dnis[i] == criterio:
      ventana.tablaExpedientes.insertRow(encontrados)
      ventana.tablaExpedientes.setItem(
          encontrados, 0, QTableWidgetItem(str(datos.codigos[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 1, QTableWidgetItem(str(datos.ciudadanos[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 2, QTableWidgetItem(str(datos.dnis[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 3, QTableWidgetItem(str(datos.telefonos[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 4, QTableWidgetItem(str(datos.direcciones[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 5, QTableWidgetItem(str(datos.asuntos[i]))
      )
      ventana.tablaExpedientes.setItem(
          encontrados, 6, QTableWidgetItem(str(datos.fechas[i]))
      )
      encontrados += 1
  if encontrados == 0:
    QMessageBox.information(
        ventana, "Búsqueda", "No se encontró ningún expediente."
    )
    actualizar_tabla()


# --- INICIO DE LA APLICACIÓN (UNA SOLA VEZ) ---
app = QApplication(sys.argv)
loader = QUiLoader()

if getattr(sys, "frozen", False):
  carpeta_base = sys._MEIPASS
else:
  carpeta_base = os.path.dirname(os.path.abspath(__file__))

ruta_ui = os.path.join(carpeta_base, "ventana.ui")
ventana = loader.load(ruta_ui, None)

# Ajustar ancho del reloj para que no se corte
ventana.lblFechaHora.setFixedWidth(250)


def actualizar_reloj():
  ahora = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss")
  ventana.lblFechaHora.setText(f"Fecha y hora: {ahora}")


reloj = QTimer()
reloj.timeout.connect(actualizar_reloj)
reloj.start(1000)
actualizar_reloj()

datos.cargar_datos_desde_archivo()
actualizar_tabla()

ventana.btnRegistrar.clicked.connect(registrar)
ventana.btnEliminar.clicked.connect(eliminar)
ventana.btnOrdenar.clicked.connect(ordenar)
ventana.btnBuscar.clicked.connect(buscar)

ventana.show()
sys.exit(app.exec())
