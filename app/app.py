from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import boto3

S3_BUCKET = "autocompletion-comics-buckets"
PDF_DIR = "datasets/pdf"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"  # change to your preferred upload directory

s3 = boto3.client("s3")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in the form"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            s3.upload_fileobj(file, S3_BUCKET, f"{PDF_DIR}/{filename}")
            return "File uploaded successfully"
    return """
    <!doctype html>
    <title>comics-generator</title>
    <h1>Upload a PDF File</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    """


if __name__ == "__main__":
    if not os.path.exists("uploads/"):
        os.makedirs("uploads/")
    app.run(debug=True)
