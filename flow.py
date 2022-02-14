import os

import requests
from dotenv import load_dotenv
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types.session import QueryResult
from tqdm import tqdm


def get_flow_reply(
    session_id: int,
    user_text: str,
    language_code: str = "ru",
) -> QueryResult:
    project_id = os.getenv("GOOGLE_PROJECT_ID")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project=project_id, session=session_id)

    text_input = dialogflow.TextInput(text=user_text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def get_prepared_intents(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def create_intent(project_id: str, title: str, intent_content: dict):

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for question in intent_content["questions"]:
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[intent_content["answer"]])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=title,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    return response


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv("GOOGLE_PROJECT_ID")

    intents_url = "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
    intents = get_prepared_intents(intents_url)

    for title, content in tqdm(
        iterable=intents.items(), desc="Uploading Intents", unit="Intent"
    ):
        create_intent(project_id, title, content)
