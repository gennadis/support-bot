import os

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
