# Proyecto-Final-Grupo-B - Sistema de Control de Biblioteca

## Descripcion del Proyecto

Aplicacion de escritorio para la gestion de una pequeña biblioteca, desarrollada con Python y Flet como proyecto final del modulo.

El sistema permite:
- Gestionar el inventario de libros (registro, listado, estado)
- Gestionar clientes (registro, listado)
- Realizar prestamos y devoluciones de libros
- Visualizar prestamos activos

---

## Integrantes del Grupo B

| # | Nombre | Rol | Modulo |
|---|--------|-----|--------|
| 1 | Jamil Marciaga | Lider / Coordinador | Modelos de Datos y main.py |
| 2 | Gilberto Cano | Desarrollador | Vista de Libros |
| 3 | Esequiel Gonzalez | Desarrollador | Vista de Clientes |
| 4 | Alexis Gonzalez | Desarrollador | Vista de Prestamos |

---

## Tecnologias Utilizadas

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje de programacion |
| Flet | 0.21.2 | Framework para interfaz grafica |
| Git | Ultima | Control de versiones |
| GitHub | - | Repositorio remoto |

---

## Funcionalidades Implementadas

### 1. Gestion de Libros
- Registro de libros con: Titulo, Autor e ISBN
- Listado dinamico con estado: Disponible o Prestado
- Visualizacion del cliente asignado si esta prestado
- Validacion de ISBN unico

### 2. Gestion de Clientes
- Registro de clientes con: Nombre, Apellido y Cedula
- Listado de clientes con conteo de libros prestados
- Validacion de cedula unica

### 3. Gestion de Prestamos
- Prestamo de libros disponibles a clientes registrados
- Devolucion de libros prestados
- Lista de prestamos activos
- Validaciones para evitar prestamos incorrectos

---

## Como Ejecutar la Aplicacion

### Requisitos Previos
- Python 3.8 o superior
- Git (opcional, para clonar)

### Instalacion y Ejecucion

```bash
# 1. Clonar el repositorio
git clone https://github.com/JamilMarciaga/Proyecto-Final-Grupo-B.git
cd Proyecto-Final-Grupo-B

# 2. Crear y activar entorno virtual (recomendado)
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
python main.py