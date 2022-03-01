from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Cart
from .serializer import CartSerializer
from user_app.models import UserModel
from book_app.models import BookModel
import logging

# Create your views here.


class AddToCart(APIView):

    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        Add items to cart.
        :param request: cart item data
        :return: Json response of cart added
        """
        try:
            book_object = BookModel.objects.get(book_name=request.data['book_name'])
            user_object = UserModel.objects.get(username=request.data['username'])
            if Cart.objects.filter(user_id=user_object.id, book_id=book_object.id).exists():
                return JsonResponse({'status': 'Failure', 'message': 'Details already exist', 'data': request.data})

            book_price = book_object.book_price
            total_price = float(book_price) * int(request.data['quantity'])
            cart = Cart(user_id=user_object,
                        book_id=book_object, quantity=request.data['quantity'],
                        total_price=total_price)
            cart.save()
            cart_object = CartSerializer(cart)
            return JsonResponse({'status': 'success', 'message': 'added to cart', 'data': cart_object.data})
        except Exception as e:
            self.logger.debug(msg=e)
            print(e)
            return JsonResponse({'status': 'Failure', 'message': 'failed to add data', 'Error': e})

    def get(self, request):
        """
        get all items from cart.
        :param request: empty
        :return: Json response of cart items
        """
        try:
            cart = Cart.objects.all()
            cart_objects = CartSerializer(cart, many=True)
            return JsonResponse({'status': 'success', 'message': 'added to cart', 'data': cart_objects.data})
        except Exception as e:
            self.logger.debug(msg=e)
            print(e)
            return JsonResponse({'status': 'Failure', 'message': 'failed to fetch data', 'Error': e})

    def put(self, request):
        """
        update item of cart.
        :param request: cart item data
        :return: Json response of cart added
        """
        try:
            book_object = BookModel.objects.get(book_name=request.data['book_name'])
            user_object = UserModel.objects.get(username=request.data['username'])
            cart = Cart.objects.get(user_id=user_object.id, book_id=book_object.id)
            if cart:
                book_price = book_object.book_price
                total_price = float(book_price) * int(request.data['quantity'])
                new_cart_data = Cart(user_id=user_object,
                                     book_id=book_object, quantity=request.data['quantity'],
                                     total_price=total_price)
                cart_item = CartSerializer(cart, data=new_cart_data)
                cart_item.is_valid()
                cart_item.save()
                return JsonResponse({'status': 'success', 'message': 'updated the cart item', 'data': cart_item.data})
        except Exception as e:
            self.logger.debug(msg=e)
            print(e)
            return JsonResponse({'status': 'Failure', 'message': 'failed to fetch data', 'Error': e})

    def delete(self, request):
        """
        delete item from cart.
        :param request: cart item to delete
        :return: Json response
        """
        try:
            book_object = BookModel.objects.get(book_name=request.data['book_name'])
            user_object = UserModel.objects.get(username=request.data['username'])
            if Cart.objects.get(user_id=user_object.id, book_id=book_object.id).delete():
                return JsonResponse({'status': 'success', 'message': 'Deleted the cart item'})
            else:
                return JsonResponse({'status': 'Failure', 'message': 'Given data doesnt exist'})
        except Exception as e:
            self.logger.debug(msg=e)
            print(e)
            return JsonResponse({'status': 'Failure', 'message': 'failed to fetch data', 'Error': "Doesnt exist"})
