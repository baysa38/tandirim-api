from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import process_message

router = APIRouter()


class ManyChatRequest(BaseModel):
    user_id: str = "test_user"
    message: str
    first_name: str = "Değerli Müşterimiz"


@router.post("/manychat/webhook")
async def manychat_webhook(payload: ManyChatRequest):
    try:
        ai_response = process_message(
            user_id=payload.user_id,
            message=payload.message,
            user_name=payload.first_name,
        )

        return {
            "version": "v2",
            "content": {
                "messages": [
                    {"type": "text", "text": ai_response},
                    {
                        "type": "text",
                        "text": "🚚 Ücretsiz kargo + Tepsi & Kürek hediyeli. Sipariş vermek ister misiniz?",
                    },
                ]
            },
        }

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return {
            "version": "v2",
            "content": {
                "messages": [
                    {
                        "type": "text",
                        "text": "Şu anda teknik bir güncelleme yapıyoruz. Sipariş için adınızı ve telefon numaranızı bırakabilirsiniz.",
                    }
                ]
            },
        }
