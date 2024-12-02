from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Task, User
from api.serializers import UserSerialzier, LoginSerializer, TaskSerializer

#registerView
class RegisterView(APIView):
    
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerialzier(data =data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'message': 'Account created successfully'}, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)


#loginView
class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.data)
                #print(response)
                return Response( response, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
#taskView
class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            tasks = Task.objects.filter(user = request.user)
            if not tasks:
                return Response({'detail': 'No tasks found for this user.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(tasks, many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = TaskSerializer(data = data)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request,pk=None):
        try:
            data = request.data     
            task = Task.objects.get(id = pk)
            
            if task.user!= request.user:
                raise Exception('You are not authorized to update this task')

            serializer = TaskSerializer(task, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Task updated successfully'}, status = status.HTTP_200_OK)
            print(serializer.errors)
            return Response({
                'message': 'something went wrong'
                },
                status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status = status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            #task = get_object_or_404(Task, id = pk)
            task = Task.objects.get(id=pk)
            print(id)
            # print(task.user)
            # print(request.user)
            if task.user !=  request.user:
                return Response("You are not authorized to delete this task")

            task.delete()
            return Response({'message': 'task deleted successfully'}, status = status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        

class DeleteAllTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def delete(self, request):
        try:
            user_tasks = Task.objects.filter(user = request.user)
            if not user_tasks:
                return Response({"detail": "No tasks found for the logged-in user."}, status=status.HTTP_404_NOT_FOUND)
            user_tasks.delete()
            return Response({"message": "All tasks deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

def index(request):
    if(request.user.is_authenticated) :
        return render(request, 'tasks.html')
    else:
        return render(request, 'register.html')
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)