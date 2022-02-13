import json
import os
from pprint import pprint

import requests
from google.cloud import dialogflow


def get_flow_reply(session_id: int, user_text: str, language_code: str = "ru") -> str:
    project_id = os.getenv("GOOGLE_PROJECT_ID")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project=project_id, session=session_id)

    text_input = dialogflow.TextInput(text=user_text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def get_prepared_intents(url: str):
    response = requests.get(url)
    response.raise_for_status()

    return json.loads(response.text)


if __name__ == "__main__":
    url = "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
    intents = get_prepared_intents(url)
    pprint(intents)
