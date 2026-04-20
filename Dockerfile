# 1. Traemos una computadora limpia con Python 3.11 ya instalado
FROM python:3.11-slim

# 2. Creamos una carpeta de trabajo dentro de esa computadora virtual
WORKDIR /code

# 3. LA CONEXIÓN: Copiamos tu lista de requisitos desde tu Windows/WSL al contenedor
COPY ./app/requirements.txt /code/requirements.txt

# 4. LA ACCIÓN: Le decimos al sistema que instale todo lo que dice esa lista
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiamos el resto de tu código (tu CRUD) al contenedor
COPY ./app /code

# 6. El comando final para que la app empiece a funcionar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
