# 🛒 MiniSupers

Este proyecto está basado en el ejemplo de **Mini Proyecto** proporcionado en el PDF del INFO. A partir de este modelo inicial, se realizarán **modificaciones progresivas** para agregar funcionalidad y complejidad de forma gradual.

Elegimos este proyecto por ser accesible y didáctico, ideal para aprender paso a paso los fundamentos del desarrollo de interfaces gráficas y lógica en Python.

---

## 🚀 Objetivo

Desarrollar una aplicación de escritorio con Python y `tkinter` que simule un sistema de gestión de tareas (en versiones futuras, se adaptará al contexto de un minisuper).

---

## 📦 Código Base

El siguiente código fue la base brindada para iniciar el proyecto. Representa una pequeña app de "Lista de Tareas" utilizando `tkinter`.

```python
import tkinter as tk

# Ventana principal
ventana = tk.Tk()
ventana.title('Lista de tareas')
ventana.geometry('400x200')

# Campo de entrada
ingreso_tarea = tk.Entry(ventana)
ingreso_tarea.pack()

# Función para agregar tareas
def agregar_tarea():
    tarea = ingreso_tarea.get()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        ingreso_tarea.delete(0, tk.END)

boton_agregar = tk.Button(ventana, text='Agregar tarea', command=agregar_tarea)
boton_agregar.pack()

# Función para eliminar tareas seleccionadas
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        lista_tareas.delete(seleccion)

boton_eliminar = tk.Button(ventana, text='Eliminar tarea', command=eliminar_tarea)
boton_eliminar.pack()

# Lista de tareas
lista_tareas = tk.Listbox(ventana)
lista_tareas.pack()

# Ejecutar la aplicación
ventana.mainloop()
