import flet as ft

class VistaPrestamos:
    def __init__(self, page, libros, clientes):
        self.page = page
        self.libros = libros
        self.clientes = clientes

        self.drop_libros = ft.Dropdown(
            label="Seleccionar Libro",
            width=300,
            on_change=self.cambiar_estado_boton
        )
        self.drop_clientes = ft.Dropdown(
            label="Seleccionar Cliente",
            width=300,
            on_change=self.cambiar_estado_boton
        )
        
        self.btn_prestar = ft.ElevatedButton(
            "Realizar Préstamo",
            icon=ft.icons.BOOK,
            disabled=True,
            on_click=self.prestar_libro
        )
        
        self.lista_prestados = ft.ListView(expand=True, spacing=10)
        self.mensaje = ft.Text("")
        
        self.actualizar_listas()

    def cambiar_estado_boton(self, e):
        if self.drop_libros.value and self.drop_clientes.value:
            self.btn_prestar.disabled = False
        else:
            self.btn_prestar.disabled = True
        self.page.update()

    def prestar_libro(self, e):
        isbn_seleccionado = self.drop_libros.value
        cedula_seleccionada = self.drop_clientes.value
        
        libro_encontrado = None
        for libro in self.libros:
            if libro.get("isbn") == isbn_seleccionado:
                libro_encontrado = libro
                break
        
        cliente_encontrado = None
        for cliente in self.clientes:
            if cliente.get("cedula") == cedula_seleccionada:
                cliente_encontrado = cliente
                break
        
        if libro_encontrado and cliente_encontrado:
            if libro_encontrado.get("estado") == "Disponible":
                libro_encontrado["estado"] = "Prestado"
                libro_encontrado["cliente"] = f"{cliente_encontrado['nombre']} {cliente_encontrado['apellido']}"
                
                self.mensaje.value = f"✅ Préstamo exitoso: '{libro_encontrado['titulo']}' prestado a {libro_encontrado['cliente']}."
                self.mensaje.color = ft.colors.GREEN
                
                self.drop_libros.value = None
                self.drop_clientes.value = None
                self.btn_prestar.disabled = True
                
                self.actualizar_listas()
                self.page.update()
            else:
                self.mensaje.value = "❌ Error: El libro ya está prestado."
                self.mensaje.color = ft.colors.RED
                self.page.update()

    def devolver_libro(self, e, libro):
        if libro["estado"] == "Prestado":
            libro["estado"] = "Disponible"
            libro["cliente"] = None
            
            self.mensaje.value = f"✅ Libro '{libro['titulo']}' devuelto exitosamente."
            self.mensaje.color = ft.colors.GREEN
            
            self.actualizar_listas()
            self.page.update()

    def actualizar_listas(self):
        self.drop_libros.options = []
        for libro in self.libros:
            if libro.get("estado") == "Disponible":
                self.drop_libros.options.append(
                    ft.dropdown.Option(key=libro["isbn"], text=libro["titulo"])
                )
        
        self.drop_clientes.options = []
        for cliente in self.clientes:
            self.drop_clientes.options.append(
                ft.dropdown.Option(key=cliente["cedula"], text=f"{cliente['nombre']} {cliente['apellido']}")
            )

        self.lista_prestados.controls.clear()
        for libro in self.libros:
            if libro.get("estado") == "Prestado":
                self.lista_prestados.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"📖 {libro['titulo']}", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Prestado a: {libro.get('cliente', 'Desconocido')}"),
                                ft.Row([
                                    ft.Text(f"Estado: {libro['estado']}", color=ft.colors.ORANGE),
                                    ft.Button("Devolver", icon=ft.icons.BACK_HAND, on_click=lambda e, l=libro: self.devolver_libro(e, l))
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
            ft.ElevatedButton("Volver al Menú", icon=ft.icons.ARROW_BACK, on_click=self.page.volver_al_menu)
        ], expand=True, spacing=15)