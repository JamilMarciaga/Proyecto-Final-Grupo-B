import flet as ft

def main(page: ft.Page):
    page.title = "Mi Proyecto Grupo B"  # Ponerle título a la ventana
    page.window_width = 800             # Ancho de la ventana
    page.window_height = 600            # Alto de la ventana
    
    # Creamos controles
    titulo = ft.Text("¡Bienvenido al Sistema!", size=30, weight="bold")
    boton_agregar = ft.IconButton(ft.icons.ADD)
    boton_salir = ft.ElevatedButton("Salir", on_click=lambda _: page.window_close())

    # Los ponemos en una fila (uno al lado del otro)
    fila_botones = ft.Row([boton_agregar, boton_salir])

    # Agregamos todo a la página
    page.add(
        titulo,
        fila_botones
    )

ft.app(target=main)