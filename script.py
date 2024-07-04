import random
import string
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import time
import csv

import secrets

def generate_access_key_and_secret_key():
    """Generates random access key ID and secret access key (insecure)."""
    access_key_id = secrets.token_urlsafe(32)
    secret_access_key = secrets.token_urlsafe(40)
    return access_key_id, secret_access_key

def generate_access_key_id():
    """Generate a random AWS-like Access Key ID"""
    prefix = 'AKIA'
    characters = string.ascii_uppercase + string.digits
    key_id = prefix + ''.join(random.choice(characters) for _ in range(28))
    return key_id

def generate_secret_access_key():
    """Generate a random AWS-like Secret Access Key"""
    characters = string.ascii_letters + string.digits + string.punctuation
    # AWS secret access keys typically do not include certain punctuation characters
    safe_characters = characters.replace('"', '').replace("'", '').replace('\\', '')
    secret_key = ''.join(random.choice(safe_characters) for _ in range(40))
    return secret_key

def verify_access_keys(access_key_id, secret_access_key):
    """Verify if the provided AWS access keys are valid."""
    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name='us-east-1'  # Example region
    )
    try:
        s3 = session.client('s3')
        s3.list_buckets()  # Simple API call to list S3 buckets
        print("Access Key is valid!")
        return True
    except (ClientError, NoCredentialsError, PartialCredentialsError) as error:
        print(f"Failed to use access key: {error}")
        return False

def save_keys_to_csv(filename, access_key_id, secret_access_key):
    """Save the access key ID and secret access key to a CSV file."""
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([access_key_id, secret_access_key])
        print("Key written to CSV file.")

def main():
    filename = 'aws_api_keys.csv'
    port = 0

    while True:
        access_key_id = generate_access_key_id()
        secret_access_key = generate_secret_access_key()

        print(f"Access Key ID: {access_key_id}")
        print(f"Secret Access Key: {secret_access_key}")

        port += 1

        if port >= 203:
            save_keys_to_csv(filename, access_key_id, secret_access_key)
            try_count = 0  # Reset the count after adding a key

        time.sleep(2)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
