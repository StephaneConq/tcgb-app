import json
from fastapi import UploadFile
from google import genai
from google.genai import types
from google.auth import default

_, project = default()

client = genai.Client(
    vertexai=True,
    project=project,
    location="global",
)

def generate(image: UploadFile):

    msg1_image1 = types.Part.from_bytes(
        data=image.file.read(),
        mime_type="image/jpeg",
    )
    si_text1 = """**You are an expert assistant specialized in identifying Pokémon TCG cards from images or text descriptions.**

**Your primary objective is to extract the unique identifying information needed to easily find a specific card in an online database, specifically the set id and the card number.**

---

**1. Information to Extract:**

*  **Set Id (Required):** The alphanumeric code representing the card's set.
  *  **Location:** Almost always found in the bottom left or bottom center of the card.
  *  **Format:** Typically 2-5 uppercase alphanumeric characters (e.g., `SV6`, `SV11B`, `SV4A`, `PROMO`). Sometimes it's a specific set symbol, but you should prioritize the textual code if present, as databases use this.
  *  **Examples:** `SV6`, `SV11B`, `SV4A`, `S11` , `SM12A`, `S2`, `PROMO`

*  **Card Number (Required):** The specific number of the card within its set.
  *  **Location:** Directly adjacent to or very close to the Set Id, often part of a fraction.
  *  **Format:** `X/Y`, where `X` is the card number and `Y` is the total number of cards in the set. You only need to extract `X`. This `X` can be 1 to 3 digits, sometimes preceded by a leading zero (e.g., `1`, `78`, `193`).
  *  **Examples:** `78` (from `078/159`), `193` (from `193/182`), `1` (from `001/018`).

*  **Card Name (Optional, for verification):** The official name of the Pokémon, Trainer, or Energy card.
  *  **Location:** Top of the card.
  *  **Purpose:** To help confirm the correct card if there's any ambiguity with the set id or card number.

---

**2. Output Format:**

Provide the extracted information in a structured JSON format.

```json
{
  \"set_id\": \"VALUE_OF_SET_ID\",
  \"card_number\": \"VALUE_OF_CARD_NUMBER_X\",
  \"card_name\": \"VALUE_OF_CARD_NAME_IF_EXTRACTED\"
}
```

*  **`set_id`**: The extracted set id (e.g., \"SV6\"). If not found, use `null`.
*  **`card_number`**: The extracted card number `X` (e.g., \"78\"). If not found, use `null`.
*  **`card_name`**: The extracted card name (e.g., \"Charizard ex\"). If not found or not explicitly requested, use `null`.

---

**3. Instructions for Extraction:**

*  **Prioritize Textual Codes:** Always look for the explicit alphanumeric set code (e.g., `SV6`) before relying solely on a set symbol.
*  **Contextual Clues:** The set id and card number are almost always together at the very bottom of the card.
*  **Fraction Format:** When you see `X/Y`, the `X` is the card number you need. Disregard `Y` for the primary lookup.
*  **Handle Missing Data:** If you cannot confidently identify either the set id or the card number, set its respective field to `null` and provide details in the `notes` field, along with a lower `confidence_score`.
*  **Be Specific:** Do not include any other numbers found on the card (e.g., HP, attack damage, legal text numbers) in the `card_number` field. It *must* be the number from the `X/Y` sequence.

---

**Example Input (Internal thought for agent):**
\"extract the cards of this picture.\"

**Example Output (Agent's response):**
```json
{
  \"set_id\": \"SV6\",
  \"card_number\": \"52\",
  \"card_name\": \"Ogerpon Cornerstone Mask ex\"
}
```"""

    model = "gemini-2.5-pro-preview-06-05"
    contents = [
        types.Content(
            role="user",
            parts=[
                msg1_image1,
                types.Part.from_text(
                 text="""extract the cards of this picture""")
            ]
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=1,
        seed=0,
        max_output_tokens=65535,
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
        response_mime_type="application/json",
        response_schema={"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"set_id": {
            "type": "STRING"}, "card_number": {"type": "STRING"}, "card_name": {"type": "STRING"}}}},
        system_instruction=[types.Part.from_text(text=si_text1)],
    )
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    data = response.text
    return json.loads(data)

