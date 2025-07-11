import json
from fastapi import UploadFile
from google import genai
from google.genai import types
from google.auth import default

from config import CARD_DETECTION_PROMPT, RESPONSE_SCHEMA
from models.card import Cards
from services.firestore import FirestoreService

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

    model = "gemini-2.5-pro"
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
        response_schema=RESPONSE_SCHEMA,
        system_instruction=[types.Part.from_text(text=si_text1)],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    data = response.text
    return json.loads(data)


def find_card_in_firestore(card_number, set_id, firestore_service=None, cache_series={}):
    if not firestore_service:
        firestore_service = FirestoreService()

    if set_id in cache_series:
        set_doc = {
            "_id": cache_series[set_id]
        }
    else:
        set_doc = firestore_service.query_documents(
            'series',
            filters=[
                ("set_id", "==", set_id)
            ]
        )
        if not set_doc:
            print('set not')
            return None, cache_series

        set_doc = set_doc[0]
        cache_series[set_id] = set_doc.get('_id')

    card_data = firestore_service.query_sub_collection(
        "series",
        set_doc.get('_id'),
        "cards",
        filters=[
            ("card_number", "==", card_number)
        ]
    )
    if not card_data:
        print("card not found")
        return None, cache_series

    return card_data, cache_series
