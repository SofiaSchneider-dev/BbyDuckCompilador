def error_semantico(mensaje, linea=None):
    """Lanza un error semántico. Si se sabe la línea, se agrega al mensaje."""
    if linea is None:
        raise Exception("Error semántico: " + mensaje)
    raise Exception(f"Error semántico en línea {linea}: {mensaje}")
