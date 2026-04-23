from fastapi import FastAPI, HTTPException, Depends

from fastapi.responses import HTMLResponse

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

# 1. Configuración de la Base de Datos
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Modelo
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
@app.get("/")
def read_root():
    return {
        "sistema": "Gestión de Entregas - Motorizados",
        "desarrollador": "Oscar Mamani Pilco",
        "estado": "Servidor en la Nube (DigitalOcean) Operativo",
        "version": "1.0.2",
        "ubicacion": "Puno, Perú"
    }
"""
"""

@app.get("/", response_class=HTMLResponse) # <--- Le decimos que responderá HTML
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestión de Entregas - Oscar</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 max-w-md w-full text-center">
            <h1 class="text-3xl font-bold text-blue-400 mb-4">🚀 Sistema de Entregas</h1>
            <p class="text-slate-400 mb-6 text-lg">Bienvenido al centro de control de motorizados.</p>
            
            <div class="space-y-4 text-left bg-slate-900/50 p-6 rounded-lg border border-slate-700">
                <div class="flex justify-between">
                    <span class="text-slate-500">Desarrollador:</span>
                    <span class="font-medium">Oscar Mamani Pilco</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-500">Estado:</span>
                    <span class="text-green-400 font-bold uppercase text-sm flex items-center">
                        <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span> En Línea
                    </span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-500">Ubicación:</span>
                    <span class="font-medium italic">Puno, Perú</span>
                </div>
            </div>

            <div class="mt-8">
                <a href="/docs" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105">
                    Ir al Panel de Control
                </a>
            </div>
            
            <p class="mt-8 text-xs text-slate-500">Versión 1.2.0 • DigitalOcean Production</p>
        </div>
    </body>
    </html>
    """
"""
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Control de Logística - Oscar</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans">
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 max-w-2xl w-full">
                <header class="text-center mb-8">
                    <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 mb-2">
                        Panel de Entregas
                    </h1>
                    <p class="text-slate-400">Logística de Motorizados • Puno, Perú</p>
                </header>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-slate-900/50 p-6 rounded-xl border border-slate-700">
                        <h2 class="text-blue-400 font-bold mb-2">Estado del Servidor</h2>
                        <p class="text-2xl font-mono text-green-400">ONLINE</p>
                    </div>
                    <div class="bg-slate-900/50 p-6 rounded-xl border border-slate-700">
                        <h2 class="text-emerald-400 font-bold mb-2">Versión de App</h2>
                        <p class="text-2xl font-mono text-white">v1.3.0</p>
                    </div>
                </div>

                <div class="space-y-4 mb-8">
                    <h3 class="text-slate-300 font-semibold border-b border-slate-700 pb-2">Accesos Directos</h3>
                    <div class="flex flex-wrap gap-4">
                        <a href="/items/" class="flex-1 text-center bg-slate-700 hover:bg-slate-600 p-4 rounded-lg transition">
                            📦 Ver Pedidos
                        </a>
                        <a href="/docs" class="flex-1 text-center bg-blue-600 hover:bg-blue-500 p-4 rounded-lg transition font-bold">
                            ➕ Registrar Nuevo
                        </a>
                    </div>
                </div>

                <footer class="text-center text-xs text-slate-500 border-t border-slate-700 pt-6">
                    Desarrollado por <span class="text-slate-300 font-medium">Oscar Mamani Pilco</span> • Desplegado en DigitalOcean
                </footer>
            </div>
        </div>
    </body>
    </html>
    """
@app.post("/items/")
def crear_item(nombre: str, descripcion: str, db: Session = Depends(get_db)):
    nuevo = ItemDB(nombre=nombre, descripcion=descripcion)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/items/")
def listar_items(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()
