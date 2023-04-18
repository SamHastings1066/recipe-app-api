""""
Test custom Django management commands.
"""
# We import patch to mock the behaviour of the database to simulate the db
# returning a response
from unittest.mock import patch

# OperationalError is one of the errors we might get from psycopg2 when we try
# to connect to a db before it is ready.
from psycopg2 import OperationalError as Psycopg2Error

# call_command is a helper function from django allowing us to call a command
# by its name
from django.core.management import call_command
# import another operational error that may get thrown by the db.
from django.db.utils import OperationalError
# import the simpleTestCase - the base test class.
from django.test import SimpleTestCase


# we mock db behaviour using @patch. we do this for all test methods by
# decorating the class with patch. We provide patch with the path to the
# command we are going to be mocking. We use the Command.check method that
# wait_for_db has inherited from the BaseCommand class. We mock that 'check'
# method to simulate the response.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # the patched check object will be passed in as aparam to this func
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if datbase ready.
        In the case that we run the wait_for_db command and the database is in
        fact ready, we want the wait_for_db command to allow us to continue.
        """
        # When check is called inside our command inside our test case, we just
        # want to return the value True.
        patched_check.return_value = True

        call_command('wait_for_db')

        # Ensure that the mocked object (the check method inside our command)
        # is called with these parameters
        patched_check.assert_called_once_with(databases=['default'])

    # Tets what happens when the database isn't ready
    # arguments are applied inside out. so time.sleep takes the patched_sleep
    # arg check takes the patched_check arg.
    # time.sleep replaces the sleep function with a mocked object.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error"""
        # die_effect allows you to raise exceptions and pass in objects that
        # are handled differently depending on their type: If we pass in an
        # exception then the mocking library knows to raise that exception.
        # if we pass in a boolean it will return a boolean value. The line
        # below says the first two times we call the mocked method (check) we
        # want it to raise the Pscycopg2Error, then we raise three operational
        # errors.
        # These are arbitrary values. The Psycopg2Error is returned when pg
        # hasn't even started up yet. The OperationalError, from django, is
        # from when the dev database hasn't been set up yet.
        # The sixth time we call check it returns True.

        patched_check.side_effect = [Psycopg2Error] * 2 + \
          [OperationalError] * 3 + [True] # noqa

        call_command('wait_for_db')

        # ensure the mocked 'check' method was called 6 times
        self.assertEqual(patched_check.call_count, 6)
        # make sure that patched_check is called with database as default
        patched_check.asset_called_with(databases=['default'])
