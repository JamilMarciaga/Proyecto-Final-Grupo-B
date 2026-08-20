import flet as ft
from vistas.vista_libros import VistaLibros
from vistas.vista_clientes import VistaClientes
from vistas.vista_prestamos import VistaPrestamos

def crear_contenido_menu(page):
    titulo = ft.Text("Menú Principal", size=30, weight=ft.FontWeight.BOLD)
    
    def abrir_libros(e):
        page.clean()
        vista = VistaLibros(page, page.libros)
        page.add(vista.construir())
        page.update()
        vista.actualizar_lista()

    def abrir_clientes(e):
        page.clean()
        vista = VistaClientes(page, page.clientes)
        page.add(vista.construir())
        page.update()
        vista.actualizar_lista()

    def abrir_prestamos(e):
        page.clean()
        page.add(VistaPrestamos(page, page.libros, page.clientes).construir())
        page.update()

    def cerrar_sesion(e):
        page.window_close()

    btn_clientes = ft.ElevatedButton("Gestión de Clientes", width=250, icon=ft.icons.PEOPLE, on_click=abrir_clientes)
    btn_libros = ft.ElevatedButton("Gestión de Libros", width=250, icon=ft.icons.BOOK, on_click=abrir_libros)
    btn_prestamos = ft.ElevatedButton("Gestión de Préstamos", width=250, icon=ft.icons.LIBRARY_BOOKS, on_click=abrir_prestamos)
    btn_salir = ft.ElevatedButton("Cerrar Sesión", on_click=cerrar_sesion, color="white", bgcolor=ft.colors.RED, width=250, icon=ft.icons.LOGOUT)

    return ft.Column([
        ft.Container(content=titulo, padding=ft.padding.only(bottom=20)),
        btn_clientes,
        btn_libros,
        btn_prestamos,
        ft.Container(height=20),
        btn_salir
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

def menu_view(page: ft.Page):
    page.clean()
    
    def volver_al_menu(e):
        page.clean()
        page.add(crear_contenido_menu(page))
        page.update()

    page.volver_al_menu = volver_al_menu
    page.add(crear_contenido_menu(page))