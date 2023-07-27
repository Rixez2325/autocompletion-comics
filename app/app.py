import time
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
import boto3

S3_BUCKET = "autocompletion-comics-buckets"
PDF_DIR = "datasets/pdf"
RESULT_DIR = "datasets/generated_page"
EC2_INSTANCE_ID = "i-0b88b6d191f445ba1"  # "i-0c081f69c808982e6"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"  # change to your preferred upload directory

s3 = boto3.client("s3")
aws_session = boto3.Session(region_name="eu-west-1")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    # ec2 = aws_session.resource("ec2")
    # ec2.Instance(EC2_INSTANCE).start()
    # time.sleep(10)
    import logging

    logging.basicConfig(level=logging.DEBUG)

    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in the form"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET, f"{PDF_DIR}/{filename}")
            run_ec2_process()
            return "File uploaded successfully, processing in progress ..."
    return """
    <!doctype html>
    <html>
    <head>
        <title>comics-generator</title>
        <style>
            body {
                font-family: 'Comic Sans MS', sans-serif;
                background-image: url("https://example.com/path/to/comic/background.png");
                background-repeat: repeat;
                padding: 50px;
            }
            h1 {
                color: #444;
                text-align: center;
            }
            form {
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            .drop_zone {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                margin: 20px 0;
                cursor: pointer;
                color: #aaa;
            }
            .drop_zone.dragover {
                border-color: #008CBA;
                color: #008CBA;
            }
            .custom-file-upload {
                display: inline-block;
                padding: 6px 12px;
                cursor: pointer;
                margin-top: 20px;
                border-radius: 4px;
                background-color: #008CBA; 
                color: white; 
            }
            input[type=submit] {
                background-color: #4CAF50; 
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 20px 2px;
                cursor: pointer;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            #file {
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>Upload a PDF File</h1>
        <form method="POST" enctype="multipart/form-data">
            <div id="drop_zone" class="drop_zone">Drag and drop a file<br>
                
            </div>
            <label for="file" class="custom-file-upload">update from computer</label>
            <input id="file" type="file" name="file">
            <br>
            <input type="submit" value="Upload">
        </form>
        <script>
            const dropZone = document.getElementById('drop_zone');
            const fileInput = document.getElementById('file');

            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });

            dropZone.addEventListener('dragleave', (e) => {
                dropZone.classList.remove('dragover');
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                fileInput.files = e.dataTransfer.files;
                dropZone.innerText = `File selected: ${fileInput.files[0].name}`;
            });

            fileInput.onchange = function () {
                dropZone.innerText = `File selected: ${this.files[0].name}`;
            };
        </script>
    </body>
    </html>

    """


def run_ec2_process():
    ssm = boto3.client("ssm", region_name="eu-west-1")  # replace with your region

    response = ssm.send_command(
        InstanceIds=[EC2_INSTANCE_ID],  # replace with your instance ID
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [
                "python3 /home/ec2-user/autocompletion-comics/python_package/src/main.py --aws"
                # "python3 /home/ec2-user/test.py"
            ]
        },
    )
    command_id = response["Command"]["CommandId"]

    time.sleep(5)

    # Check command status
    while True:
        output = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=EC2_INSTANCE_ID,
        )

        if output["Status"] != "InProgress":
            print("Command output:", output["StandardOutputContent"])
            break


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


# Lambda handler function
def lambda_handler(event, context):
    with app.test_request_context(
        path=event["path"], method=event["httpMethod"], headers=event["headers"]
    ):
        try:
            rv = app.full_dispatch_request()

            if rv.status_code == 302 and not rv.autocorrect_location_header:
                rv.autocorrect_location_header = True

            headers = dict(rv.headers)
            body = rv.get_data()

            if "Content-Type" not in headers:
                headers["Content-Type"] = "text/plain"

            return {
                "statusCode": rv.status_code,
                "headers": headers,
                "body": body.decode("utf-8"),
                "isBase64Encoded": False,
            }

        except Exception as e:
            response = Response(
                "An error occurred: %s\n" % str(e),
                status=500,
                headers={"Content-Type": "text/plain"},
            )
            headers = dict(response.headers)
            body = response.get_data()

            return {
                "statusCode": response.status_code,
                "headers": headers,
                "body": body.decode("utf-8"),
                "isBase64Encoded": False,
            }


if __name__ == "__main__":
    app.run(debug=True)
