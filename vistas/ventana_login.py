import flet as ft
import sqlite3
from data.database import get_connection
from vistas.ventana_menu import menu_view

def login_view(page: ft.Page):
    page.clean()
    
    # Configurar el color de fondo de la ventana
    page.bgcolor = ft.colors.SURFACE_VARIANT
    
    usuario_input = ft.TextField(label="Usuario", width=300)
    pass_input = ft.TextField(label="Contraseña", password=True, width=300, can_reveal_password=True)
    mensaje_error = ft.Text("", color=ft.colors.ERROR)

    def iniciar_sesion(e):
        usuario = usuario_input.value
        contraseña = pass_input.value
        
        if not usuario or not contraseña:
            mensaje_error.value = "Por favor, complete todos los campos."
            page.update()
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                # Crear la notificación de bienvenida
                snack = ft.SnackBar(
                    content=ft.Text(f"¡Bienvenido {usuario}!", size=16, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.GREEN_400,
                    duration=2000  # Duración en milisegundos
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()
                
                # Esperar un momento para que el usuario vea el mensaje y luego ir al menú
                import threading
                def ir_al_menu():
                    import time
                    time.sleep(1.5)
                    menu_view(page)
                
                threading.Thread(target=ir_al_menu).start()
                
            else:
                mensaje_error.value = "Usuario o contraseña incorrectos."
                page.update()
                
        except Exception as error:
            mensaje_error.value = f"Error de conexión: {error}"
            page.update()

    btn_login = ft.ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion, width=300)

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Iniciar Sesión", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE_VARIANT),
                ft.Container(height=20), # Espacio
                usuario_input,
                pass_input,
                ft.Container(height=10),
                btn_login,
                ft.Container(height=10),
                mensaje_error
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    )