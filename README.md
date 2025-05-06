This repo contains grain level code as of now. 
Once it gets published , live project link will be shared here. 


# Gmail Cleaner Web App 🧹📧

A secure and user-friendly web application built with Flask that allows users to clean up their Gmail inbox by deleting emails from Social and Promotions categories. Users can choose custom deletion preferences (e.g., custom, weekly, monthly, yearly), and background email cleanup is automated using Apache Airflow.

## 🔧 Features

- 🔐 OAuth 2.0 authentication for secure Gmail access
- 📬 Delete emails from "Social" and "Promotions" tabs
- 📅 Options for custom, weekly, monthly, or yearly cleanup
- ⚙️ Airflow-powered scheduling for automated email deletion
- 🧱 Modular Object-Oriented Python design for maintainability
- 🌐 Web UI with a clean and interactive interface

## 🧠 Tech Stack

- **Frontend:** HTML, CSS (Jinja2 with Flask)
- **Backend:** Python (Flask, Gmail API, OOP)
- **Scheduler:** Apache Airflow

## 🚀 How It Works

1. User visits the web app and authenticates with Google.
2. Chooses deletion frequency (custom, weekly, etc.).
3. A corresponding Airflow DAG is triggered.
4. DAG executes Gmail API logic to delete categorized emails.
5. Emails are cleaned up automatically based on user choice.
