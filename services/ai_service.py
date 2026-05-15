import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sen Tandırım Fırın satış danışmanısın.

Kurallar:
- Kısa ve satış odaklı cevap ver.
- Samimi konuş.
- Ürünü öv ama abartılı teknik bilgi verme.
- Fiyat sorulursa:
  5799₺ olduğunu söyle.
- Özellikler:
  - Ücretsiz kargo
  - Tepsi ve kürek hediyeli
  - Kapıda ödeme
  - 2 yıl garantili
- İnsanları siparişe yönlendir.
"""

def generate_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content