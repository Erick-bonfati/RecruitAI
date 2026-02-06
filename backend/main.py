from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import httpx
import json
from pypdf import PdfReader
from io import BytesIO
from pathlib import Path
from threading import Lock

app = FastAPI()

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistência simples em arquivo JSON
METRICAS_PATH = Path(__file__).parent / "data" / "metricas.json"
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
JOBS_FILE = DATA_DIR / "jobs.json"

_jobs_lock = Lock()


class Experiencia(BaseModel):
    empresa: Optional[str] = ""
    cargo: Optional[str] = ""
    periodo: Optional[str] = ""
    descricao: Optional[str] = ""

class Educacao(BaseModel):
    instituicao: Optional[str] = ""
    curso: Optional[str] = ""
    periodo: Optional[str] = ""

class Curriculo(BaseModel):
    nome: Optional[str] = ""
    email: Optional[str] = ""
    telefone: Optional[str] = ""
    linkedin: Optional[str] = ""
    skills: List[str] = []
    experiencias: List[Experiencia] = []
    educacao: List[Educacao] = []
    certificacoes: List[str] = []
    idiomas: List[str] = []

# Modelo de vaga
class Job(BaseModel):
    title: str
    description: str
    location: Optional[str] = "Remoto · Brasil"
    level: Optional[str] = "Pleno"
    area: Optional[str] = "tech"
    must: List[str] = []
    nice: List[str] = []
    tasks: List[str] = []
    yearsExp: Optional[int] = None
    seniority: Optional[str] = ""


def load_jobs() -> List[Job]:
    if not JOBS_FILE.exists():
        return []
    try:
        data = json.loads(JOBS_FILE.read_text(encoding="utf-8"))
        return [Job(**item) for item in data]
    except Exception as exc:
        print("Erro ao ler jobs.json:", exc)
        return []

def save_jobs(jobs: List[Job]) -> None:
    with _jobs_lock:
        JOBS_FILE.write_text(json.dumps([job.dict() for job in jobs], ensure_ascii=False, indent=2), encoding="utf-8")
        

# Extrair o texto do PDF

def extrair_texto_pdf(file_bytes: bytes) -> str:
    leitor = PdfReader(BytesIO(file_bytes))
    texto_pagina = []
    for pagina in leitor.pages:
        texto_pagina.append(pagina.extract_text() or "")
    return "\n".join(texto_pagina).strip()

# Chamar llama3 localmente

async def chamar_llama3(texto: str) -> dict:
    prompt = f"""
        Você é um extrator de currículo.
        Extraia as informações do texto abaixo e responda APENAS com JSON válido, sem explicações.

        Formato esperado:
        {{
        "nome": "",
        "email": "",
        "telefone": "",
        "linkedin": "",
        "skills": [],
        "experiencias": [{{ "empresa": "", "cargo": "", "periodo": "", "descricao": "" }}],
        "educacao": [{{ "instituicao": "", "curso": "", "periodo": "" }}],
        "certificacoes": [],
        "idiomas": []
        }}

        Texto do currículo:
        \"\"\"{texto}\"\"\"
    """
    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "temperature": 0,
            },
        )
        response.raise_for_status()
        dados = response.json()
        
        # Aqui estamos assumindo que a resposta contém um campo 'response' com o JSON desejado
        raw = dados.get("response", "").strip()
        print("Resposta bruta do Llama3:", raw)

        if not raw:
            raise HTTPException(status_code=500, detail="Nenhuma resposta do modelo Llama3")

        # Tenta converter a response em JSON
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Resposta inválida do modelo Llama3")

# Endpoint principal
@app.post("/extrair")
async def extrair_curriculo(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são suportados.")
    
    print("Novo currículo recebido:", file.filename)

    file_bytes = await file.read()
    texto = extrair_texto_pdf(file_bytes)

    print("Texto extraído, tamanho:", len(texto))

    if not texto:
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")
    
    print("Enviando para Llama3...")
    llm_json = await chamar_llama3(texto)

    # Validar JSON com Pydantic
    try:
        parsed = Curriculo(**llm_json)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"JSON inválido: {e}")
    
    print("JSON gerado com sucesso")
    return parsed

@app.get("/jobs", response_model=List[Job])
async def listar_jobs():
    return load_jobs()

@app.post("/jobs", response_model=Job)
async def criar_job(job: Job):
    jobs = load_jobs()
    jobs.append(job)
    save_jobs(jobs)
    return job

@app.get("/metricas")
def obter_metricas():
    if not METRICAS_PATH.exists():
        raise HTTPException(status_code=500, detail="Métricas não encontradas.")
    data = json.loads(METRICAS_PATH.read_text(encoding="utf-8"))
    
    if JOBS_FILE.exists():
        try: 
            jobs = json.loads(JOBS_FILE.read_text(encoding="utf-8"))
            data["vagas_ativas"] = len(jobs)
        except Exception as exc:
            print("Erro ao ler jobs.json para métricas:", exc)
    return data

