from googleapiclient.errors import HttpError

class GmailCleaner:
    def __init__(self, service):
        self.service = service

    def list_emails(self, label):
        try:
            results = self.service.users().messages().list(userId="me", labelIds=[label], maxResults=10).execute()
            messages = results.get("messages", [])
            email_ids = []
            subjects = []
            for msg in messages:
                msg_detail = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                headers = msg_detail.get("payload", {}).get("headers", [])
                subject = next((header["value"] for header in headers if header["name"] == "Subject"), "No Subject")
                subjects.append(subject)
                email_ids.append(msg["id"])
            return email_ids, subjects
        except HttpError as error:
            print(f"An error occurred: {error}")
            return [], []

    def delete_emails(self, email_ids):
        try:
            for email_id in email_ids:
                self.service.users().messages().delete(userId="me", id=email_id).execute()
            return True
        except HttpError as error:
            print(f"Error deleting emails: {error}")
            return False


# ------------------- gmail_cleaner/scheduler.py -------------------
def trigger_airflow_dag(option):
    # Placeholder: Logic to trigger Airflow DAG based on option (e.g., weekly, monthly)
    print(f"Triggering Airflow DAG for option: {option}")
