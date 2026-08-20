import flet as ft


class VistaClientes:
    """
    Vista para gestionar el registro y listado de clientes.

    Trabaja con la clase Biblioteca definida en data/biblioteca.py:
    - agregar_cliente()
    - buscar_cliente_por_cedula()
    - obtener_libros_de_cliente()
    """

    def __init__(self, biblioteca, page):
        self.biblioteca = biblioteca
        self.page = page

        # Callback utilizado para actualizar otras vistas,
        # especialmente la lista de clientes de Préstamos.
        self.callback_actualizar = None

        # ==========================================================
        # CAMPOS DEL FORMULARIO
        # ==========================================================

        self.txt_nombre = ft.TextField(
            label="Nombre",
            hint_text="Ingrese el nombre",
            expand=True,
        )

        self.txt_apellido = ft.TextField(
            label="Apellido",
            hint_text="Ingrese el apellido",
            expand=True,
        )

        self.txt_cedula = ft.TextField(
            label="Cédula / ID",
            hint_text="Ingrese la cédula",
            expand=True,
        )

        # Campo para buscar clientes
        self.txt_buscar = ft.TextField(
            label="Buscar cliente",
            hint_text="Nombre, apellido o cédula",
            prefix_icon=ft.icons.SEARCH,
            on_change=self.buscar_clientes,
            expand=True,
        )

        # Mensajes de validación
        self.mensaje = ft.Text("")

        # Indicador de clientes registrados
        self.total_clientes = ft.Text(
            "Clientes registrados: 0",
            weight=ft.FontWeight.BOLD,
        )

        # Lista visual de clientes
        self.lista_clientes = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

    # ==========================================================
    # UTILIDADES
    # ==========================================================

    def _mostrar_mensaje(self, texto, error=False):
        self.mensaje.value = texto

        if error:
            self.mensaje.color = ft.colors.RED
        else:
            self.mensaje.color = ft.colors.GREEN

        self.page.update()

    def _limpiar_campos(self):
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_cedula.value = ""

    # ==========================================================
    # REGISTRO DE CLIENTES
    # ==========================================================

    def registrar_cliente(self, e):
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        cedula = self.txt_cedula.value.strip()

        # Validar campos vacíos
        if not nombre or not apellido or not cedula:
            self._mostrar_mensaje(
                "Debe completar todos los campos.",
                True,
            )
            return

        # Intentar registrar el cliente utilizando Biblioteca
        agregado = self.biblioteca.agregar_cliente(
            nombre,
            apellido,
            cedula,
        )

        if not agregado:
            self._mostrar_mensaje(
                "Ya existe un cliente registrado con esta cédula.",
                True,
            )
            return

        self._limpiar_campos()

        self.mensaje.value = (
            f"Cliente registrado correctamente: "
            f"{nombre} {apellido}."
        )
        self.mensaje.color = ft.colors.GREEN

        # Actualizar listado de clientes
        self._cargar_clientes()

        # Actualizar la Vista de Préstamos
        if self.callback_actualizar:
            self.callback_actualizar()
        else:
            self.page.update()

    # ==========================================================
    # LISTADO Y BÚSQUEDA
    # ==========================================================

    def _cargar_clientes(self, filtro=""):
        self.lista_clientes.controls.clear()

        clientes = self.biblioteca.clientes

        filtro = filtro.lower().strip()

        if filtro:
            clientes = [
                cliente
                for cliente in clientes
                if filtro in cliente.nombre.lower()
                or filtro in cliente.apellido.lower()
                or filtro in cliente.cedula.lower()
            ]

        self.total_clientes.value = (
            f"Clientes registrados: "
            f"{len(self.biblioteca.clientes)}"
        )

        # Si no existen clientes
        if not clientes:
            self.lista_clientes.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                ft.icons.PERSON_SEARCH,
                                size=42,
                                color=ft.colors.BLUE_GREY_400,
                            ),
                            ft.Text(
                                "No hay clientes para mostrar.",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Los clientes registrados "
                                "aparecerán aquí."
                            ),
                        ],
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                    ),
                    alignment=ft.alignment.center,
                    padding=30,
                )
            )
            return

        # Mostrar clientes registrados
        for cliente in clientes:
            libros_prestados = (
                self.biblioteca.obtener_libros_de_cliente(
                    cliente.cedula
                )
            )

            cantidad_prestados = len(libros_prestados)

            self.lista_clientes.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.icons.PERSON,
                                    size=35,
                                    color=ft.colors.BLUE_700,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            f"{cliente.nombre} "
                                            f"{cliente.apellido}",
                                            size=18,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                        ft.Text(
                                            f"Cédula / ID: "
                                            f"{cliente.cedula}"
                                        ),
                                        ft.Text(
                                            f"Libros prestados: "
                                            f"{cantidad_prestados}"
                                        ),
                                    ],
                                    expand=True,
                                    spacing=4,
                                ),
                            ],
                        ),
                        padding=15,
                    )
                )
            )

    def buscar_clientes(self, e):
        self._cargar_clientes(
            self.txt_buscar.value
        )
        self.page.update()

    def actualizar_clientes(self, e=None):
        self.txt_buscar.value = ""
        self._cargar_clientes()
        self.page.update()

    # ==========================================================
    # CONSTRUCCIÓN DE LA VISTA
    # ==========================================================

    def crear(self):
        # Cargar información inicial antes de montar la vista.
        self._cargar_clientes()

        formulario = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Registrar nuevo cliente",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Row(
                            controls=[
                                self.txt_nombre,
                                self.txt_apellido,
                                self.txt_cedula,
                            ]
                        ),

                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Registrar cliente",
                                    icon=ft.icons.PERSON_ADD,
                                    on_click=self.registrar_cliente,
                                ),

                                ft.OutlinedButton(
                                    text="Actualizar datos",
                                    icon=ft.icons.REFRESH,
                                    on_click=(
                                        self.actualizar_clientes
                                    ),
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

        buscador = ft.Row(
            controls=[
                self.txt_buscar,
                self.total_clientes,
            ],
            vertical_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
        )

        return ft.Column(
            controls=[
                ft.Text(
                    "Gestión de Clientes",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Registre y consulte los clientes del "
                    "Sistema de Control de Biblioteca."
                ),

                formulario,
                buscador,

                ft.Text(
                    "Clientes registrados",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                self.lista_clientes,
            ],
            expand=True,
            spacing=15,
        )

    # Alias por compatibilidad con otras vistas del proyecto.
    construir = crear