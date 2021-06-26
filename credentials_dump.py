import os

credentials_json = os.getenv('GOOGLE_CREDENTIALS')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

with open(credentials_path, 'w') as file:
    file.write(credentials_json)
