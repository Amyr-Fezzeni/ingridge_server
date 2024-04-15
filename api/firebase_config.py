import firebase_admin
from firebase_admin import credentials, firestore
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(f"{base_dir}/firebase_credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
print('Logged in')


usersCollection = db.collection('users')
