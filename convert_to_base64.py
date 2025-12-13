import base64

# RUTA A TU IMAGEN
path = r"C:\Users\acarreton\OneDrive - Analistas Financieros Internacionales (Afi)\Desktop\Máster Data Engineering\PC3\imagenes\gatito.jpg"

with open(path, "rb") as f:
    b = f.read()

b64 = base64.b64encode(b).decode("utf-8")

# Guardar el base64 en un archivo
with open("base64_output.txt", "w") as out:
    out.write(b64)

print("Base64 guardado en base64_output.txt")
