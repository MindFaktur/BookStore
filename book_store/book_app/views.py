from django.shortcuts import render
from .serializer import BookSerializer
from .models import BookModel
from rest_framework.views import APIView
from django.http import JsonResponse
import logging
import json
from user_app.models import UserModel
# Create your views here.


class AddBook(APIView):

    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        Get book details from user and create book
        :param request:
        :return: Json response
        """

        try:
            book = BookSerializer(data=request.data)
            book.is_valid()

            if UserModel.objects.filter(username=request.data['username']).exists() and BookModel.objects.filter(book_name=request.data['book_name']).exists():
                return JsonResponse({'success': False, 'message': 'Book_name already exists'})

            book.save()
            return JsonResponse({'success': True, 'message': 'Book created successfully',
                                 'data': book.data})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'Duplicate or Invalid Details provided'})

    def get(self, request):
        """
        Get all books
        :param request:
        :return: Books
        """

        try:
            all_books = BookModel.objects.all()
            book_dict = BookSerializer(all_books, many=True)
            return JsonResponse({'success': True, 'message': 'Fetched all', 'data': book_dict.data})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': 'False', 'message': 'Error'})

    def put(self, request):
        """
        Update author_name and released date name based on book_name.
        :param request:
        :return: Json reponse of success or failure
        """

        try:

            if UserModel.objects.filter(username=request.data['username']).exists():
                book_object = BookModel.objects.get(book_name=request.data['book_name'])
                if book_object:
                    book = BookSerializer(book_object, data=request.data)
                    book.is_valid()
                    book.save()
                    return JsonResponse({'success': True, 'message': 'Successfully updated',
                                         'data': book.data})
                else:
                    return JsonResponse({'success': False, 'message': 'book_name does not exist'})
            else:
                return JsonResponse({'success': False, 'message': 'username does not exist'})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'error'})

    def delete(self, request):
        """
        Delete the book object based on given book_name
        :param request:
        :return: Json Response
        """

        try:
            if UserModel.objects.filter(username=request.data['username']).exists():
                if BookModel.objects.get(book_name=request.data['book_name']).delete():
                    return JsonResponse({'success': True, 'message': 'Deleted successfully'})
                else:
                    return JsonResponse({'success': False, 'message': 'book doesnt exist'})
            else:
                return JsonResponse({'success': False, 'message': 'username doesnt exist'})
        except Exception as e:
            self.logger.exception(msg=e)
            return JsonResponse({'success': False, 'message': 'book does not exists or error'})




