# Tandırım E-Ticaret Otomasyonu

## Kurulum

1. Bu klasörü Antigravity / VS Code ile aç.
2. Terminal aç.
3. Şunu çalıştır:

```bash
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn main:app --reload
```

## Test

Tarayıcıdan aç:

```text
http://127.0.0.1:8000/docs
```

Webhook adresi:

```text
POST /api/v1/manychat/webhook
```

Test body:

```json
{
  "user_id": "123",
  "message": "fiyat nedir",
  "first_name": "Ahmet"
}
```

## ManyChat URL

Local testte URL:

```text
http://127.0.0.1:8000/api/v1/manychat/webhook
```

Canlıya alınca Railway/Render adresinin sonuna bunu ekle:

```text
/api/v1/manychat/webhook
```
