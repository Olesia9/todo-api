from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from datetime import date, timedelta
from .decorators import define_usage
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED


# URL /
@define_usage(returns={'url_usage': 'Dict'})
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_index(requet):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == 'api_':
            if hasattr(item[1], 'usage'):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)


# URL /signin/
@define_usage(params={'username': 'String', 'password': 'String'},
              returns={'authenticated': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signin(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except:
        return Response({'error': 'Please provide correct username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})


# /register/ Регистрация клиента
@define_usage(params={'username': 'String', 'password': 'String', 'email': 'String'},
              returns={'registered': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signup(request):
    try:
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
    except KeyError:
        return Response({'error': 'Please provide username, password, and email'},
                        status=HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'registered': True, 'token': "Token " + token.key}, status=HTTP_201_CREATED)
    else:
        return Response({'registered': False, 'token': None}, status=HTTP_400_BAD_REQUEST)


# URL /all/
@define_usage(returns={'tasks': 'Dict'})
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_all_tasks(request):
    tasks = TaskSerializer(request.user.task_set.all(), many=True)
    return Response({'tasks': tasks.data})


# URL /new/
@define_usage(params={'description': 'String', 'due_in': 'Int'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_new_task(request):
    task = Task(user=request.user,
                description=request.data['description'],
                due=date.today() + timedelta(days=int(request.data['due_in'])))
    task.save()
    return Response({'done': True})


# URL /update/
@define_usage(params={'task_id': 'Int', 'description': 'String', 'due_in': 'Int'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_update_task(request):
    task = request.user.task_set.get(id=int(request.data['task_id']))
    try:
        task.description = request.data['description']
    except: # Description update is optional
        pass
    try:
        task.due = date.today() + timedelta(days=int(request.data['due_in']))
    except: # Due date update is optional
        pass
    task.save()
    return Response({'done': True})


# URL /delete/
@define_usage(params={'task_id': 'Int'},
              returns={'done': 'Bool'})
@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_delete_task(request):
    task = request.user.task_set.get(id=int(request.data['task_id']))
    task.delete()
    return Response({'done': True})
