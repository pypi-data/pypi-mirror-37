from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .backends import FireStore, MockNoSQL
from enum import Enum

class BACKENDS(Enum):
    FIRESTORE = 'firestore'
    MOCK = 'mock'

class SYNC_TYPE(Enum):
    UPDATE = 'update'
    DELETE = 'delete'

def get_readonly_backend(backend):
    if backend == BACKENDS.FIRESTORE.value:
        return FireStore(settings.FIRESTORE_CREDENTIALS_FILE)
    if backend == BACKENDS.MOCK.value:
        return MockNoSQL()

# todo: run these async
def perform_sync(instance, sync_type=SYNC_TYPE.UPDATE, created = False):
    model_requires_sync = getattr(instance, 'readonly_sync', False) == True

    if model_requires_sync:
        backends = getattr(settings, 'NOSQL_BACKENDS', [])
        for backend_name in backends:
            backend = get_readonly_backend(backend_name)
            if backend is not None:
                if sync_type == SYNC_TYPE.DELETE:
                    backend.delete(instance)
                else:
                    backend.sync(instance, created)


@receiver(post_save, dispatch_uid="django_nosql.sync")
def sync_readonly_db(sender, instance, created, **kwargs):
    perform_sync(instance, SYNC_TYPE.UPDATE, created)

@receiver(post_delete, dispatch_uid="django_nosql.sync.delete")
def sync_remove_readonly_db(sender, instance, **kwargs):
    perform_sync(instance, SYNC_TYPE.DELETE)
