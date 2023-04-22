"""
Views for the user API.
"""
# rest_framework handles a lot of the logic that we need to create objects in
# the database. It does that by providing different base classes that we can
# configure for our views that will handle the base request in a standardized
# way. We can also override some of that behaviour.
from rest_framework import generics

from user.serializers import UserSerializer


# The CreateAPIView base class from generics handles HTTP post requests
# designed for creating objects. You just need to tell it which Serializer
# to use. It knows which model to create the new object in because the model
# is defined in the serializer.
class CreateUserView(generics.CreateAPIView):
  """Create a new user in the system"""
  serializer_class = UserSerializer
