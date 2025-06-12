import json
from fastapi import UploadFile
from google import genai
from google.genai import types
from google.auth import default

from config import CARD_DETECTION_PROMPT
from models.card import Cards

_, project = default()

client = genai.Client(
    vertexai=True,
    project=project,
    location="global",
)

def generate(image: UploadFile) -> Cards:

    msg1_image1 = types.Part.from_bytes(
        data=image.file.read(),
        mime_type="image/jpeg",
    )
    si_text1 = CARD_DETECTION_PROMPT

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
            "type": "STRING"}, "card_number": {"type": "STRING"}, "card_name": {"type": "STRING"}, "licence": {"type": "STRING"}}}},
        system_instruction=[types.Part.from_text(text=si_text1)],
    )
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    data = response.text
    return json.loads(data)

