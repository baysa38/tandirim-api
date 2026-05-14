import os
from dotenv import load_dotenv

# .env dosyasını router ve servisler yüklenmeden önce oku
load_dotenv()

from fastapi import FastAPI
from routers import manychat_webhook

app = FastAPI(
    title="Tandırım E-Ticaret Asistanı API",
    description="ManyChat ve satış otomasyonu için webhook API",
    version="1.0.0",
)

app.include_router(manychat_webhook.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "ok", "message": "Tandırım E-Ticaret Asistanı çalışıyor"}


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
