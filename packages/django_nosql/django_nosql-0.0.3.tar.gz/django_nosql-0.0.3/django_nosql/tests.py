# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, override_settings
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from django.conf import settings
import unittest

def create_fake_user():
    return get_user_model().objects.create(username='fake_user', password='testtest')

from .signals import FireStore

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

fb = FireStore(settings.FIRESTORE_CREDENTIALS_FILE)

class SignalsTestCase(TestCase):

    def setUp(self):
        self.user = create_fake_user()
        self.user.collection = 'test_users'
        self.user.serializer_path = 'django_nosql.tests.UserSerializer'

    @unittest.skip('integration test')
    def test_it_syncs_wth_firestore(self):
        fb.sync(self.user)

    @unittest.skip('integration test')
    def test_it_deletes_from_firestore(self):
        fb.delete(self.user)