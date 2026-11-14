"""
Clase Cliente: encapsula los datos personales y los valida de forma estricta.
"""

import re                                        # Expresiones regulares para validar formatos

from .entidad import EntidadBase
from .excepciones import ClienteInvalidoError, ParametroFaltanteError

# Patrones de validacion (se compilan una sola vez)
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}$")    # Solo letras y espacios
PATRON_DOCUMENTO = re.compile(r"^\d{6,12}$")                      # Solo digitos, 6 a 12
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")         # usuario@dominio.ext
PATRON_TELEFONO = re.compile(r"^\d{7,10}$")                       # 7 a 10 digitos


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus atributos son privados (_nombre, _documento...)."""

    prefijo = "CLI"                              # Los IDs seran CLI-001, CLI-002, ...

    def __init__(self, nombre, documento, correo, telefono):
        # Cada asignacion pasa por el setter correspondiente, que valida el dato.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        super().__init__()                       # Genera el ID solo si todo fue valido

    # ---------- Validaciones auxiliares ----------
    @staticmethod
    def _texto_obligatorio(valor, campo):
        """Verifica que el dato exista y sea un texto no vacio."""
        if valor is None:                                            # No se entrego el dato
            raise ParametroFaltanteError(f"Falta el dato obligatorio: {campo}.")
        if not isinstance(valor, str):                               # Tipo incorrecto
            raise ClienteInvalidoError(f"{campo} debe ser texto, se recibio {type(valor).__name__}.")
        valor = valor.strip()                                        # Quita espacios sobrantes
        if not valor:                                                # Texto vacio
            raise ClienteInvalidoError(f"{campo} no puede estar vacio.")
        return valor

    # ---------- Propiedades (getters y setters) ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._texto_obligatorio(valor, "nombre")
        if not PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(f"Nombre invalido: '{valor}' (solo letras, 3 a 60 caracteres).")
        self._nombre = valor.title()                                 # Guarda con formato Nombre Apellido

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = self._texto_obligatorio(valor, "documento")
        if not PATRON_DOCUMENTO.match(valor):
            raise ClienteInvalidoError(f"Documento invalido: '{valor}' (solo numeros, 6 a 12 digitos).")
        self._documento = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = self._texto_obligatorio(valor, "correo")
        if not PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo invalido: '{valor}'.")
        self._correo = valor.lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._texto_obligatorio(valor, "telefono")
        if not PATRON_TELEFONO.match(valor):
            raise ClienteInvalidoError(f"Telefono invalido: '{valor}' (7 a 10 digitos).")
        self._telefono = valor

    # ---------- Metodo abstracto implementado ----------
    def describir(self):
        return f"[{self.id}] {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
