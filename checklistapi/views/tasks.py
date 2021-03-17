"""View module for handling requests about tasks"""
from django.db.models import query
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from datetime import date
from checklistapi.models import Task, MyUser


class Tasks(ViewSet):

    def list(self, request):
        """Handle GET requests to get all tasks
        Returns:
            Response -- JSON serialized list of all tasks
        """

        # Get all task records from database
        all_tasks = Task.objects.all()

        # Get current logged in user
        current_user = MyUser.objects.get(user=request.auth.user)

        # Get all tasks associated to the current_user
        all_tasks = all_tasks.filter(user=current_user)

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TaskSerializer(
            all_tasks, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for default Django Users
    Arguments:
        serializers
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        depth = 1


class MyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for tasks
    Arguments:
        serializers
    """

    user = UserSerializer(many=False)

    class Meta:
        model = MyUser
        fields = ('id', 'user')
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    """JSON serializer for Tasks
    Arguments:
        serializers
    """

    user = MyUserSerializer(many=False)

    class Meta:
        model = Task
        fields = ('id', 'user', 'task_name', 'task_description',
                  'creation_date', 'is_complete')
        depth = 1