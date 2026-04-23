from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime # <--- Nueva importación para la hora
import pytz # <--- Para manejar la hora de Perú

# 1. Configuración de la Base de Datos
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Modelo Actualizado
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    # Nueva columna: se guarda automáticamente al crear el registro
    hora = Column(String, default=lambda: datetime.now(pytz.timezone('America/Lima')).strftime("%H:%M:%S"))

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- VISTAS HTML ---

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel de Logística - Oscar</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center min-h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 max-w-md w-full text-center">
            <h1 class="text-3xl font-bold text-blue-400 mb-6">🚀 Sistema Puno Entregas</h1>
            <div class="space-y-4">
                <a href="/ver-pedidos" class="block w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-6 rounded-lg transition">
                    📦 Ver Tabla de Pedidos
                </a>
                <a href="/docs" class="block w-full bg-slate-700 hover:bg-slate-600 text-white py-3 px-6 rounded-lg transition">
                    ➕ Registrar en Consola
                </a>
            </div>
            <p class="mt-8 text-xs text-slate-500 italic">Desarrollador: Oscar Mamani Pilco • v1.5.0</p>
        </div>
    </body>
    </html>
    """

@app.get("/ver-pedidos", response_class=HTMLResponse)
def ver_pedidos(db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    
    filas_html = ""
    for item in items:
        # Si el item es viejo y no tiene hora, ponemos "N/A"
        hora_display = item.hora if hasattr(item, 'hora') and item.hora else "--:--:--"
        filas_html += f"""
        <tr class="border-b border-slate-700 hover:bg-slate-700/50 transition">
            <td class="px-6 py-4 font-medium text-blue-300">#{item.id}</td>
            <td class="px-6 py-4 text-slate-200">{item.nombre}</td>
            <td class="px-6 py-4 text-slate-400">{item.descripcion}</td>
            <td class="px-6 py-4 text-emerald-400 font-mono text-sm">{hora_display}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Listado de Pedidos</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans p-4 md:p-10">
        <div class="max-w-5xl mx-auto">
            <div class="flex justify-between items-center mb-8">
                <h1 class="text-3xl font-bold text-blue-400">Relación de Entregas</h1>
                <a href="/" class="text-slate-400 hover:text-white transition">← Volver</a>
            </div>
            
            <div class="bg-slate-800 rounded-xl shadow-xl overflow-hidden border border-slate-700">
                <table class="w-full text-left">
                    <thead class="bg-slate-700/50 text-slate-300 uppercase text-xs">
                        <tr>
                            <th class="px-6 py-4">ID</th>
                            <th class="px-6 py-4">Motorizado</th>
                            <th class="px-6 py-4">Descripción</th>
                            <th class="px-6 py-4">Hora (PE)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_html if filas_html else '<tr><td colspan="4" class="text-center py-10">Sin pedidos.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

# Endpoints de API
@app.post("/items/")
def crear_item(nombre: str, descripcion: str, db: Session = Depends(get_db)):
    nuevo = ItemDB(nombre=nombre, descripcion=descripcion)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo