import flet as ft

class VistaClientes:
    def __init__(self, biblioteca, page):
        self.biblioteca = biblioteca
        self.page = page

        self.txt_nombre = ft.TextField(label="Nombre", expand=True)
        self.txt_apellido = ft.TextField(label="Apellido", expand=True)
        self.txt_cedula = ft.TextField(label="Cédula/ID", expand=True)
        
        self.mensaje = ft.Text("")
        self.lista_clientes = ft.ListView(expand=True, spacing=10)

    def registrar_cliente(self, e):
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        cedula = self.txt_cedula.value.strip()

        if not nombre or not apellido or not cedula:
            self.mensaje.value = "Todos los campos son obligatorios."
            self.mensaje.color = ft.colors.RED
            self.mensaje.update()
            return

        exito = self.biblioteca.agregar_cliente(nombre, apellido, cedula)
        
        if not exito:
            self.mensaje.value = "Ya existe un cliente con esa Cédula."
            self.mensaje.color = ft.colors.RED
            self.mensaje.update()
            return

        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_cedula.value = ""
        
        self.mensaje.value = "Cliente registrado correctamente."
        self.mensaje.color = ft.colors.GREEN
        self.mensaje.update()
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_clientes.controls.clear()
        for cliente in self.biblioteca.clientes:
            self.lista_clientes.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{cliente.nombre} {cliente.apellido}"),
                    subtitle=ft.Text(f"Cédula: {cliente.cedula}")
                )
            )
        self.lista_clientes.update()

    def construir(self):
        formulario = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Registrar Cliente", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([self.txt_nombre, self.txt_apellido]),
                    ft.Row([self.txt_cedula, ft.ElevatedButton("Registrar", on_click=self.registrar_cliente)]),
                    self.mensaje
                ], spacing=10),
                padding=20
            )
        )
        
        return ft.Column([
            ft.Text("Gestión de Clientes", size=28, weight=ft.FontWeight.BOLD),
            formulario,
            ft.Text("Lista de Clientes", size=20, weight=ft.FontWeight.BOLD),
            self.lista_clientes,
        ], expand=True, spacing=15)