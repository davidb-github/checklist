#View module for handling requests about tasks
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from checklistapi.models import Task, MyUser


class Tasks(ViewSet):

    #Handle GET requests to get all tasks Returns: Response:JSON serialized list of all tasks
    def list(self, request):
        # Get all task records from database
        all_tasks    = Task.objects.all()
        # Get current logged in user
        current_user = MyUser.objects.get(user=request.auth.user)
        # Get all tasks associated to the current_user
        all_tasks    = all_tasks.filter(user=current_user)

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TaskSerializer(
            all_tasks, many=True, context={'request': request})

        return Response(serializer.data)

    #Handle GET requests for single task Returns:Response -- JSON serialized task
    def retrieve(self, request, pk=None):
        try:
            task       = Task.objects.get(pk=pk)
            serializer = TaskSerializer(
                task, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    #Handle POST operations for tasks Returns: Response -- JSON serialized task instance
    def create(self, request):
        current_user = MyUser.objects.get(user=request.auth.user)

        # Grab data from client's request to build a new task instance
        task                  = Task()
        task.user             = current_user
        task.task_name        = request.data["task_name"]
        task.task_description = request.data["task_description"]
        task.is_complete      = False

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            task.save()
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    #Handle PUT requests for a task Returns:Response -- Empty body with 204 status code
    def update(self, request, pk=None):
        current_user = MyUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Task, get the task record
        # from the database whose primary key is `pk`
        task                  = Task.objects.get(pk=pk)
        task.user             = current_user
        task.task_name        = request.data["task_name"]
        task.task_description = request.data["task_description"]
        task.is_complete      = request.data["is_complete"]

        # Save the updated task instance to database,
        # overwriting the original values.
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    #Handle DELETE requests for a single game Returns: Response -- 200, 404, or 500 status code
    def destroy(self, request, pk=None):

        try:
            task = Task.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## Serializers ##

#JSON serializer for default Django Users Arguments:serializers
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
                   'id',
                   'first_name',
                   'last_name'
                 )
        depth = 1

#JSON serializer for tasks Arguments: serializers
class MyUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = MyUser
        fields = (
                  'id',
                  'user'
                 )
        depth = 1

#JSON serializer for Tasks Arguments: serializers
class TaskSerializer(serializers.ModelSerializer):

    user = MyUserSerializer(many=False)

    class Meta:
        model = Task
        fields = (
                  'id', 
                  'user',
                  'task_name',
                  'task_description',
                  'creation_date',
                  'is_complete'
                 )
        depth = 1