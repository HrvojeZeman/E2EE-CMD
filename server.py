from fastapi import FastAPI, File, UploadFile
import shutil
import os
from fastapi.security import \
	HTTPBasicCredentials
import urllib3
import mysql.connector


app = FastAPI()

UPLOAD_DIR = r"C:\Users\Hrvoje\OneDrive - Univerza v Mariboru\Namizje\Library of Congress\Moji prispevki\AES Enkripcija\uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
	file_path = os.path.join(UPLOAD_DIR, file.filename)
	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)
	return {"filename": file.filename, "path": file_path}

@app.post("/authenticate/")
async def authenticate(credentials: HTTPBasicCredentials = HTTPBasicCredentials()):
	pass

def DoesUserExist(username: str, password: str):
	connection = mysql.connector.connect(
	host="localhost",
	user="your_username",
	password="your_password",
	database="your_database"
)

# Create a cursor object
# cursor = connector.cursor()

# Example query
# cursor.execute("SELECT * FROM your_table")

# cr_2uHGya3gOh5nQqQyNaAdTN9kR9d
