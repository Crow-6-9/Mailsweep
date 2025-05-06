from flask import Flask, render_template, request, redirect, url_for
from gmail_cleaner.auth import GmailAuth
from gmail_cleaner.gmail_utils import GmailCleaner
from gmail_cleaner.scheduler import trigger_airflow_dag

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        schedule_option = request.form.get("schedule")
        trigger_airflow_dag(schedule_option)
        return render_template("confirmation.html", option=schedule_option)
    return render_template("schedule.html")

@app.route("/delete", methods=["GET"])
def manual_delete():
    auth = GmailAuth()
    service = auth.authenticate()
    cleaner = GmailCleaner(service)

    email_ids, subjects = cleaner.list_emails("CATEGORY_PROMOTIONS")
    cleaner.delete_emails(email_ids)
    return f"Deleted {len(email_ids)} promotion emails."  # You can render a template instead

if __name__ == "__main__":
    app.run(debug=True)
