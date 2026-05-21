class FirebaseOutputStrategy:
    def __init__(self, service_account_file, collection):
        self.service_account_file = service_account_file
        self.collection = collection

    def output(self, data):
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            cred = credentials.Certificate(self.service_account_file)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        for index, item in enumerate(data):
            db.collection(self.collection).document(str(index + 1)).set(item)

        return f"Data was written to Firebase Firestore collection: {self.collection}"