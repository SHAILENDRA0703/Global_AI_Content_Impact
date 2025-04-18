from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id='AKIA4HCKTXCYHKSBVDOY',
                  aws_secret_access_key='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',
                  region_name='Europe (Stockholm) eu-north-1')

BUCKET_NAME = 'shailendra-ai-impact-bucket'  

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    s3.upload_fileobj(file, BUCKET_NAME, file.filename)

    return jsonify({"message": f"{file.filename} uploaded to {BUCKET_NAME}!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
