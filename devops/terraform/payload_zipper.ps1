# run it at repo root
Copy-Item -Path "app/app.py" -Destination "devops/terraform/lambda_function_payload/"
Set-Location "devops/terraform/lambda_function_payload/"
pip install  --upgrade -r "../../../app/requirements.txt" -t .

Compress-Archive -Path . -DestinationPath ../lambda_function_payload.zip
# Add-Type -A 'System.IO.Compression.FileSystem'
# [IO.Compression.ZipFile]::CreateFromDirectory('.', './lambda_function_payload.zip')