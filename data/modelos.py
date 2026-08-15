from dataclasses import dataclass
from typing import Optional

@dataclass
class Libro:
    titulo: str
    autor: str
    isbn: str
    estado: str = "Disponible"
    cliente_asignado: Optional[str] = None

@dataclass
class Cliente:
    nombre: str
    apellido: str
    cedula: str