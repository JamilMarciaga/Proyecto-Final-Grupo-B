import flet as ft
from data.biblioteca import Biblioteca
from vistas.vista_libros import VistaLibros
from vistas.vista_clientes import VistaClientes
from vistas.vista_prestamos import VistaPrestamos

def main(page: ft.Page):
    page.title = "Sistema de Control de Biblioteca - Grupo B"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 950
    page.window_height = 750

    biblioteca = Biblioteca()

    vista_libros = VistaLibros(biblioteca, page)
    vista_clientes = VistaClientes(biblioteca, page)
    vista_prestamos = VistaPrestamos(biblioteca, page)

    def al_cambiar_pestana(e):
        if e.control.selected_index == 2:
            vista_prestamos.actualizar_listas()
            page.update()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=al_cambiar_pestana,
        tabs=[
            ft.Tab(
                tab_content=ft.Row([ft.Icon(ft.icons.BOOK), ft.Text("Libros")]),
                content=vista_libros.construir()
            ),
            ft.Tab(
                tab_content=ft.Row([ft.Icon(ft.icons.PEOPLE), ft.Text("Clientes")]),
                content=vista_clientes.construir()
            ),
            ft.Tab(
                tab_content=ft.Row([ft.Icon(ft.icons.LOCAL_LIBRARY), ft.Text("Prestamos")]),
                content=vista_prestamos.construir()
            ),
        ],
        expand=True,
    )

    titulo = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.LIBRARY_BOOKS, size=40, color=ft.colors.BLUE_700),
            ft.Text("Sistema de Control de Biblioteca - Grupo B", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(bottom=15),
    )

    page.add(titulo, tabs)

if __name__ == "__main__":
    ft.app(target=main)