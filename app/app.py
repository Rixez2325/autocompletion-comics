import time
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import boto3

S3_BUCKET = "autocompletion-comics-buckets"
PDF_DIR = "datasets/pdf"
RESULT_DIR = "datasets/generated_page"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"  # change to your preferred upload directory

s3 = boto3.client("s3")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    run_ec2_process()
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in the form"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET, f"{PDF_DIR}/{filename}")
            return "File uploaded successfully, processing in progress ..."
    return """
    <!doctype html>
    <title>comics-generator</title>
    <h1>Upload a PDF File</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    """


def run_ec2_process():
    ssm = boto3.client("ssm", region_name="eu-west-1c")  # replace with your region

    response = ssm.send_command(
        InstanceIds=["i-0b88b6d191f445ba1"],  # replace with your instance ID
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [
                # "python /home/ec2-user/autocompletion-comics/python_package/src/main.py --aws"
                "python /home/ec2-user/test.py"
            ]
        },
    )

    command_id = response["Command"]["CommandId"]

    # Check command status
    output = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId="i-0b88b6d191f445ba1",  # replace with your instance ID
    )


def check_for_new_files():
    current_files = set()

    while True:
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=RESULT_DIR)

        if "Contents" in response:
            new_files = set(obj["Key"] for obj in response["Contents"])
            if new_files != current_files:
                print("New file detected!")
                current_files = new_files
                break  # remove this if you want to keep checking for new files

        time.sleep(10)


if __name__ == "__main__":
    if not os.path.exists("uploads/"):
        os.makedirs("uploads/")
    app.run(debug=True)
