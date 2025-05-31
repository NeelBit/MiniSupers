import tkinter as tk
from tkinter import ttk, messagebox

# Creamos la ventanita
ventana = tk.Tk()
ventana.title('MiniSupers')
ventana.geometry('600x400')

# Esto es el menú de arriba
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_productos = tk.Menu(barra_menu, tearoff=0)
menu_productos.add_command(label="Ver productos")

menu_info = tk.Menu(barra_menu, tearoff=0)
menu_info.add_command(label="Quiénes somos")

barra_menu.add_cascade(label="Productos", menu=menu_productos)
barra_menu.add_cascade(label="Quiénes somos", menu=menu_info)

# Este es el lugar donde va la tabla que muestra los productos
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

# Barra para pueder bajar y ver mas cosas si hay muchas
scroll = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Con esto decimos que la tabla va a tener 4 columnas
columnas = ('producto', 'nombre', 'precio', 'seleccionado')
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scroll.set)

#Ponemos nombre a las columnas 
tabla.heading('producto', text='Producto')
tabla.heading('nombre', text='Nombre')
tabla.heading('precio', text='Precio')
tabla.heading('seleccionado', text='✓')

# Esto es para darle un tamaño a cada columna
tabla.column('producto', width=150)
tabla.column('nombre', width=150)
tabla.column('precio', width=100)
tabla.column('seleccionado', width=50, anchor='center')

tabla.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
scroll.config(command=tabla.yview)

# Este es el botón para eliminar productos (todavía no hace nada...)
boton_eliminar = tk.Button(ventana, text="Eliminar", bg="#ffdddd")
boton_eliminar.pack(pady=5)

# (Frame = Caja) Aquí va la parte de abajo donde escribís los datos
frame_ingreso = tk.Frame(ventana)
frame_ingreso.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)#(pack es el metodo que coloca la caja en la ventana)

# Estas son etiquetas de cada campo que hicimso
tk.Label(frame_ingreso, text="Producto:").grid(row=0, column=0, sticky="w", padx=(0, 5))
tk.Label(frame_ingreso, text="Nombre:").grid(row=0, column=1, sticky="w", padx=(10, 5))
tk.Label(frame_ingreso, text="Precio:").grid(row=0, column=2, sticky="w", padx=(10, 5))

# En esta parte creamos cajitas para escribir los datos que se van a ingersarr
entrada_producto = tk.Entry(frame_ingreso, width=20)
entrada_producto.grid(row=1, column=0, padx=(0, 5))

entrada_nombre = tk.Entry(frame_ingreso, width=20)
entrada_nombre.grid(row=1, column=1, padx=(10, 5))

entrada_precio = tk.Entry(frame_ingreso, width=15)
entrada_precio.grid(row=1, column=2, padx=(10, 5))

# Esto hace que la columna del botón no se expanda
frame_ingreso.grid_columnconfigure(3, weight=1)

# Este es un botón para agregar el producto (todavía no hace nada)
boton_agregar = tk.Button(frame_ingreso, text="Agregar", bg="#ddffdd")
boton_agregar.grid(row=1, column=3, padx=(20, 0), sticky="e")

# Mostramos la ventana
ventana.mainloop()
