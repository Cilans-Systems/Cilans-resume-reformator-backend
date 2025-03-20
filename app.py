import json
import os
import re
from utils.helper import (
    extract_content_from_pdf,
    reformat_resume,
    convert_html_to_docx_tallahassee,
    convert_html_to_docx_turnpike,
    read_pdf,
)
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from celery import Celery, Task, shared_task
from io import BytesIO
import base64
from spire.doc import Document, FileFormat
import io

app = Flask(__name__)

# In-memory storage for uploaded files
uploaded_files = {}

# Enable CORS for all routes
CORS(app)

# Load environment variables from .env file
load_dotenv()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app.config.from_mapping(
    CELERY=dict(
        broker_url=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        task_ignore_result=False,
    ),
)
celery_app = celery_init_app(app)


@app.route("/")
def index():
    return "Welcome to the Resume Formatter API!"


@shared_task()
def handle_file(
    resume_content,
    keywords_json,
    resume_formate,
    ai_generated_summary,
    filename,
):
    """
    Handle file upload and process the file based on its type.

    This endpoint accepts a file from the user, processes it based on its type
    (docx, doc, pdf), cleans the resume content, reformats it with given keywords,
    and converts the result into a DOCX file. The file is then returned as a
    base64-encoded string in JSON response.

    Returns:
        JSON response with either:
            - The base64-encoded content of the formatted DOCX file along with the filename and keywords.
            - An error message and appropriate status code in case of issues.
    """
    # Process .docx files

    try:
        keywords = json.loads(keywords_json)  # Parse the JSON string into a Python list

        # Validate that 'keywords' is a list
        if not isinstance(keywords, list):
            return jsonify({"error": "Keywords must be a list"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format for keywords"}), 400

    # Reformat the cleaned resume content using the provided keywords
    formatted_resume = reformat_resume(
        resume_content, keywords, resume_formate, ai_generated_summary
    )

    # Convert the reformatted resume (HTML) into a DOCX file
    if resume_formate == "Tallahassee":
        final_formatted_doc = convert_html_to_docx_tallahassee(formatted_resume)
    elif resume_formate == "Turnpike":
        final_formatted_doc = convert_html_to_docx_turnpike(formatted_resume)
    else:
        return jsonify({"error": "Invalid resume format"}), 400

    # Save the formatted document to a BytesIO stream instead of the filesystem
    doc_stream = BytesIO()
    final_formatted_doc.save(doc_stream)
    doc_stream.seek(0)  # Reset the stream position to the beginning for reading

    # Encode the file content as base64 for transmission back to the frontend
    encoded_content = base64.b64encode(doc_stream.read()).decode("utf-8")

    if ai_generated_summary == "True":
        file_postfix = f"_AI_Formatted_({resume_formate})_(With AI Summary).docx"
    else:
        file_postfix = f"_AI_Formatted_({resume_formate}).docx"

    filename = filename.replace("_", " ")

    filename = (
        re.sub(
            r" {2,}", " ", re.sub(r"\b\w*unform\w*\b", "", filename.lower())
        ).replace(" ", "_")
        + file_postfix
    )
    filename = re.sub(r"__+", "_", filename)

    # Return the filename, base64-encoded file content, and keywords in JSON format
    return {
        "filename": filename,
        "file_content": encoded_content,
        "keywords": keywords,
    }


def clean_text(text):

    # Define a regex pattern to match any line that contains "Spire.Doc"
    pattern = r".*Spire\.Doc.*\n?"
    # Remove lines that match the pattern
    text = re.sub(pattern, "", text, flags=re.MULTILINE)
    # Replace bullet points with a dash
    text = re.sub(r"\uf0b7|\u2022|�", "-", text)
    # Remove unwanted line breaks after bullet points
    text = re.sub(r"-\s*\n\s*", "- ", text)
    # Replace multiple newlines with a single newline
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


@app.route("/file-upload", methods=["POST"])
def file_upload():

    # Check if a file is part of the request
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    uploaded_file = request.files["file"]

    # Check if the file has been selected
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Identify the file type based on MIME type
    file_type = uploaded_file.mimetype

    # Retrieve keywords from form data (JSON string), defaulting to an empty list
    keywords_json = request.form.get("keywords", "[]")

    # Retrieve the selected resume format from the form data, defaulting to "Tallahassee"
    resume_formate = request.form.get("resume_format", "Tallahassee").capitalize()

    # Retrieve the AI-generated summary from the form data, defaulting to False
    ai_generated_summary = request.form.get(
        "ai_generated_summary", "false"
    ).capitalize()

    # Generate a filename for the formatted DOCX file
    filename, _ = os.path.splitext(uploaded_file.filename)

    if (
        file_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        # Assuming uploaded_file is already defined and holds the uploaded file object
        file_path = os.path.join("static", uploaded_file.filename)
        uploaded_file.save(file_path)

        # Define the path for the PDF file
        pdf_path = file_path.replace(".docx", ".pdf")

        # Use Spire.Doc to convert DOCX to PDF
        doc = Document(file_path)
        doc.SaveToFile(pdf_path, FileFormat.PDF)

        # Read content from the PDF file (you can adjust this function as needed)
        resume_content = read_pdf(pdf_path).replace("\n\n", "\n")

        resume_content = clean_text(resume_content)

        # After use, delete the files
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        if os.path.exists(file_path):
            os.remove(file_path)

    # Process .pdf files
    elif file_type == "application/pdf":
        # Read the file content and extract text from PDF
        file_content = uploaded_file.read()
        resume_content = extract_content_from_pdf(io.BytesIO(file_content))
        resume_content = clean_text(resume_content)
    else:
        # Unsupported file type
        return jsonify({"message": "Unsupported file type"}), 400

    # Process the uploaded file using Celery
    task = handle_file.apply_async(
        args=(
            resume_content,
            keywords_json,
            resume_formate,
            ai_generated_summary,
            filename,
        ),
        time_limit=1800,
    )

    # Return the task ID to the client
    return jsonify({"task_id": task.id}), 202


@app.route("/result/<task_id>", methods=["GET"])
def result(task_id):
    task = handle_file.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != "FAILURE":
        response = task.result
    else:
        response = {
            "state": task.state,
            "error": str(task.info),  # this will be a string
        }
        return jsonify(response), 400
    return jsonify(response), 200


asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    # Start the Flask application, listening on all interfaces (0.0.0.0) for Docker compatibility
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("DEBUG_MODE", False))
