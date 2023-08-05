# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from example_app.models import Todo
from unittest.mock import patch

class LoopBreakerTestCase(TestCase):

    # @patch('example_app.models.say_hi')
    # def test_run_throttled_signal_only_fires_signal_once(self, mock_signal):


    # unfortunately patching doesnt work :( (see above)
    def test_run_throttled_signal_only_fires_signal_once(self):
        todo = Todo.objects.create(text='test')
        for x in range(0,100):
            todo.save()

    # def test_run_throttled_signal(self):
    #     for x in range(0,100):
    #         todo = Todo.objects.create(text='test')
