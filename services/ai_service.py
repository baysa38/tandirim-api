import os
from typing import Optional

SYSTEM_PROMPT = """Sen Tandırım Fırın markasının profesyonel satış asistanısın.

ÜRÜN:
Tandırım Çok Amaçlı Ev Tipi Fırın

FİYAT:
5.799₺

KAMPANYA:
- Ücretsiz kargo
- Tepsi ve kürek hediyeli
- 2 yıl garanti
- 5 taksit imkanı

ÜRÜN AVANTAJLARI:
- Evde odun ateşi tadında pişirme
- Ekmek, pide, lahmacun, pizza, börek, gözleme ve et pişirme
- Tezgah üstü günlük kullanım
- Hızlı ısınır, hızlı pişirir
- A++ düşük enerji tüketimi
- 40 cm taban yüzeyi
- 50-300 derece termostat

KONUŞMA KURALLARI:
- Kısa, net ve satış odaklı cevap ver.
- Uzun paragraf yazma.
- Müşteriyi yorma.
- Her cevapta siparişe yaklaştır.
- Gereksiz teknik detay verme.
- Samimi ama kurumsal konuş.
- Emoji az kullan.
- Müşteri fiyat sorarsa fiyatı net söyle.
- Müşteri pahalı derse enerji tasarrufu, hediye ve uzun ömürle ikna et.
- Müşteri almak isterse adres, ad soyad ve telefon iste.
- Bilmediğin konuda uydurma yapma.

AMAÇ:
Müşteriyi WhatsApp/Instagram üzerinden siparişe yönlendirmek.
"""


def _rule_based_reply(message: str) -> Optional[str]:
    message_lower = message.lower()

    if "fiyat" in message_lower or "kaç para" in message_lower or "ne kadar" in message_lower:
        return "Fiyatımız 5.799₺. Şu an ücretsiz kargo + tepsi & kürek hediyeli. Sipariş oluşturmak ister misiniz?"

    if "ne işe yarar" in message_lower or "ne yapar" in message_lower or "ne pişir" in message_lower:
        return "Tandırım Fırın ile evde taş fırın lezzetinde ekmek, lahmacun, pizza, börek, gözleme ve et pişirebilirsiniz."

    if "pahalı" in message_lower or "çok para" in message_lower:
        return "Haklısınız, fiyat önemli. Ama düşük enerji tüketimi, uzun ömür, 2 yıl garanti ve tepsi-kürek hediyesiyle uzun vadede çok avantajlıdır."

    if "almak istiyorum" in message_lower or "sipariş" in message_lower or "alacağım" in message_lower:
        return "Harika 👍 Sipariş için ad soyad, açık adres ve telefon numaranızı yazmanız yeterli."

    if "taksit" in message_lower:
        return "5 taksit imkanı mevcut. Ücretsiz kargo ve tepsi-kürek hediyesi de kampanyaya dahil. Sipariş oluşturalım mı?"

    if "kargo" in message_lower:
        return "Kargo tamamen ücretsizdir. Türkiye geneli gönderim yapıyoruz."

    if "koku" in message_lower:
        return "Ağır koku yapmaz; pişen ürünün iştah açan lezzet kokusu olur."

    return None


def _openai_reply(user_name: str, message: str) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Müşteri adı: {user_name}\nMüşteri mesajı: {message}"},
            ],
            temperature=0.4,
            max_tokens=160,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI yanıt hatası: {e}")
        return None


def process_message(user_id: str, message: str, user_name: str) -> str:
    rule_reply = _rule_based_reply(message)
    if rule_reply:
        return rule_reply

    ai_reply = _openai_reply(user_name=user_name, message=message)
    if ai_reply:
        return ai_reply

    return "Merhaba, Tandırım Fırın hakkında size yardımcı olayım. Fiyat, taksit veya sipariş bilgisi ister misiniz?"
