import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar
# Importamos la librería para los tooltips
from idlelib.tooltip import Hovertip

# Lista para guardar los productos
lista_productos = [
    {"producto": "Leche", "nombre": "La Serenísima", "precio": "1500"},
    {"producto": "Pan", "nombre": "Baguette", "precio": "1800"},
    {"producto": "Queso", "nombre": "Cremoso", "precio": "2500"},
    {"producto": "Queso", "nombre": "Sardo", "precio": "13000"},
    {"producto": "Galletitas", "nombre": "Pepitos", "precio": "600"},
    {"producto": "Galletitas", "nombre": "Chocolinas", "precio": "700"},
    {"producto": "Gaseosa", "nombre": "Sprite", "precio": "4000"},
    {"producto": "Gaseosa", "nombre": "Cabalgata", "precio": "2600"},
    {"producto": "Gaseosa", "nombre": "Manaos", "precio": "2500"},
    {"producto": "Cerveza", "nombre": "Quilmes", "precio": "3500"},
    {"producto": "Cerveza", "nombre": "Miller", "precio": "3700"},
    {"producto": "Fideos", "nombre": "Maggie", "precio": "2300"},
    {"producto": "Gaseosa", "nombre": "Coca Cola", "precio": "4000"},
    {"producto": "Aceite", "nombre": "Girasol", "precio": "5000"},
    {"producto": "Pan", "nombre": "Integral", "precio": "3000"},
]

# Usamos una lista para que sea mutable dentro de la función
contador_id = [1]  

# Creamos la ventanita
ventana = tk.Tk()
ventana.title('MiniSupers')
ventana.geometry('780x600')  # Aumentamos la altura para que entre el nuevo panel

# Icon
ventana.iconbitmap("icon/icon1.ico")

# ********************** BARRA DE MENÚ **********************

# Creamos la barra de menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Funcionalidad de "Quiénes somos"
def mostrar_quienes_somos():
    if frame_agrupados.winfo_ismapped():
        frame_agrupados.pack_forget()

    ventana_info = tk.Toplevel(ventana)
    ventana_info.title("Quiénes somos - MiniSupers")
    ventana_info.resizable(False, False)
    ventana_info.transient(ventana)
    ventana_info.grab_set()

    # Centrar la ventana respecto a la ventana principal
    ancho, alto = 500, 400
    ventana.update_idletasks()
    x_principal = ventana.winfo_x()
    y_principal = ventana.winfo_y()
    ancho_principal = ventana.winfo_width()
    alto_principal = ventana.winfo_height()
    x = x_principal + (ancho_principal // 2) - (ancho // 2)
    y = y_principal + (alto_principal // 2) - (alto // 2)
    ventana_info.geometry(f"{ancho}x{alto}+{x}+{y}")

    frame_contenido = tk.Frame(ventana_info, padx=20, pady=20)
    frame_contenido.pack(fill=tk.BOTH, expand=True)

    titulo = tk.Label(frame_contenido, text="¿Quiénes somos?", font=("Arial", 16, "bold"))
    titulo.pack(pady=(0, 20))

    texto_info = """MiniSupers es una aplicación de gestión de inventario desarrollada para pequeños supermercados y comercios.

Nuestra misión es facilitar el control y administración de productos, permitiendo:

• Agregar y eliminar productos fácilmente
• Buscar productos de manera eficiente
• Organizar productos por categorías
• Mantener un control de precios actualizado

Desarrollado con Python y Tkinter, MiniSupers ofrece una interfaz intuitiva y funcional para la gestión diaria de tu negocio.

¡Gracias por confiar en MiniSupers para tu gestión de inventario!"""

    texto_label = tk.Label(frame_contenido, text=texto_info, justify=tk.LEFT, wraplength=450, font=("Arial", 10))
    texto_label.pack(pady=(0, 20))

    boton_cerrar = tk.Button(frame_contenido, text="Cerrar", command=ventana_info.destroy, bg="#dddddd", width=15)
    boton_cerrar.pack()

menu_productos = tk.Menu(barra_menu, tearoff=0)
menu_productos.add_command(label="Ver productos", command=lambda: mostrar_productos_agrupados())

menu_info = tk.Menu(barra_menu, tearoff=0)
menu_info.add_command(label="Quiénes somos", command=mostrar_quienes_somos)

barra_menu.add_cascade(label="Productos", menu=menu_productos)
barra_menu.add_cascade(label="Quiénes somos", menu=menu_info)

# ********************** TABLA **********************

# Este es el lugar donde va la tabla que muestra los productos
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

# Barra para pueder bajar y ver mas cosas si hay muchas
scroll = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Con esto decimos que la tabla va a tener 4 columnas
columnas = ('producto', 'nombre', 'precio', 'seleccionado')
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scroll.set)
# Permitir selección múltiple en la tabla: La selección multiple presionando Ctrl o Shift
tabla.config(selectmode="extended")

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
        values=(prod["producto"], prod["nombre"], f"${prod["precio"]}", "")
    )

# Función para sincronizar los checks de la tabla con la selección actual
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

# Cambia el estado de seleccionado en la lista y en la tabla
def alternar_check(event):
    """
    Alterna el estado del check (✓) en la columna 'seleccionado' de la fila sobre la que se hizo doble clic.

    - Detecta si el doble clic fue sobre la columna 'seleccionado' de la tabla.
    - Marca o desmarca el check en la celda correspondiente.
    - Actualiza el campo 'seleccionado' del producto en la lista 'lista_productos' para mantener la sincronización.

    Parámetros:
        event (tk.Event): Evento de Tkinter que contiene información sobre la posición del clic.

    Retorna:
        None
    """
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
tabla.column('producto', width=130)
tabla.column('nombre', width=130)
tabla.column('precio', width=100)
tabla.column('seleccionado', width=90, anchor='center')

tabla.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
scroll.config(command=tabla.yview)

# ********************** FILA SELECCIONADOS Y ELIMINAR **********************

# Crea un frame para agrupar el label y el botón
frame_acciones = tk.Frame(ventana)
frame_acciones.pack(fill=tk.X, padx=10, pady=5)

# Label de seleccionados
label_seleccionados = tk.Label(frame_acciones, text="No hay productos seleccionados.")
label_seleccionados.pack(side=tk.LEFT, padx=(0, 10))

def actualizar_label_seleccionados(event=None):
    sincronizar_checks()
    cantidad = len(tabla.selection())
    label_seleccionados.config(text=(
            "No hay productos seleccionados."
            if cantidad == 0 else
            f"Seleccionado: {cantidad} producto."
            if cantidad == 1 else
            f"Seleccionados: {cantidad} productos."
        )
    )

# Asociar la función al evento de selección de la tabla
tabla.bind("<<TreeviewSelect>>", actualizar_label_seleccionados)

# Definimos la función eliminar seleccionados
def eliminar_seleccionados():
    """
    Elimina de la tabla y de la lista 'lista_productos' todos los productos que estén seleccionados y tengan el check (✓) en la columna 'seleccionado'.

    - Recorre los elementos seleccionados en la tabla.
    - Verifica si la columna 'seleccionado' está marcada con un check.
    - Elimina esos productos tanto de la tabla visual como de la lista en memoria.
    - Muestra un mensaje si no hay productos seleccionados.

    Parámetros:
        None

    Retorna:
        None
    """
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
boton_eliminar = tk.Button(frame_acciones, text="Eliminar",width=15, bg="#ffdddd", command=eliminar_seleccionados)
boton_eliminar.pack(side=tk.RIGHT, padx=(0, 10))
# Tooltip para el botón de eliminar
Hovertip(boton_eliminar, "Eliminar productos seleccionados", hover_delay=500)

# ******** FILA DE BÚSQUEDA ********

def buscar_en_tabla(consulta):
    ''' 
    Definimos la función buscar en tabla, con un ciclo For. Con el método get_children(), que devuelve una tupla de identificadores 
    de elementos, luego iteramos esa tupla con el ciclo for y compararamos los valores asociados al item con la consulta. Si son iguales,
    seleccionamos el elemento del arból, con el método selection_add().
    '''
    # No hace nada si la consulta está vacía
    if not consulta or consulta=="Ingrese el producto que busca." or not consulta.strip():
        messagebox.showinfo("Buscar", "Por favor ingrese un producto a buscar.")
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
limpiar_button = ttk.Button(
    frame_busqueda, 
    text="x", 
    width=2, 
    command=lambda: [buscar_entrada.delete(0, tk.END), buscar_entrada.focus_set()]
)

limpiar_button.pack(side=tk.LEFT)
# Tooltip para el botón de limpiar
Hovertip(limpiar_button, "Limpiar entrada de búsqueda", hover_delay=500)

# Entrada de busqueda
buscar_entrada = ttk.Entry(frame_busqueda, justify='center')
buscar_entrada.config(foreground="grey")
buscar_entrada.placeholder = "Ingrese el producto que busca."
buscar_entrada.insert(0, buscar_entrada.placeholder)

def on_focus_in(event):
    """
    Maneja el evento cuando el Entry de búsqueda recibe el foco.

    - Si el contenido del Entry es igual al placeholder, lo borra y cambia el color del texto a negro.

    Parámetros:
        event (tk.Event): Evento de Tkinter que contiene el widget que recibió el foco.

    Retorna:
        None
    """
    widget = event.widget
    # Solo ejecuta si el widget es un Entry
    if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Entry):
        if event.widget.get() == event.widget.placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(foreground="black")

def on_focus_out(event):
    """
    Maneja el evento cuando el Entry de búsqueda pierde el foco.

    - Si el Entry está vacío, coloca el texto del placeholder y cambia el color del texto a gris.

    Parámetros:
        event (tk.Event): Evento de Tkinter que contiene el widget que perdió el foco.

    Retorna:
        None
    """
    if not event.widget.get():
        event.widget.insert(0, event.widget.placeholder)
        event.widget.config(foreground="grey")

buscar_entrada.bind("<FocusIn>", on_focus_in)
buscar_entrada.bind("<FocusOut>", on_focus_out)
buscar_entrada.pack(side=tk.LEFT, padx=10, pady=5)
buscar_entrada.focus()
# Tooltip para la entrada de búsqueda
Hovertip(buscar_entrada, "¿Qué producto busca?", hover_delay=500)

# Boton de busqueda
busqueda_button = ttk.Button(frame_busqueda, text="Buscar", width=15, command=lambda: buscar_en_tabla(buscar_entrada.get()))
busqueda_button.pack(side=tk.LEFT, padx=10, pady=5)
# Tooltip para el botón de búsqueda
Hovertip(busqueda_button, "Buscar producto", hover_delay=500)

# Vincula la tecla "Enter" a la función buscar_en_tabla con buscar_entrada
buscar_entrada.bind("<Return>", lambda event: buscar_en_tabla(buscar_entrada.get()))

# ********************** EVENTOS/BTNs DE LA TABLA **********************

def seleccionar_todos(event):
    ''' 
    La función seleccionar_todos utilizará los métodos identify(), para identificar la región del heading
    e identify_column(), para identificar la columna seleccionado. 
    Si el usuario hace click en el heading de la columna 4, y existen elementos seleccionados, los va a deseleccionar con el método selection_remove(), y si
    no existen elementos seleccionados va a seleccionar a todos los elementos de la tabla, con el método selection_add().  
    '''
    region = tabla.identify("region", event.x, event.y)
    columna = tabla.identify_column(event.x)
    if region == "heading" and columna == '#4':
        if tabla.selection():
            items = tabla.selection()
            tabla.selection_remove(*items)
        else:
            items = tabla.get_children()
            for item in items:  
                tabla.selection_add(item)
                tabla.focus(item)

        # Llama manualmente a la función para actualizar el label
        actualizar_label_seleccionados()

tabla.bind('<Button-1>', seleccionar_todos)

# Cambio de nombre deel heading seleccionados cuando se posiciona el cursor del mouse en el heading.
def cambiar_heading_seleccionados(event):
    ''' 
    La función cambiar_heading_seleccionados utilizará los métodos identify_region(), para identificar la región del heading
    e identify_column(), para identificar la columna seleccionado. Si el usuario posiciona el cursor del mouse en el heading de la
    columna 4, cambiaremos el nombre del heading por 'Seleccionar todos', y si sale el cursor de esa región
    volvera a cambiar el nombre a '✓' 
    '''
    region = tabla.identify_region(event.x, event.y)
    columna = tabla.identify_column(event.x)
    if region == "heading" and columna == '#4':
        if tabla.selection():
            tabla.heading('seleccionado', text='Deseleccionar todo', anchor="center")
            pass
        else:
            tabla.heading('seleccionado', text='Seleccionar todo', anchor="center")
            pass
    else:
        tabla.heading('seleccionado', text='✓')
# Con el método bind vinculará el evento '<Motion>' del cursor del mouse, con la función cambiar_heading_seleccionados.
tabla.bind('<Motion>',cambiar_heading_seleccionados)

# Ordenamiento de la tabla por columna 'producto'
def ordenar_columna_producto():
    """
    Ordena la tabla por la columna 'producto' de forma ascendente o descendente.

    - Obtiene todos los elementos de la tabla y sus valores en la columna 'producto'.
    - Ordena los elementos alfabéticamente según el sentido actual (ascendente o descendente).
    - Reordena visualmente las filas en la tabla.
    - Alterna el sentido de ordenamiento para la próxima vez que se presione el encabezado.

    Parámetros:
        None

    Retorna:
        None
    """
    # Obtiene todos los items de la tabla
    items = tabla.get_children()
    # Obtiene los valores de la columna 'producto' y los ids
    datos = [(tabla.set(item, 'producto'), item) for item in items]
    # Alterna el sentido de ordenamiento usando un atributo en la tabla
    sentido = getattr(tabla, 'orden_producto_asc', True)
    # Ordena los datos
    datos.sort(reverse=not sentido)
    # Reordena los items en la tabla
    for index, (valor, item) in enumerate(datos):
        tabla.move(item, '', index)
    # Cambia el sentido para la próxima vez
    tabla.orden_producto_asc = not sentido

tabla.heading('producto', text='Producto', command=ordenar_columna_producto)

# Ordenamiento de la tabla por columna 'nombre'
def ordenar_columna_nombre():
    """
    Ordena la tabla por la columna 'nombre' de forma ascendente o descendente.

    - Obtiene todos los elementos de la tabla y sus valores en la columna 'nombre'.
    - Ordena los elementos alfabéticamente según el sentido actual (ascendente o descendente).
    - Reordena visualmente las filas en la tabla.
    - Alterna el sentido de ordenamiento para la próxima vez que se presione el encabezado.

    Parámetros:
        None

    Retorna:
        None
    """
    # Obtiene todos los items de la tabla
    items = tabla.get_children()
    # Obtiene los valores de la columna 'nombre' y los ids
    datos = [(tabla.set(item, 'nombre'), item) for item in items]
    # Alterna el sentido de ordenamiento usando un atributo en la tabla
    sentido = getattr(tabla, 'orden_nombre_asc', True)
    # Ordena los datos
    datos.sort(reverse=not sentido)
    # Reordena los items en la tabla
    for index, (valor, item) in enumerate(datos):
        tabla.move(item, '', index)
    # Cambia el sentido para la próxima vez
    tabla.orden_nombre_asc = not sentido

tabla.heading('nombre', text='Nombre', command=ordenar_columna_nombre)

# Ordenamiento de la tabla por columna 'precio'
def ordenar_columna_precio():
    """
    Ordena la tabla por la columna 'precio' de forma ascendente o descendente.

    - Obtiene todos los elementos de la tabla y sus valores en la columna 'precio'.
    - Convierte los valores de precio a números para ordenar correctamente.
    - Ordena los elementos numéricamente según el sentido actual (ascendente o descendente).
    - Reordena visualmente las filas en la tabla.
    - Alterna el sentido de ordenamiento para la próxima vez que se presione el encabezado.

    Parámetros:
        None

    Retorna:
        None
    """
    # Obtiene todos los items de la tabla
    items = tabla.get_children()
    # Obtiene los valores de la columna 'precio' y los ids, convirtiendo el precio a float/int para ordenar correctamente
    datos = []
    for item in items:
        valor = tabla.set(item, 'precio')
        # Elimina el símbolo $ si lo tiene y convierte a float
        try:
            valor_num = float(str(valor).replace("$", "").replace(",", "."))
        except ValueError:
            valor_num = 0
        datos.append((valor_num, item))
    # Alterna el sentido de ordenamiento usando un atributo en la tabla
    sentido = getattr(tabla, 'orden_precio_asc', True)
    # Ordena los datos numéricamente
    datos.sort(reverse=not sentido)
    # Reordena los items en la tabla
    for index, (valor, item) in enumerate(datos):
        tabla.move(item, '', index)
    # Cambia el sentido para la próxima vez
    tabla.orden_precio_asc = not sentido

tabla.heading('precio', text='Precio', command=ordenar_columna_precio)

# **************** PRODUCTOS AGRUPADOS ****************

# Frame para ver productos agrupados
frame_agrupados = tk.Frame(ventana)
frame_agrupados.pack_forget()  # Oculto al inicio

tree_agrupados = ttk.Treeview(frame_agrupados)
scrollbar=ttk.Scrollbar(tree_agrupados, orient='vertical', command=tree_agrupados.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree_agrupados['yscrollcommand']=scrollbar.set
tree_agrupados.pack(fill=tk.BOTH, expand=True)
tree_agrupados.heading("#0", text="Productos por categoría")

# Función para mostrar productos agrupados
def mostrar_productos_agrupados():
    """
    Muestra una ventana emergente con los productos agrupados por tipo.

    - Agrupa los productos de la lista 'lista_productos' según el campo 'producto'.
    - Muestra en un cuadro de mensaje (messagebox) cada grupo con los nombres y precios de los productos correspondientes.

    Parámetros:
        None

    Retorna:
        None
    """
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

# **************** INGRESO DE PRODUCTOS ****************

# (Frame = Caja) Aquí va la parte de abajo donde escribís los datos
frame_ingreso = tk.Frame(ventana)
frame_ingreso.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

# Estas son etiquetas de cada campo que hicimos
label_font = ("Arial", 10, "bold")
tk.Label(frame_ingreso,font=label_font, text="Producto:").grid(row=0, column=0, sticky="w", padx=(5, 5), pady=(0, 2))
tk.Label(frame_ingreso,font=label_font, text="Nombre:").grid(row=0, column=1, sticky="w", padx=(5, 5), pady=(0, 2))
tk.Label(frame_ingreso,font=label_font, text="Precio:").grid(row=0, column=3, sticky="w", padx=(0, 0), pady=(0, 0))

# En esta parte creamos cajitas para escribir los datos que se van a ingresar

entrada_producto = tk.Entry(frame_ingreso, width=30, justify='center', fg="grey")
entrada_producto.placeholder = "Ingrese el tipo de producto (ej. Leche, Pan, Gaseosa)"
entrada_producto.insert(0, entrada_producto.placeholder)
entrada_producto.bind("<FocusIn>", on_focus_in)
entrada_producto.bind("<FocusOut>", on_focus_out)
entrada_producto.grid(row=1, column=0, padx=10)
Hovertip(entrada_producto, "Ingrese el tipo de producto (ej. Leche, Pan, Gaseosa)", hover_delay=500)

entrada_nombre = tk.Entry(frame_ingreso, width=30, justify='center', fg="grey")
entrada_nombre.placeholder = "Ingrese la marca del producto"
entrada_nombre.insert(0, entrada_nombre.placeholder)
entrada_nombre.bind("<FocusIn>", on_focus_in)
entrada_nombre.bind("<FocusOut>", on_focus_out)
entrada_nombre.grid(row=1, column=1, padx=10)
Hovertip(entrada_nombre, "Ingrese el nombre del producto (ej. La Serenísima, Baguette, Manaos)", hover_delay=500)
# agregamos una etiqueta con el simbolo $ que se va a ubicar entre las entradas de nombre y precio.
simbolo_peso = tk.Label(frame_ingreso, text="$").grid(row=1, column=2, sticky="w", padx=(5,0))

entrada_precio = tk.Entry(frame_ingreso, width=15, justify='center', fg="grey")
entrada_precio.placeholder = "Ingrese el precio del producto"
entrada_precio.insert(0, entrada_precio.placeholder)
entrada_precio.bind("<FocusIn>", on_focus_in)
entrada_precio.bind("<FocusOut>", on_focus_out)
entrada_precio.grid(row=1, column=3, sticky='w', padx=(0,10))
Hovertip(entrada_precio, "Ingrese el precio del producto (ej. 1200)", hover_delay=500)

# Vincula la tecla "Enter" a la función carga_nuevo_producto con la entrada de precio
entrada_precio.bind("<Return>", lambda event: carga_nuevo_producto(event))

# Esto hace que la columna del botón no se expanda
frame_ingreso.grid_columnconfigure(4, weight=1)

# Defino la función carga nuevo producto
def carga_nuevo_producto(event=None):
    """
    Agrega un nuevo producto a la lista de productos y a la tabla visual.

    - Toma los valores de los campos de entrada (producto, nombre, precio).
    - Valida que los campos no estén vacíos y que el precio sea un número.
    - Genera un ID único para el producto.
    - Guarda el producto en la lista 'lista_productos' con el campo 'seleccionado' en False.
    - Inserta el producto en la tabla (Treeview) con el nuevo ID.
    - Limpia los campos de entrada y muestra el placeholder si corresponde.

    Parámetros:
        event (tk.Event, opcional): Evento de Tkinter, se usa cuando la función es llamada desde un bind. Por defecto es None.

    Retorna:
        None
    """
    producto = entrada_producto.get().strip().title().capitalize()
    nombre = entrada_nombre.get().strip().title().capitalize()
    precio = entrada_precio.get().strip()

    if any([producto==(entrada_producto.placeholder or ''),nombre==(entrada_nombre.placeholder or ''), 
            precio==(entrada_precio.placeholder or '') ]):
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
        return
    else: 
        try:
            float(precio)
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
            values=(producto, nombre, f"${precio}", "")
            )

            # Limpiar entradas
            entrada_producto.delete(0, tk.END)
            entrada_nombre.delete(0, tk.END)
            entrada_precio.delete(0, tk.END)

            # Simula el evento focus out para mostrar el placeholder
            for entrada in (entrada_producto, entrada_nombre, entrada_precio):
                event = tk.Event()
                event.widget = entrada
                on_focus_out(event)

            ventana.focus()

        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio debe ser un número.")
            return

# Este es el botón para agregar el producto
boton_agregar = tk.Button(frame_ingreso, text="Agregar",width=15, bg="#ddffdd", command=carga_nuevo_producto, justify='center')
boton_agregar.grid(row=1, column=4, padx=(5), sticky="e")
# Tooltip para el botón de agregar
Hovertip(boton_agregar, "Agregar nuevo producto. Rellene todos los campos", hover_delay=500)

# Que al seleccionar un campo, aparezca el placeholder
ventana.bind("<FocusIn>", on_focus_in)
# ventana.bind("<FocusIn>", on_focus_in_busqueda)

# Mostramos la ventana
ventana.mainloop()