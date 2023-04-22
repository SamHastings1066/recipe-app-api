"""
Serializers for the user API view.
"""
from django.contrib.auth import get_user_model

# Serializers model includes the tools we need for defining serializers.
# Serializers convert objects to and from python objects. They take
# 'adjacent' input from the API, validates it to make sure it is secure and
# adheres to validation rules, and then converts it into a python object or
# a model we can user in our database.
from rest_framework import serializers


# ModelSerializer is a base class from the serializers module. It creates
# model serializers - which allow us to validate and save thing to a model
# defined in our serilazer.
class UserSerializer(serializers.ModelSerializer):
  """Serializer for the user object."""

  # The Meta class tells the django rest framework the model, fields and
  # any additional arguments we want to pass to the serializer.
  class Meta:
    model = get_user_model() # this serializer is for our user model
    # The list of fields that we ant to make available through the serializer
    # they are created when we make a request to be saved in the model that is
    # created. We don't want to include things like is_active or is_staff
    # because when users create objects they could set those values
    # themselves in the request. Only allo fileds that you want the user to
    # be able to change using the API.
    fields = ['email', 'password', 'name']
    # Dict allowing us to provide extra meta data to the fields e.g.
    # whether we want a field to be write-only/read-only. Write_only
    # menas the user will be able to set the value but the value wont
    # be returned in the API response. So they can write values to password
    # but not read it.
    extra_kwargs = {'password': {'write_only': True, 'min_length':5}}

  # This method overrides the serializers behaviour when creating new
  # objects. The default behaviour to create an object with whatever
  # values are passed in. E.g. if you pass in the password field, by default
  # the serializer will save it as text in the model. We want it to
  # pass out password thorugh encryption. We do so using the create_user
  # method we provided to our model manager.
  # We pass in the validated data from our serializer. The create() method
  # is only called when the validation is successful.
  def create(self, validated_data):
    """Create and return a user with encrypted password."""
    return get_user_model().objects.create_user(**validated_data)
