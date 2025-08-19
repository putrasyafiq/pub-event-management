# 🗓️ Event Management Web Application

A simple, mobile-optimized web application built with Flask and Python for managing events. This application allows users to create, view, and edit event details, with all data persistently stored in Google BigQuery.

## ✨ Features

- **Event Creation**: Easily create new events with details like name, date, description, and attendees.
- **Event Listing**: View a comprehensive list of all created events.
- **Event Editing**: Modify existing event details by clicking on an event from the list.
- **Mobile Optimized**: Responsive design for seamless usage across various devices.
- **BigQuery Integration**: All event data is stored and retrieved from a Google BigQuery table (`dataset_id.table_id`).

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package installer)
- A Google Cloud Project with BigQuery API enabled.
- A service account key file (`service-account-key.json`) for authentication with BigQuery. This file should be placed in the root directory of the project.

### Installation

1. **Clone the repository (if applicable):**
   ```bash
   # If this were a git repository
   # git clone <repository-url>
   # cd pub-event-management
   ```

2. **Create and activate a virtual environment:**
   It's recommended to use a virtual environment to manage dependencies.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   # .venv\Scripts\activate   # On Windows
   ```

3. **Install Python dependencies:**
   ```bash
   pip install Flask google-cloud-bigquery
   ```

### Configuration

- **BigQuery Table**: Ensure you have a BigQuery table named `dataset_id.table_id` in your Google Cloud Project. The schema for this table should match the following structure:

    ```json
    [
      {
        "mode": "REQUIRED",
        "name": "id",
        "type": "STRING"
      },
      {
        "mode": "REQUIRED",
        "name": "name",
        "type": "STRING"
      },
      {
        "mode": "REQUIRED",
        "name": "date",
        "type": "DATETIME"
      },
      {
        "mode": "NULLABLE",
        "name": "desc",
        "type": "STRING"
      },
      {
        "fields": [
          {
            "mode": "NULLABLE",
            "name": "display_name",
            "type": "STRING"
          },
          {
            "mode": "REQUIRED",
            "name": "user_id",
            "type": "STRING"
          }
        ],
        "mode": "REPEATED",
        "name": "users",
        "type": "RECORD"
      }
    ]
    ```

- **Service Account Key**: Place your `service-account-key.json` file in the root directory of the project. This file is used by the application to authenticate with Google Cloud BigQuery.

### Running the Application

1. **Ensure your virtual environment is activated.**
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Flask application:**
   ```bash
   python backend.py
   ```

3. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

## 📂 Project Structure

```
.
├── backend.py              # Flask application backend
├── service-account-key.json # Google Cloud service account key (for BigQuery)
├── css/
│   └── style.css           # Stylesheet for the web application
├── docs/
│   ├── bq-schema-aq_events.txt # BigQuery table schema definition
│   └── instructions.txt    # Original project instructions
└── html/
    ├── create_event.html   # HTML template for creating new events
    ├── edit_event.html     # HTML template for editing existing events
    └── index.html          # HTML template for listing events
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you find any bugs or have suggestions for improvements.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).