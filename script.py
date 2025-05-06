import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify", "https://mail.google.com/"]  # Added modify scope to allow email deletion


def authenticate_gmail():
    """Authenticate and return the Gmail API service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service


def list_emails(service, label):
    """List and display emails from the specified label (Promotions or Social)."""
    try:
        results = service.users().messages().list(userId="me", labelIds=[label], maxResults=10).execute()
        messages = results.get("messages", [])
        if not messages:
            print(f"No new emails found in the {label} section.")
            return []

        print(f"\nRecent emails from the {label} section:")
        email_ids = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_detail.get("payload", {}).get("headers", [])
            subject = next((header["value"] for header in headers if header["name"] == "Subject"), "No Subject")
            print(f"- {subject}")
            email_ids.append(msg["id"])
        return email_ids

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def delete_emails(service, email_ids, label_name):
    """Delete emails based on their IDs."""
    if not email_ids:
        print(f"No emails to delete in the {label_name} section.")
        return
    try:
        for email_id in email_ids:
            service.users().messages().delete(userId="me", id=email_id).execute()
        print(f"All emails in the {label_name} section have been deleted.")
    except HttpError as error:
        print(f"An error occurred while deleting emails: {error}")


def main():
    print("Welcome to Gmail Social & Promotions Email Reader!")
    input("Press Enter to proceed with Gmail authentication...")

    service = authenticate_gmail()

    # Fetch emails from Social and Promotions sections
    social_emails = list_emails(service, "CATEGORY_SOCIAL")
    promotions_emails = list_emails(service, "CATEGORY_PROMOTIONS")

    print("\nWhich section's emails would you like to delete?")
    print("1. Social")
    print("2. Promotions")
    print("3. None")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        delete_emails(service, social_emails, "Social")
    elif choice == "2":
        delete_emails(service, promotions_emails, "Promotions")
    elif choice == "3":
        print("No emails were deleted.")
    else:
        print("Invalid choice. Please restart the script and enter 1, 2, or 3.")


if __name__ == "__main__":
    main()



# import os
# import pickle
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # Define the Gmail API scope (read-only access)
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# def authenticate_gmail():
#     """Authenticates and returns the Gmail API service."""
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#     service = build('gmail', 'v1', credentials=creds)
#     return service

# def list_recent_emails(service):
#     """Fetch and display the subject lines of recent emails."""
#     try:
#         # Get the list of messages from the inbox
#         results = service.users().messages().list(userId='me', maxResults=23).execute()
#         messages = results.get('messages', [])

#         if not messages:
#             print("No new emails found.")
#             return

#         print("Recent emails:")
#         for msg in messages:
#             msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
#             headers = msg_detail.get('payload', {}).get('headers', [])
#             subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
#             print(f"- {subject}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def main():
#     print("Welcome to the Gmail Email Reader Script!")
#     input("Press Enter to proceed with Gmail authentication...")

#     service = authenticate_gmail()
#     list_recent_emails(service)

# if __name__ == '__main__':
#     main()


# import os  # reading only 
# import pickle
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # Define the Gmail API scope for read-only access
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# def authenticate_gmail():
#     """Authenticates and returns the Gmail API service."""
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#     service = build('gmail', 'v1', credentials=creds)
#     return service

# def list_emails_by_label(service, label):
#     """Fetch and display emails from the specified Gmail label (Social or Promotions)."""
#     try:
#         # Fetch messages with the specified label
#         results = service.users().messages().list(userId='me', labelIds=[label]).execute()
#         messages = results.get('messages', [])

#         if not messages:
#             print(f"No new emails found in the {label} section.")
#             return

#         print(f"Recent emails from the {label} section:")
#         for msg in messages:
#             msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
#             headers = msg_detail.get('payload', {}).get('headers', [])
#             subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
#             print(f"- {subject}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def main():
#     print("Welcome to Gmail Social & Promotions Email Reader Script!")
#     input("Press Enter to proceed with Gmail authentication...")

#     service = authenticate_gmail()

#     print("\nFetching emails from Social and Promotions sections...\n")
#     list_emails_by_label(service, 'CATEGORY_SOCIAL')
#     list_emails_by_label(service, 'CATEGORY_PROMOTIONS')

# if __name__ == '__main__':
#     main()
