from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types.session import QueryResult


def get_flow_reply(
    google_project_id: str,
    session_id: int,
    user_text: str,
    language_code: str = "ru",
) -> QueryResult:

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project=google_project_id, session=session_id)

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
