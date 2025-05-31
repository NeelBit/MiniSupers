import tkinter as tk
from tkinter import ttk, messagebox

ventana = tk.Tk()
ventana.title('MiniSupers')
ventana.geometry('600x400')

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_productos = tk.Menu(barra_menu, tearoff=0)
menu_productos.add_command(label="Ver productos")

menu_info = tk.Menu(barra_menu, tearoff=0)
menu_info.add_command(label="Quiénes somos")

barra_menu.add_cascade(label="Productos", menu=menu_productos)
barra_menu.add_cascade(label="Quiénes somos", menu=menu_info)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

scroll = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

columnas = ('nombre', 'precio', 'seleccionado')
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scroll.set)

tabla.heading('nombre', text='Nombre')
tabla.heading('precio', text='Precio')
tabla.heading('seleccionado', text='✓')

tabla.column('nombre', width=200)
tabla.column('precio', width=100)
tabla.column('seleccionado', width=50, anchor='center')

tabla.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
scroll.config(command=tabla.yview)

boton_eliminar = tk.Button(ventana, text="Eliminar", bg="#ffdddd")
boton_eliminar.pack(pady=5)

frame_ingreso = tk.Frame(ventana)
frame_ingreso.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

tk.Label(frame_ingreso, text="Nombre:").grid(row=0, column=0, sticky="w", padx=(0, 5))
tk.Label(frame_ingreso, text="Precio:").grid(row=0, column=1, sticky="w", padx=(10, 5))

entrada_nombre = tk.Entry(frame_ingreso, width=25)
entrada_nombre.grid(row=1, column=0, padx=(0, 5))

entrada_precio = tk.Entry(frame_ingreso, width=15)
entrada_precio.grid(row=1, column=1, padx=(10, 5))

frame_ingreso.grid_columnconfigure(2, weight=1)

boton_agregar = tk.Button(frame_ingreso, text="Agregar", bg="#ddffdd")
boton_agregar.grid(row=1, column=2, padx=(20, 0), sticky="e")

ventana.mainloop()
