import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("mental-maths-test-firebase-adminsdk-rpxil-eb13c9e20d.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# users = db.collection("users").stream()
# for user in users:
#     person = user.to_dict()
#     print(person.get('name'))

users = db.collection("users")
users.document("ivan.v.petrov@gmail.com").set({
    'name': 'Ivan',
    'hash': '0x42',
    'salt': '?/@£'
})


