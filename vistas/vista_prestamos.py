import flet as ft

class VistaPrestamos:
    def __init__(self, biblioteca, page):
        self.page = page
        self.biblioteca = biblioteca

        self.drop_libros = ft.Dropdown(label="Seleccionar Libro", width=300, on_change=self.cambiar_estado_boton)
        self.drop_clientes = ft.Dropdown(label="Seleccionar Cliente", width=300, on_change=self.cambiar_estado_boton)
        
        self.btn_prestar = ft.ElevatedButton("Realizar Préstamo", icon=ft.icons.BOOK, disabled=True, on_click=self.prestar_libro)
        
        self.lista_prestados = ft.ListView(expand=True, spacing=10)
        self.mensaje = ft.Text("")
        
        self.actualizar_listas()

    def cambiar_estado_boton(self, e):
        self.btn_prestar.disabled = not (self.drop_libros.value and self.drop_clientes.value)
        self.page.update()

    def prestar_libro(self, e):
        isbn = self.drop_libros.value
        cedula = self.drop_clientes.value
        
        exito = self.biblioteca.prestar_libro(isbn, cedula)
        
        if exito:
            libro = self.biblioteca.buscar_libro_por_isbn(isbn)
            cliente = self.biblioteca.buscar_cliente_por_cedula(cedula)
            
            self.mensaje.value = f"✅ Préstamo exitoso: '{libro.titulo}' prestado a {cliente.nombre}."
            self.mensaje.color = ft.colors.GREEN
            
            self.drop_libros.value = None
            self.drop_clientes.value = None
            self.btn_prestar.disabled = True
            
            self.actualizar_listas()
        else:
            self.mensaje.value = "❌ Error: El libro no está disponible o los datos son incorrectos."
            self.mensaje.color = ft.colors.RED
            
        self.page.update()

    def devolver_libro(self, e, libro):
        exito = self.biblioteca.devolver_libro(libro.isbn)
        if exito:
            self.mensaje.value = f"✅ Libro '{libro.titulo}' devuelto exitosamente."
            self.mensaje.color = ft.colors.GREEN
            self.actualizar_listas()
            self.page.update()

    def actualizar_listas(self):
        self.drop_libros.options = []
        for libro in self.biblioteca.obtener_libros_disponibles():
            self.drop_libros.options.append(ft.dropdown.Option(key=libro.isbn, text=libro.titulo))
        
        self.drop_clientes.options = []
        for cliente in self.biblioteca.clientes:
            self.drop_clientes.options.append(ft.dropdown.Option(key=cliente.cedula, text=f"{cliente.nombre} {cliente.apellido}"))

        self.lista_prestados.controls.clear()
        for libro in self.biblioteca.obtener_libros_prestados():
            cliente = self.biblioteca.buscar_cliente_por_cedula(libro.cliente_asignado)
            nombre_cliente = f"{cliente.nombre} {cliente.apellido}" if cliente else "Desconocido"
            
            self.lista_prestados.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"📖 {libro.titulo}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Prestado a: {nombre_cliente}"),
                            ft.Row([
                                ft.Text(f"Estado: {libro.estado}", color=ft.colors.ORANGE),
                                ft.ElevatedButton("Devolver", icon=ft.icons.BACK_HAND, on_click=lambda e, l=libro: self.devolver_libro(e, l))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=5),
                        padding=15
                    )
                )
            )

    def construir(self):
        return ft.Column([
            ft.Text("Gestión de Préstamos", size=28, weight=ft.FontWeight.BOLD),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Realizar nuevo préstamo", size=20, weight=ft.FontWeight.BOLD),
                        self.drop_libros,
                        self.drop_clientes,
                        self.btn_prestar,
                        self.mensaje
                    ], spacing=15),
                    padding=20
                )
            ),
            ft.Divider(height=30),
            ft.Text("Libros actualmente prestados", size=20, weight=ft.FontWeight.BOLD),
            self.lista_prestados,
        ], expand=True, spacing=15)