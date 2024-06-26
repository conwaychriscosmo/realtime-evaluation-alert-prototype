
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
import os.path
import os
from openai import OpenAI
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "C:\\Users\\conwa\\realtime-evaluation\\prototype\\random_email_thing\\credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    os.environ["OPENAI_API_KEY"] = "{your api key here}"
    llm_client=OpenAI()

    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    service.users().messages().get(userId="me",id='190567e1219e7a42').execute()
    message_response = service.users().messages().list(userId="me", maxResults=50).execute()
    message_list = message_response['messages']
    joyful_message_ids = []
    for message in message_list:
        message_text = service.users().messages().get(userId="me",id=message['id']).execute()
        message_str = str(message_text)
        message_for_gpt = f"Please respond yes or no: will the following message bring the recipient more joy than they had before, '{message_str}' ?"
        #vector_embedding = llm_client.embeddings.create(
        #  model="text-embedding-ada-002",
        #  input=message_str, I don't want to pay for superfluous embeddings
        #  encoding_format="float"
        #)
        completion = llm_client.chat.completions.create(
          model = "gpt-3.5-turbo-0125",
          messages=[
            {"role": "system", "content": "You are genie that exists to promote happiness, joy, and all forms of stoke!  Please wield your great wisdom of happiness to review the messages and promote the emails that will bring the intended recipient more joy than they had before."},
            {"role": "user", "content": message_for_gpt[0:5000]}
          ]
        )
        if "yes" in completion.choices[0].message.content.lower():
            joyful_message_ids.append(message['id'])
    print(len(joyful_message_ids))

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
# [END gmail_quickstart]
