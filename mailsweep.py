import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes required
SCOPES = ["https://www.googleapis.com/auth/gmail.modify", "https://mail.google.com/"]  

class GmailHandler:
    def __init__(self):
        self.service = self.authenticate_gmail()
    
    def authenticate_gmail(self):
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
        return build("gmail", "v1", credentials=creds)

    def list_emails(self, label):
        """List and display emails from the specified label (Promotions or Social)."""
        try:
            results = self.service.users().messages().list(userId="me", labelIds=[label], maxResults=10).execute()
            messages = results.get("messages", [])
            if not messages:
                print(f"No new emails found in the {label} section.")
                return []
            
            print(f"\nRecent emails from the {label} section:")
            email_ids = []
            for msg in messages:
                msg_detail = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                headers = msg_detail.get("payload", {}).get("headers", [])
                subject = next((header["value"] for header in headers if header["name"] == "Subject"), "No Subject")
                print(f"- {subject}")
                email_ids.append(msg["id"])
            return email_ids
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def delete_emails(self, email_ids, label_name):
        """Delete emails based on their IDs."""
        if not email_ids:
            print(f"No emails to delete in the {label_name} section.")
            return
        try:
            for email_id in email_ids:
                self.service.users().messages().delete(userId="me", id=email_id).execute()
            print(f"All emails in the {label_name} section have been deleted.")
        except HttpError as error:
            print(f"An error occurred while deleting emails: {error}")

class GmailManager:
    def __init__(self):
        self.gmail_handler = GmailHandler()
    
    def run(self):
        """Main function to list and delete emails."""
        print("Welcome to Gmail Social & Promotions Email Reader!")
        input("Press Enter to proceed with Gmail authentication...")
        
        # Fetch emails from Social and Promotions sections
        social_emails = self.gmail_handler.list_emails("CATEGORY_SOCIAL")
        promotions_emails = self.gmail_handler.list_emails("CATEGORY_PROMOTIONS")
        
        print("\nWhich section's emails would you like to delete?")
        print("1. Social")
        print("2. Promotions")
        print("3. None")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            self.gmail_handler.delete_emails(social_emails, "Social")
        elif choice == "2":
            self.gmail_handler.delete_emails(promotions_emails, "Promotions")
        elif choice == "3":
            print("No emails were deleted.")
        else:
            print("Invalid choice. Please restart the script and enter 1, 2, or 3.")

if __name__ == "__main__":
    GmailManager().run()
