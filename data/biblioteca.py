from typing import Optional, List, Dict
from .modelos import Libro, Cliente

class Biblioteca:
    def __init__(self):
        self.libros: List[Libro] = []
        self.clientes: List[Cliente] = []
        self.prestamos: Dict[str, str] = {}

    # ---------- METODOS PARA LIBROS ----------
    
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> bool:
        if self.buscar_libro_por_isbn(isbn):
            return False
        self.libros.append(Libro(titulo=titulo, autor=autor, isbn=isbn))
        return True

    def buscar_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def obtener_libros_disponibles(self) -> List[Libro]:
        return [l for l in self.libros if l.estado == "Disponible"]

    def obtener_libros_prestados(self) -> List[Libro]:
        return [l for l in self.libros if l.estado == "Prestado"]

    # ---------- METODOS PARA CLIENTES ----------
    
    def agregar_cliente(self, nombre: str, apellido: str, cedula: str) -> bool:
        if self.buscar_cliente_por_cedula(cedula):
            return False
        self.clientes.append(Cliente(nombre=nombre, apellido=apellido, cedula=cedula))
        return True

    def buscar_cliente_por_cedula(self, cedula: str) -> Optional[Cliente]:
        for cliente in self.clientes:
            if cliente.cedula == cedula:
                return cliente
        return None

    def obtener_libros_de_cliente(self, cedula: str) -> List[Libro]:
        return [l for l in self.libros if l.cliente_asignado == cedula]

    # ---------- METODOS PARA PRESTAMOS ----------
    
    def prestar_libro(self, isbn: str, cedula_cliente: str) -> bool:
        libro = self.buscar_libro_por_isbn(isbn)
        cliente = self.buscar_cliente_por_cedula(cedula_cliente)
        
        if not libro or not cliente:
            return False
        if libro.estado != "Disponible":
            return False
        
        libro.estado = "Prestado"
        libro.cliente_asignado = cedula_cliente
        self.prestamos[isbn] = cedula_cliente
        return True

    def devolver_libro(self, isbn: str) -> bool:
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro or libro.estado != "Prestado":
            return False
        
        libro.estado = "Disponible"
        libro.cliente_asignado = None
        if isbn in self.prestamos:
            del self.prestamos[isbn]
        return True