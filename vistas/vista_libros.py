import flet as ft


class VistaLibros:
    def __init__(self, page, libros):
        self.page = page
        self.libros = libros

        # Campos para registrar libros
        self.txt_titulo = ft.TextField(
            label="Título",
            hint_text="Ingrese el título del libro",
            expand=True
        )

        self.txt_autor = ft.TextField(
            label="Autor",
            hint_text="Ingrese el autor",
            expand=True
        )

        self.txt_isbn = ft.TextField(
            label="ISBN",
            hint_text="Ingrese el ISBN",
            expand=True
        )

        # Campo de búsqueda
        self.txt_buscar = ft.TextField(
            label="Buscar libro",
            hint_text="Título, autor o ISBN",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            on_change=self.buscar_libro
        )

        # Filtro por estado
        self.filtro_estado = ft.Dropdown(
            label="Filtrar por estado",
            width=200,
            options=[
                ft.DropdownOption(
                    key="Todos",
                    text="Todos"
                ),
                ft.DropdownOption(
                    key="Disponible",
                    text="Disponible"
                ),
                ft.DropdownOption(
                    key="Prestado",
                    text="Prestado"
                )
            ],
            value="Todos",
            on_select=self.cambiar_filtro
        )

        # Mensaje para el usuario
        self.mensaje = ft.Text("")

        # Contadores
        self.total_libros = ft.Text(
            "Total: 0",
            weight=ft.FontWeight.BOLD
        )

        self.total_disponibles = ft.Text(
            "Disponibles: 0",
            weight=ft.FontWeight.BOLD
        )

        self.total_prestados = ft.Text(
            "Prestados: 0",
            weight=ft.FontWeight.BOLD
        )

        # Lista donde aparecerán los libros
        self.lista_libros = ft.ListView(
            expand=True,
            spacing=10
        )

        # Variables de búsqueda y filtro
        self.texto_busqueda = ""
        self.estado_filtro = "Todos"

        # Mostrar información inicial
        self.actualizar_lista()

    # ==========================================================
    # OBTENER DATOS DEL LIBRO
    # ==========================================================

    def obtener_valor(self, libro, atributo, defecto=""):
        """
        Permite trabajar tanto con diccionarios como con objetos.
        """

        if isinstance(libro, dict):
            return libro.get(atributo, defecto)

        return getattr(libro, atributo, defecto)

    # ==========================================================
    # REGISTRAR LIBRO
    # ==========================================================

    def registrar_libro(self, e):

        titulo = self.txt_titulo.value.strip()
        autor = self.txt_autor.value.strip()
        isbn = self.txt_isbn.value.strip()

        # Validar campos vacíos
        if not titulo or not autor or not isbn:
            self.mostrar_mensaje(
                "Debe completar todos los campos.",
                True
            )
            return

        # Validar ISBN repetido
        for libro in self.libros:

            isbn_existente = self.obtener_valor(
                libro,
                "isbn"
            )

            if str(isbn_existente).strip().lower() == isbn.lower():

                self.mostrar_mensaje(
                    "Ya existe un libro con ese ISBN.",
                    True
                )

                return

        # Crear nuevo libro
        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "isbn": isbn,
            "estado": "Disponible",
            "cliente": None
        }

        # Agregar libro a la lista
        self.libros.append(nuevo_libro)

        # Limpiar campos
        self.txt_titulo.value = ""
        self.txt_autor.value = ""
        self.txt_isbn.value = ""

        # Mostrar mensaje
        self.mostrar_mensaje(
            "Libro registrado correctamente.",
            False
        )

        # Actualizar la lista
        self.actualizar_lista()

    # ==========================================================
    # BUSCAR LIBRO
    # ==========================================================

    def buscar_libro(self, e):

        self.texto_busqueda = (
            self.txt_buscar.value.strip().lower()
        )

        self.actualizar_lista()

    # ==========================================================
    # CAMBIAR FILTRO
    # ==========================================================

    def cambiar_filtro(self, e):

        self.estado_filtro = self.filtro_estado.value

        self.actualizar_lista()

    # ==========================================================
    # CREAR TARJETA DE LIBRO
    # ==========================================================

    def crear_tarjeta_libro(self, libro):

        titulo = self.obtener_valor(
            libro,
            "titulo",
            "Sin título"
        )

        autor = self.obtener_valor(
            libro,
            "autor",
            "Sin autor"
        )

        isbn = self.obtener_valor(
            libro,
            "isbn",
            "Sin ISBN"
        )

        estado = self.obtener_valor(
            libro,
            "estado",
            "Disponible"
        )

        cliente = self.obtener_valor(
            libro,
            "cliente",
            None
        )

        informacion = [
            ft.Text(
                titulo,
                size=18,
                weight=ft.FontWeight.BOLD
            ),

            ft.Text(
                f"Autor: {autor}"
            ),

            ft.Text(
                f"ISBN: {isbn}"
            ),

            ft.Text(
                f"Estado: {estado}",
                weight=ft.FontWeight.BOLD
            )
        ]

        # Mostrar cliente si el libro está prestado
        if cliente:
            informacion.append(
                ft.Text(
                    f"Prestado a: {cliente}"
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=informacion,
                    spacing=5
                ),
                padding=15
            )
        )

    # ==========================================================
    # ACTUALIZAR LISTA DE LIBROS
    # ==========================================================

    def actualizar_lista(self):

        self.lista_libros.controls.clear()

        disponibles = 0
        prestados = 0

        for libro in self.libros:

            titulo = str(
                self.obtener_valor(
                    libro,
                    "titulo",
                    ""
                )
            )

            autor = str(
                self.obtener_valor(
                    libro,
                    "autor",
                    ""
                )
            )

            isbn = str(
                self.obtener_valor(
                    libro,
                    "isbn",
                    ""
                )
            )

            estado = str(
                self.obtener_valor(
                    libro,
                    "estado",
                    "Disponible"
                )
            )

            # Contar libros
            if estado == "Disponible":
                disponibles += 1

            elif estado == "Prestado":
                prestados += 1

            # Aplicar filtro
            if (
                self.estado_filtro != "Todos"
                and estado != self.estado_filtro
            ):
                continue

            # Aplicar búsqueda
            texto = f"{titulo} {autor} {isbn}".lower()

            if (
                self.texto_busqueda
                and self.texto_busqueda not in texto
            ):
                continue

            # Agregar libro a la lista
            self.lista_libros.controls.append(
                self.crear_tarjeta_libro(libro)
            )

        # Actualizar contadores
        self.total_libros.value = (
            f"Total: {len(self.libros)}"
        )

        self.total_disponibles.value = (
            f"Disponibles: {disponibles}"
        )

        self.total_prestados.value = (
            f"Prestados: {prestados}"
        )

        # Si no hay resultados
        if len(self.lista_libros.controls) == 0:

            self.lista_libros.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No se encontraron libros."
                    ),
                    padding=20
                )
            )

        self.lista_libros.update()

    # ==========================================================
    # MOSTRAR MENSAJE
    # ==========================================================

    def mostrar_mensaje(self, texto, error=False):

        self.mensaje.value = texto

        if error:
            self.mensaje.color = ft.Colors.RED
        else:
            self.mensaje.color = ft.Colors.GREEN

        self.mensaje.update()

    # ==========================================================
    # CONSTRUIR VISTA
    # ==========================================================

    def construir(self):

        formulario = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[

                        ft.Text(
                            "Registrar nuevo libro",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Row(
                            controls=[
                                self.txt_titulo,
                                self.txt_autor
                            ]
                        ),

                        ft.Row(
                            controls=[
                                self.txt_isbn,

                                ft.Button(
                                    content="Registrar libro",
                                    icon=ft.Icons.ADD,
                                    on_click=self.registrar_libro
                                )
                            ]
                        ),

                        self.mensaje
                    ],
                    spacing=12
                ),
                padding=20
            )
        )

        filtros = ft.Row(
            controls=[
                self.txt_buscar,
                self.filtro_estado
            ]
        )

        estadisticas = ft.Row(
            controls=[
                self.total_libros,
                self.total_disponibles,
                self.total_prestados
            ],
            spacing=25
        )

        return ft.Column(
            controls=[

                ft.Text(
                    "Gestión de Libros",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Registre y consulte el inventario "
                    "de libros de la biblioteca."
                ),

                formulario,

                estadisticas,

                filtros,

                ft.Text(
                    "Inventario de libros",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                self.lista_libros
            ],

            expand=True,
            spacing=15
        )
