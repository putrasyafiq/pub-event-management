from flask import Flask, request, render_template, redirect, url_for, jsonify
import uuid
import datetime
from google.cloud import bigquery
import os

app = Flask(__name__, template_folder='html', static_folder='css')

# Configure BigQuery client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"
client = bigquery.Client()
TABLE_ID = "project_id.dataset_id.table_id" # Replace with your actual project ID, dataset ID, and table ID

@app.route('/')
def index():
    query = f"SELECT id, name, date, `desc`, users FROM `{TABLE_ID}`"
    query_job = client.query(query)
    events_data = []
    for row in query_job:
        event = dict(row)
        # Convert BigQuery Row to a dictionary, handling nested records
        if event['users']:
            event['users'] = [dict(user) for user in event['users']]
        events_data.append(event)
    return render_template('index.html', events=events_data)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_id = str(uuid.uuid4())
        name = request.form['name']
        date_str = request.form['date']
        desc = request.form.get('desc')
        users_data = request.form.get('users')

        try:
            date_obj = datetime.datetime.fromisoformat(date_str)
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS", 400

        users = []
        if users_data:
            for user_entry in users_data.split(';'):
                if ':' in user_entry:
                    display_name, user_id = user_entry.split(':', 1)
                    users.append({"display_name": display_name.strip(), "user_id": user_id.strip()})
                else:
                    users.append({"user_id": user_entry.strip()})

        rows_to_insert = [{
            "id": event_id,
            "name": name,
            "date": date_obj.isoformat(),
            "desc": desc,
            "users": users
        }]

        errors = client.insert_rows_json(TABLE_ID, rows_to_insert)
        if errors:
            return jsonify(errors), 500
        return redirect(url_for('index'))
    return render_template('create_event.html')

@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    query = f"SELECT id, name, date, `desc`, users FROM `{TABLE_ID}` WHERE id = '{event_id}'"
    query_job = client.query(query)
    event_rows = list(query_job)

    if not event_rows:
        return "Event not found", 404

    event = dict(event_rows[0])
    if event['users']:
        event['users'] = [dict(user) for user in event['users']]

    if request.method == 'POST':
        name = request.form['name']
        date_str = request.form['date']
        desc = request.form.get('desc')
        users_data = request.form.get('users')

        try:
            date_obj = datetime.datetime.fromisoformat(date_str)
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS", 400

        users = []
        if users_data:
            for user_entry in users_data.split(';'):
                if ':' in user_entry:
                    display_name, user_id = user_entry.split(':', 1)
                    users.append({"display_name": display_name.strip(), "user_id": user_id.strip()})
                else:
                    users.append({"user_id": user_entry.strip()})

        # BigQuery does not support UPDATE directly on nested fields or complex types easily.
        # A common pattern is to delete and re-insert, or use a MERGE statement.
        # For simplicity, we'll update all fields.
        # Note: This update query is simplified and might not handle all edge cases for nested records.
        update_query = f"""
        UPDATE `{TABLE_ID}`
        SET
            name = @name,
            date = @date,
            `desc` = @desc,
            users = @users
        WHERE id = @id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("name", "STRING", name),
                bigquery.ScalarQueryParameter("date", "DATETIME", date_obj.isoformat()),
                bigquery.ScalarQueryParameter("desc", "STRING", desc),
                bigquery.ArrayQueryParameter(
                    "users",
                    "STRUCT<display_name STRING, user_id STRING>",
                    [bigquery.StructQueryParameter("users", {"display_name": u.get("display_name"), "user_id": u["user_id"]}) for u in users]
                ),
                bigquery.ScalarQueryParameter("id", "STRING", event_id),
            ]
        )
        query_job = client.query(update_query, job_config=job_config)
        query_job.result() # Wait for the job to complete

        return redirect(url_for('index'))
    return render_template('edit_event.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)