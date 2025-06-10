import tkinter as tk
from tkinter import ttk, messagebox

# Lista para guardar los productos
lista_productos = [
    {"producto": "Leche", "nombre": "La Serenísima", "precio": "1200"},
    {"producto": "Pan", "nombre": "Baguette", "precio": "800"},
    {"producto": "Queso", "nombre": "Cremoso", "precio": "2500"},
]
contador_id = [1]  # Usamos una lista para que sea mutable dentro de la función

# Creamos la ventanita
ventana = tk.Tk()
ventana.title('MiniSupers')
ventana.geometry('600x450')

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

# Sincroniza la lista de productos con la tabla al iniciar
for prod in lista_productos:
    # Si no tiene id, asígnale uno
    if "id" not in prod:
        prod["id"] = contador_id[0]
        contador_id[0] += 1
    tabla.insert(
        "",
        tk.END,
        iid=str(prod["id"]),
        values=(prod["producto"], prod["nombre"], prod["precio"], "")
    )

# Permitir selección múltiple en la tabla: La selección multiple presionando Ctrl o Shift
tabla.config(selectmode="extended")

def sincronizar_checks(event=None):
    """
    Sincroniza la columna 'seleccionado' (check) de la tabla con la selección actual del usuario.
    Marca con '✓' la columna 'seleccionado' de las filas seleccionadas y la desmarca en las no seleccionadas.
    Se ejecuta automáticamente cada vez que cambia la selección de la tabla.
    """

    # Obtiene el conjunto de IDs de los elementos actualmente seleccionados en la tabla
    seleccionados = set(tabla.selection())

    # Recorre todos los elementos (filas) de la tabla
    for item in tabla.get_children():

        # Obtiene los valores actuales de la fila como una lista
        valores = list(tabla.item(item, "values"))

        # Si el item está seleccionado, pone el check (✓) en la columna 'seleccionado'
        if item in seleccionados:
            valores[3] = "✓"
        else:
            # Si no está seleccionado, deja la columna 'seleccionado' vacía
            valores[3] = ""
        
        # Actualiza los valores de la fila en la tabla
        tabla.item(item, values=valores)

# Defino la función carga nuevo producto
def carga_nuevo_producto():
    producto = entrada_producto.get().strip()
    nombre = entrada_nombre.get().strip()
    precio = entrada_precio.get().strip()

    if not producto or not nombre or not precio:
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
        return
    try:
        float(precio)
    except ValueError:
        messagebox.showwarning("Precio inválido", "El precio debe ser un número.")
        return

    id_producto = contador_id[0]
    contador_id[0] += 1

    # Guardar en la lista
    nuevo = {
        "id": id_producto,
        "producto": producto,
        "nombre": nombre,
        "precio": precio,
        "seleccionado": False
    }
    lista_productos.append(nuevo)

    # Insertar en la tabla
    tabla.insert(
        "",
        tk.END,
        iid=str(id_producto),  # Usamos el id como iid
        values=(producto, nombre, precio, "")
    )

    # Limpiar entradas
    entrada_producto.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)

# Cambia el estado de seleccionado en la lista y en la tabla
def alternar_check(event):
    item_id = tabla.identify_row(event.y)
    col = tabla.identify_column(event.x)
    if not item_id or col != '#4':
        return
    valores = list(tabla.item(item_id, "values"))
    seleccionado = valores[3] == "✓"
    valores[3] = "" if seleccionado else "✓"
    tabla.item(item_id, values=valores)
    # Actualiza en la lista
    for prod in lista_productos:
        if str(prod["id"]) == item_id:
            prod["seleccionado"] = not seleccionado
            break

tabla.bind("<Double-1>", alternar_check)

# Vincula la selección de la tabla con la función de sincronización
tabla.bind("<<TreeviewSelect>>", sincronizar_checks)

# Ponemos nombre a las columnas 
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

#Definimos la función eliminar seleccionados
def eliminar_seleccionados():
    seleccionados = tabla.selection()
    if not seleccionados:
        messagebox.showinfo("Eliminar", "No hay productos seleccionados.")
        return
    mensaje = messagebox.askquestion('Advertencia', "¿Está seguro que quiere eliminar los productos seleccionados?")
    if mensaje == "yes":
        for item_id in seleccionados:
            tabla.delete(item_id)
            # Elimina de la lista
            lista_productos[:] = [prod for prod in lista_productos if str(prod["id"]) != item_id]

# Este es el botón para eliminar productos
boton_eliminar = tk.Button(ventana, text="Eliminar", bg="#ffdddd", command=eliminar_seleccionados)
boton_eliminar.pack(pady=5)

''' definimos la función buscar en tabla, con un ciclo For. Con el método get_children(), que devuelve una tupla de identificadores 
de elementos, luego iteramos esa tupla con el ciclo for y compararamos los valores asociados al item con la consulta. Si son iguales,
seleccionamos el elemento del arból, con el método selection_add().
'''
def buscar_en_tabla(consulta):
    if len(consulta) ==0:
        messagebox.showinfo("Buscar", f"No ingresó un texto para buscar. Por favor ingrese nuevamente")
    else:
        items = tabla.get_children()
        contador = 0
        tabla.selection_remove(items)
        for item in items:  
            if consulta.lower() in str(tabla.item(item)['values']).lower():
                tabla.selection_add(item)
                tabla.focus(item)
                contador +=1
                pass
        if contador == 0:
            messagebox.showinfo("Buscar", f"No encontró resultados para '{consulta}'.")

# Entrada de busqueda
buscar_entrada= ttk.Entry(ventana)
buscar_entrada.pack(side=tk.TOP, padx=10, pady=5)

# Boton de busqueda
busqueda_button = ttk.Button(ventana, text="Buscar", command=lambda: buscar_en_tabla(buscar_entrada.get()))
busqueda_button.pack(side=tk.TOP, padx=10, pady=5)

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

# Vincula la tecla "Enter" a la función carga_nuevo_producto
entrada_precio.bind("<Return>", lambda event: carga_nuevo_producto())

# Esto hace que la columna del botón no se expanda
frame_ingreso.grid_columnconfigure(3, weight=1)

# Este es un botón para agregar el producto
boton_agregar = tk.Button(frame_ingreso, text="Agregar", bg="#ddffdd", command=carga_nuevo_producto)
boton_agregar.grid(row=1, column=3, padx=(20, 0), sticky="e")

# Mostramos la ventana
ventana.mainloop()
