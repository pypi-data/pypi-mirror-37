import importlib, firebase_admin
from firebase_admin import credentials, firestore


class NoSQLBackend:

    def __get_serializer_class(self, serializer_path):
        bits = serializer_path.split('.')
        class_name = bits.pop()
        module_string = (".").join(bits)
        mod = importlib.import_module(module_string)
        return getattr(mod, class_name)

    def get_serialized(self, instance, created = False):
        serializer = self.__get_serializer_class(instance.serializer_path)
        dta = serializer(instance).data
        id = str(instance.id)
        return (id, dta)


class MockNoSQL(NoSQLBackend):

    def sync(self, instance, created = False):
        id, dta = self.get_serialized(instance, created)
        return dta

    def delete(self, instance):
        return instance


class FireStore(NoSQLBackend):

    def __init__(self, path_to_credentials):
        super().__init__()
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(path_to_credentials)
            app = firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def sync(self, instance, created = False):
        id, dta = self.get_serialized(instance, created)
        return self.db.collection(instance.collection).document(id).set(dta)

    def delete(self, instance):
        return self.db.collection(instance.collection)\
            .document(str(instance.id))\
            .delete()
