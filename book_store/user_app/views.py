from .models import UserModel
from .serializer import UserSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
import logging
from django.contrib.auth.models import auth
from utility.jwt import JwtCode
# Create your views here.


class UserRegister(APIView):

    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        Register User based on the details given
        :return: Json Response
        """
        try:
            received_user = UserSerializer(data=request.data)
            if received_user.is_valid():
                user = UserModel.objects.create_user(username=received_user.data['username'],
                                                     password=received_user.data['password'],
                                                     email=received_user.data['email'],
                                                     first_name=received_user.data['first_name'],
                                                     last_name=received_user.data['last_name'],
                                                     phone=received_user.data['phone'],
                                                     )
                created_user = UserSerializer(user)
                data = created_user.data['username']
                token = JwtCode().encoder(data)
                return JsonResponse({'success': True, 'message': 'Registration Successfull', 'token': token})
            else:
                self.logger.debug(msg=f"invalid data {received_user.data}")
                return JsonResponse({'success': False, 'message': 'Data is invalid', 'data': 'Invalid'})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'Data is invalid or duplicate', 'data': 'Invalid'})


class UserLogin(APIView):

    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        Check if the user exists and logged in invalid data
        :param request: Request sent from the user
        :return: Json response
        """

        try:
            received_data = UserSerializer(data=request.data)
            does_user_exist = auth.authenticate(username=received_data.initial_data.get('username'),
                                                password=received_data.initial_data.get('password'))
            if does_user_exist:
                data = received_data.initial_data.get('username')
                token = JwtCode().encoder(data)
                return JsonResponse({'success': True, 'message': 'Successfully logged in',
                                     'data': token})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'Error occured'})

    def get(self, request):
        """
        Get all user username
        :param request:
        :return: All usernames
        """

        try:
            users = UserModel.objects.all()
            user_dict = UserSerializer(users, many=True)
            username_list = []
            for user in user_dict.data:
                username_list.append(user['username'])
            return JsonResponse({'success': True, 'message': 'Data fetched', 'data': username_list})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'Error occurred'})

