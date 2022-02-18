import argparse
import json
import os

from dotenv import load_dotenv
from tqdm import tqdm
from google.api_core.exceptions import GoogleAPIError

from google_dialogflow_api import create_intent


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload intents to DialogFlow from JSON file"
    )
    parser.add_argument("-p", "--path", help="Intents JSON file path", required=True)

    return parser.parse_args()


def main():
    load_dotenv()
    project_id = os.getenv("GOOGLE_PROJECT_ID")

    args = parse_arguments()

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
