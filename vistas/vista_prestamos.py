import flet as ft


class VistaPrestamos:
    """
    Vista para gestionar préstamos y devoluciones de libros.

    Trabaja con la clase Biblioteca definida en data/biblioteca.py:
    - obtener_libros_disponibles()
    - obtener_libros_prestados()
    - buscar_cliente_por_cedula()
    - prestar_libro()
    - devolver_libro()
    """

    def __init__(self, biblioteca, page):
        self.biblioteca = biblioteca
        self.page = page

        # Selección para registrar un préstamo
        self.dd_libro = ft.Dropdown(
            label="Libro disponible",
            hint_text="Seleccione un libro",
            expand=True,
            options=[],
        )

        self.dd_cliente = ft.Dropdown(
            label="Cliente",
            hint_text="Seleccione un cliente",
            expand=True,
            options=[],
        )

        self.mensaje = ft.Text("")

        # Indicadores
        self.total_activos = ft.Text(
            "Préstamos activos: 0",
            weight=ft.FontWeight.BOLD,
        )

        self.total_disponibles = ft.Text(
            "Libros disponibles: 0",
            weight=ft.FontWeight.BOLD,
        )

        self.total_clientes = ft.Text(
            "Clientes registrados: 0",
            weight=ft.FontWeight.BOLD,
        )

        # Lista de préstamos activos
        self.lista_prestamos = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

    # ==========================================================
    # UTILIDADES
    # ==========================================================

    def _mostrar_mensaje(self, texto, error=False):
        self.mensaje.value = texto
        self.mensaje.color = ft.colors.RED if error else ft.colors.GREEN
        self.page.update()

    def _nombre_cliente(self, cedula):
        cliente = self.biblioteca.buscar_cliente_por_cedula(cedula)

        if not cliente:
            return f"Cliente {cedula}"

        return f"{cliente.nombre} {cliente.apellido}"

    # ==========================================================
    # CARGA / ACTUALIZACIÓN DE CONTROLES
    # ==========================================================

    def _cargar_dropdowns(self):
        """
        Carga libros disponibles y clientes sin llamar page.update().
        Se usa durante la construcción inicial y también en refrescos.
        """
        libros = self.biblioteca.obtener_libros_disponibles()
        clientes = self.biblioteca.clientes

        valor_libro_actual = self.dd_libro.value
        valor_cliente_actual = self.dd_cliente.value

        self.dd_libro.options = [
            ft.dropdown.Option(
                key=libro.isbn,
                text=f"{libro.titulo} — {libro.autor} | ISBN: {libro.isbn}",
            )
            for libro in libros
        ]

        self.dd_cliente.options = [
            ft.dropdown.Option(
                key=cliente.cedula,
                text=f"{cliente.nombre} {cliente.apellido} | Cédula: {cliente.cedula}",
            )
            for cliente in clientes
        ]

        # Mantener selección solamente si todavía existe
        if valor_libro_actual not in [op.key for op in self.dd_libro.options]:
            self.dd_libro.value = None

        if valor_cliente_actual not in [op.key for op in self.dd_cliente.options]:
            self.dd_cliente.value = None

        self.total_disponibles.value = f"Libros disponibles: {len(libros)}"
        self.total_clientes.value = f"Clientes registrados: {len(clientes)}"

    def _cargar_prestamos(self):
        """
        Reconstruye la lista visual de préstamos activos.
        """
        self.lista_prestamos.controls.clear()

        prestamos = self.biblioteca.obtener_libros_prestados()
        self.total_activos.value = f"Préstamos activos: {len(prestamos)}"

        if not prestamos:
            self.lista_prestamos.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.icons.CHECK_CIRCLE_OUTLINE,
                                size=42,
                                color=ft.colors.GREEN_600,
                            ),
                            ft.Text(
                                "No hay préstamos activos.",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Los préstamos registrados aparecerán aquí."
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=30,
                )
            )
            return

        for libro in prestamos:
            cedula = libro.cliente_asignado
            cliente = self._nombre_cliente(cedula)

            self.lista_prestamos.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            libro.titulo,
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(f"Autor: {libro.autor}"),
                                        ft.Text(f"ISBN: {libro.isbn}"),
                                        ft.Text(
                                            f"Prestado a: {cliente} ({cedula})"
                                        ),
                                    ],
                                    expand=True,
                                    spacing=4,
                                ),
                                ft.ElevatedButton(
                                    text="Devolver",
                                    icon=ft.icons.KEYBOARD_RETURN,
                                    on_click=lambda e, isbn=libro.isbn: self.devolver_libro(
                                        isbn
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=15,
                    )
                )
            )

    def _refrescar_vista(self):
        self._cargar_dropdowns()
        self._cargar_prestamos()
        self.page.update()

    def _actualizar_dropdowns(self, e=None):
        """
        Método público usado desde main.py como callback cuando cambian
        los clientes. También puede utilizarse para refrescar manualmente
        los libros disponibles.
        """
        self._refrescar_vista()

    # ==========================================================
    # PRÉSTAMOS
    # ==========================================================

    def registrar_prestamo(self, e):
        isbn = self.dd_libro.value
        cedula = self.dd_cliente.value

        if not isbn or not cedula:
            self._mostrar_mensaje(
                "Debe seleccionar un libro disponible y un cliente.",
                True,
            )
            return

        libro = self.biblioteca.buscar_libro_por_isbn(isbn)
        cliente = self.biblioteca.buscar_cliente_por_cedula(cedula)

        if not libro:
            self._mostrar_mensaje(
                "El libro seleccionado ya no existe.",
                True,
            )
            self._refrescar_vista()
            return

        if not cliente:
            self._mostrar_mensaje(
                "El cliente seleccionado ya no existe.",
                True,
            )
            self._refrescar_vista()
            return

        if libro.estado != "Disponible":
            self._mostrar_mensaje(
                "El libro seleccionado ya se encuentra prestado.",
                True,
            )
            self._refrescar_vista()
            return

        prestado = self.biblioteca.prestar_libro(isbn, cedula)

        if not prestado:
            self._mostrar_mensaje(
                "No fue posible registrar el préstamo.",
                True,
            )
            return

        self.dd_libro.value = None
        self.dd_cliente.value = None
        self.mensaje.value = (
            f'Préstamo registrado: "{libro.titulo}" para '
            f"{cliente.nombre} {cliente.apellido}."
        )
        self.mensaje.color = ft.colors.GREEN

        self._refrescar_vista()

    # ==========================================================
    # DEVOLUCIONES
    # ==========================================================

    def devolver_libro(self, isbn):
        libro = self.biblioteca.buscar_libro_por_isbn(isbn)

        if not libro:
            self._mostrar_mensaje(
                "No se encontró el libro que desea devolver.",
                True,
            )
            return

        titulo = libro.titulo
        devuelto = self.biblioteca.devolver_libro(isbn)

        if not devuelto:
            self._mostrar_mensaje(
                "No fue posible procesar la devolución.",
                True,
            )
            return

        self.mensaje.value = f'Devolución registrada: "{titulo}".'
        self.mensaje.color = ft.colors.GREEN

        self._refrescar_vista()

    # ==========================================================
    # CONSTRUCCIÓN DE LA VISTA
    # ==========================================================

    def crear(self):
        # Cargar datos iniciales sin actualizar la página antes de montar.
        self._cargar_dropdowns()
        self._cargar_prestamos()

        formulario = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Registrar nuevo préstamo",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Row(
                            controls=[
                                self.dd_libro,
                                self.dd_cliente,
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Registrar préstamo",
                                    icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                    on_click=self.registrar_prestamo,
                                ),
                                ft.OutlinedButton(
                                    text="Actualizar datos",
                                    icon=ft.icons.REFRESH,
                                    on_click=self._actualizar_dropdowns,
                                ),
                            ]
                        ),
                        self.mensaje,
                    ],
                    spacing=12,
                ),
                padding=20,
            )
        )

        estadisticas = ft.Row(
            controls=[
                self.total_activos,
                self.total_disponibles,
                self.total_clientes,
            ],
            spacing=25,
        )

        return ft.Column(
            controls=[
                ft.Text(
                    "Préstamos y Devoluciones",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Asigne libros disponibles a clientes registrados "
                    "y gestione sus devoluciones."
                ),
                formulario,
                estadisticas,
                ft.Text(
                    "Préstamos activos",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                self.lista_prestamos,
            ],
            expand=True,
            spacing=15,
        )

    # Alias por compatibilidad si el equipo decide usar el nombre
    # construir() en todas las vistas.
    construir = crear
