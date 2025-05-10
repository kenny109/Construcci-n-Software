def clean_file(file_path):
    # Leer el archivo en modo binario
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Eliminar bytes nulos
    clean_content = content.replace(b'\x00', b'')
    
    # Escribir el contenido limpio de vuelta al archivo
    with open(file_path, 'wb') as file:
        file.write(clean_content)
    
    print(f"Limpieza completada. Se eliminaron {len(content) - len(clean_content)} bytes nulos.")

if __name__ == "__main__":
    # Ruta al archivo que contiene bytes nulos
    file_path = "app/models/models.py"
    clean_file(file_path)