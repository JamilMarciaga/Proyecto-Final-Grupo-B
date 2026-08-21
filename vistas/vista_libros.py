import flet as ft

class VistaLibros:
    def __init__(self, biblioteca, page):
        self.biblioteca = biblioteca
        self.page = page

        self.txt_titulo = ft.TextField(label="Título", hint_text="Ingrese el título del libro", expand=True)
        self.txt_autor = ft.TextField(label="Autor", hint_text="Ingrese el autor", expand=True)
        self.txt_isbn = ft.TextField(label="ISBN", hint_text="Ingrese el ISBN", expand=True)

        self.txt_buscar = ft.TextField(
            label="Buscar libro",
            hint_text="Título, autor o ISBN",
            prefix_icon=ft.icons.SEARCH,
            expand=True,
            on_change=self.buscar_libro
        )

        self.filtro_estado = ft.Dropdown(
            label="Filtrar por estado", width=200,
            options=[
                ft.dropdown.Option(key="Todos", text="Todos"),
                ft.dropdown.Option(key="Disponible", text="Disponible"),
                ft.dropdown.Option(key="Prestado", text="Prestado")
            ],
            value="Todos", on_change=self.cambiar_filtro
        )

        self.mensaje = ft.Text("")
        self.total_libros = ft.Text("Total: 0", weight=ft.FontWeight.BOLD)
        self.total_disponibles = ft.Text("Disponibles: 0", weight=ft.FontWeight.BOLD)
        self.total_prestados = ft.Text("Prestados: 0", weight=ft.FontWeight.BOLD)

        self.lista_libros = ft.ListView(expand=True, spacing=10)
        self.texto_busqueda = ""
        self.estado_filtro = "Todos"

    def registrar_libro(self, e):
        titulo = self.txt_titulo.value.strip()
        autor = self.txt_autor.value.strip()
        isbn = self.txt_isbn.value.strip()

        if not titulo or not autor or not isbn:
            self.mostrar_mensaje("Debe completar todos los campos.", True)
            return

        exito = self.biblioteca.agregar_libro(titulo, autor, isbn)
        if not exito:
            self.mostrar_mensaje("Ya existe un libro con ese ISBN.", True)
            return

        self.txt_titulo.value = ""
        self.txt_autor.value = ""
        self.txt_isbn.value = ""

        self.mostrar_mensaje("Libro registrado correctamente.", False)
        self.actualizar_lista()

    def buscar_libro(self, e):
        self.texto_busqueda = self.txt_buscar.value.strip().lower()
        self.actualizar_lista()

    def cambiar_filtro(self, e):
        self.estado_filtro = self.filtro_estado.value
        self.actualizar_lista()

    def crear_tarjeta_libro(self, libro):
        informacion = [
            ft.Text(libro.titulo, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"Autor: {libro.autor}"),
            ft.Text(f"ISBN: {libro.isbn}"),
            ft.Text(f"Estado: {libro.estado}", weight=ft.FontWeight.BOLD)
        ]
        if libro.cliente_asignado:
            cliente = self.biblioteca.buscar_cliente_por_cedula(libro.cliente_asignado)
            nombre_cliente = f"{cliente.nombre} {cliente.apellido}" if cliente else "Desconocido"
            informacion.append(ft.Text(f"Prestado a: {nombre_cliente}"))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(controls=informacion, spacing=5),
                padding=15
            )
        )

    def actualizar_lista(self):
        self.lista_libros.controls.clear()
        disponibles = prestados = 0

        for libro in self.biblioteca.libros:
            estado = libro.estado
            
            if estado == "Disponible":
                disponibles += 1
            elif estado == "Prestado":
                prestados += 1

            if self.estado_filtro != "Todos" and estado != self.estado_filtro:
                continue

            texto = f"{libro.titulo} {libro.autor} {libro.isbn}".lower()
            if self.texto_busqueda and self.texto_busqueda not in texto:
                continue

            self.lista_libros.controls.append(self.crear_tarjeta_libro(libro))

        self.total_libros.value = f"Total: {len(self.biblioteca.libros)}"
        self.total_disponibles.value = f"Disponibles: {disponibles}"
        self.total_prestados.value = f"Prestados: {prestados}"

        if len(self.lista_libros.controls) == 0:
            self.lista_libros.controls.append(
                ft.Container(content=ft.Text("No se encontraron libros."), padding=20)
            )

        self.lista_libros.update()

    def mostrar_mensaje(self, texto, error=False):
        self.mensaje.value = texto
        self.mensaje.color = ft.colors.RED if error else ft.colors.GREEN
        self.mensaje.update()

    def construir(self):
        formulario = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Registrar nuevo libro", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([self.txt_titulo, self.txt_autor]),
                    ft.Row([self.txt_isbn, ft.ElevatedButton("Registrar libro", icon=ft.icons.ADD, on_click=self.registrar_libro)]),
                    self.mensaje
                ], spacing=12),
                padding=20
            )
        )

        filtros = ft.Row([self.txt_buscar, self.filtro_estado])
        estadisticas = ft.Row([self.total_libros, self.total_disponibles, self.total_prestados], spacing=25)

        return ft.Column([
            ft.Text("Gestión de Libros", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Registre y consulte el inventario de libros de la biblioteca."),
            formulario,
            estadisticas,
            filtros,
            ft.Text("Inventario de libros", size=20, weight=ft.FontWeight.BOLD),
            self.lista_libros,
        ], expand=True, spacing=15)