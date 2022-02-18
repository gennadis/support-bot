import argparse
import json
import os

from dotenv import load_dotenv
from tqdm import tqdm
from google.api_core.exceptions import GoogleAPIError

from google_dialogflow_api import create_intent


def main():
    load_dotenv()
    project_id = os.getenv("GOOGLE_PROJECT_ID")

    parser = argparse.ArgumentParser(description="Upload intents from JSON file")
    parser.add_argument("-p", "--path", help="Intents JSON file path", required=True)
    args = parser.parse_args()

    intents_filepath = args.path
    with open(intents_filepath, "r") as file:
        intents = json.load(file)

    for title, content in tqdm(
        iterable=intents.items(), desc="Uploading Intents", unit="Intent"
    ):
        try:
            create_intent(project_id, title, content)
        except GoogleAPIError as e:
            print(f"Intent uploading error: {e}")
            continue


if __name__ == "__main__":
    main()
