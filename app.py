from flask import Flask, render_template, request
import psycopg2
import os
import boto3

app = Flask(__name__)

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_REGION_NAME = os.getenv('S3_REGION_NAME')

s3_client = boto3.client('s3', region_name=S3_REGION_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-connection', methods=['POST'])
def test_connection():
    dbname = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')

    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        message = f"Connected to PostgreSQL database, version: {db_version[0]}"
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        message = f"Error while connecting to PostgreSQL: {error}"
        success = False
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()

    return render_template('result.html', success=success, message=message)


@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    try:
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return "File uploaded successfully"
    except Exception as e:
        return f"Error uploading file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)