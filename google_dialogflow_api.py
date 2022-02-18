import argparse
import json
import os

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types.session import QueryResult
from tqdm import tqdm

load_dotenv()
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload intents to DialogFlow from JSON file"
    )
    parser.add_argument("--add", help="Intents JSON filename", required=True)

    return parser.parse_args()


def get_flow_reply(
    session_id: int,
    user_text: str,
    language_code: str = "ru",
) -> QueryResult:

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project=GOOGLE_PROJECT_ID, session=session_id)

    text_input = dialogflow.TextInput(text=user_text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def create_intent(
    project_id: str,
    title: str,
    intent_content: dict,
) -> dialogflow.Intent:

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

    args = parse_arguments()

    intents_filepath = args.add
    with open(intents_filepath, "r") as file:
        intents = json.load(file)

    for title, content in tqdm(
        iterable=intents.items(), desc="Uploading Intents", unit="Intent"
    ):
        try:
            create_intent(project_id, title, content)
        except GoogleAPIError as e:
            print(e)
            continue