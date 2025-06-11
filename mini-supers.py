import tkinter as tk
from tkinter import ttk, messagebox

# Importamos la librería para los tooltips
from idlelib.tooltip import Hovertip

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
ventana.geometry('600x600')  # Aumentamos la altura para que entre el nuevo panel

# Esto es el menú de arriba
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_productos = tk.Menu(barra_menu, tearoff=0)
menu_productos.add_command(label="Ver productos", command=lambda: mostrar_productos_agrupados())

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

tabla.bind("<<TreeviewSelect>>", sincronizar_checks)

# Defino la función carga nuevo producto
def carga_nuevo_producto():
    producto = entrada_producto.get().strip().title()
    nombre = entrada_nombre.get().strip().title()
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
    # Obtiene el ID del item (fila) sobre el que se hizo doble clic, usando la posición vertical del mouse
    item_id = tabla.identify_row(event.y)
    # Obtiene la columna sobre la que se hizo doble clic, usando la posición horizontal del mouse
    col = tabla.identify_column(event.x)

    # Si no se hizo clic sobre ningún item o no es la columna 4 ('seleccionado'), sale de la función
    if not item_id or col != '#4':
        return
    
    # Obtiene los valores actuales de la fila como una lista
    valores = list(tabla.item(item_id, "values"))
    # Determina si el check está marcado actualmente (si hay un "✓" en la columna 'seleccionado')
    seleccionado = valores[3] == "✓"
    # Alterna el valor del check: si estaba marcado, lo desmarca; si no, lo marca
    valores[3] = "" if seleccionado else "✓"
    # Actualiza los valores de la fila en la tabla con el nuevo estado del check
    tabla.item(item_id, values=valores)

    # Busca el producto correspondiente en la lista_productos y actualiza su campo 'seleccionado'
    for prod in lista_productos:
        if str(prod["id"]) == item_id:
            prod["seleccionado"] = not seleccionado
            break

tabla.bind("<Double-1>", alternar_check)

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
            lista_productos[:] = [prod for prod in lista_productos if str(prod["id"]) != item_id]

# Este es el botón para eliminar productos
boton_eliminar = tk.Button(ventana, text="Eliminar", bg="#ffdddd", command=eliminar_seleccionados)
boton_eliminar.pack(pady=5)

# Tooltip para el botón de eliminar
Hovertip(boton_eliminar, "Eliminar productos seleccionados", hover_delay=500)

''' definimos la función buscar en tabla, con un ciclo For. Con el método get_children(), que devuelve una tupla de identificadores 
de elementos, luego iteramos esa tupla con el ciclo for y compararamos los valores asociados al item con la consulta. Si son iguales,
seleccionamos el elemento del arból, con el método selection_add().
'''
def buscar_en_tabla(consulta):
    # No hace nada si la consulta está vacía
    if not consulta:
        return  
    else:
        items = tabla.get_children()
        contador = 0
        tabla.selection_remove(*items)  # El asterisco * descompone la tupla en argumentos individuales, así se eliminan todas las selecciones previas.
        consulta = consulta.strip()
    
    for item in items:  
        if consulta.lower() in str(tabla.item(item)['values']).lower():
            tabla.selection_add(item)
            tabla.focus(item)
            contador += 1

    # Limpia la entrada de búsqueda
    buscar_entrada.delete(0, tk.END)
    
    if contador == 0:
        messagebox.showinfo("Buscar", f"No encontró resultados para '{consulta}'.")

# Frame para agrupar el entry de búsqueda y los botones
frame_busqueda = tk.Frame(ventana)
frame_busqueda.pack(side=tk.TOP, padx=10, pady=5)

# Botón para limpiar el entry de búsqueda
limpiar_button = ttk.Button(frame_busqueda, text="❌", width=4, command=lambda: buscar_entrada.delete(0, tk.END))
limpiar_button.pack(side=tk.LEFT, padx=(0, 2), pady=2)

# Tooltip para el botón de limpiar
Hovertip(limpiar_button, "Limpiar entrada de búsqueda", hover_delay=500)

# Entrada de busqueda
buscar_entrada = ttk.Entry(frame_busqueda, justify='center')
buscar_entrada.pack(side=tk.LEFT, padx=10, pady=5)
buscar_entrada.focus()

# Boton de busqueda
busqueda_button = ttk.Button(frame_busqueda, text="Buscar", command=lambda: buscar_en_tabla(buscar_entrada.get()))
busqueda_button.pack(side=tk.LEFT, padx=10, pady=5)

# Tooltip para el botón de búsqueda
Hovertip(busqueda_button, "Buscar producto", hover_delay=500)

# Vincula la tecla "Enter" a la función buscar_en_tabla con buscar_entrada
buscar_entrada.bind("<Return>", lambda event: buscar_en_tabla(buscar_entrada.get()))

# NUEVO: Frame para ver productos agrupados
frame_agrupados = tk.Frame(ventana)
frame_agrupados.pack_forget()  # Oculto al inicio

tree_agrupados = ttk.Treeview(frame_agrupados)
tree_agrupados.pack(fill=tk.BOTH, expand=True)
tree_agrupados.heading("#0", text="Productos por categoría")

# Función para mostrar productos agrupados
def mostrar_productos_agrupados():
    if frame_agrupados.winfo_ismapped():
        frame_agrupados.pack_forget()
        return

    for item in tree_agrupados.get_children():
        tree_agrupados.delete(item)

    grupos = {}
    for producto in lista_productos:
        grupo = producto['producto']
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(producto)

    for grupo, items in grupos.items():
        nodo = tree_agrupados.insert("", "end", text=grupo)
        for item in items:
            tree_agrupados.insert(nodo, "end", text=f"{item['nombre']} - ${item['precio']}")

    frame_agrupados.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# (Frame = Caja) Aquí va la parte de abajo donde escribís los datos
frame_ingreso = tk.Frame(ventana)
frame_ingreso.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

# Estas son etiquetas de cada campo que hicimso
tk.Label(frame_ingreso, text="Producto:").grid(row=0, column=0, sticky="w", padx=(0, 5))
tk.Label(frame_ingreso, text="Nombre:").grid(row=0, column=1, sticky="w", padx=(10, 5))
tk.Label(frame_ingreso, text="Precio:").grid(row=0, column=2, sticky="w", padx=(10, 5))

# En esta parte creamos cajitas para escribir los datos que se van a ingresar
entrada_producto = tk.Entry(frame_ingreso, width=20)
entrada_producto.grid(row=1, column=0, padx=(0, 5))
Hovertip(entrada_producto, "Ingrese el tipo de producto (ej. Leche, Pan, Gaseosa)", hover_delay=500)

entrada_nombre = tk.Entry(frame_ingreso, width=20)
entrada_nombre.grid(row=1, column=1, padx=(10, 5))
Hovertip(entrada_nombre, "Ingrese el nombre del producto (ej. La Serenísima, Baguette, Manaos)", hover_delay=500)

entrada_precio = tk.Entry(frame_ingreso, width=15)
entrada_precio.grid(row=1, column=2, padx=(10, 5))
Hovertip(entrada_precio, "Ingrese el precio del producto (ej. 1200)", hover_delay=500)

# Vincula la tecla "Enter" a la función carga_nuevo_producto con la entrada de precio
entrada_precio.bind("<Return>", lambda event: carga_nuevo_producto())

# Esto hace que la columna del botón no se expanda
frame_ingreso.grid_columnconfigure(3, weight=1)

# Este es el botón para agregar el producto
boton_agregar = tk.Button(frame_ingreso, text="Agregar", bg="#ddffdd", command=carga_nuevo_producto)
boton_agregar.grid(row=1, column=3, padx=(20, 0), sticky="e")

# Tooltip para el botón de agregar
Hovertip(boton_agregar, "Agregar nuevo producto. Rellene todos los campos", hover_delay=500)

# Mostramos la ventana
ventana.mainloop()
