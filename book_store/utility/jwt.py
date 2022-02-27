import jwt


class JwtCode:

    def encoder(self, data):
        """
        Encode the given data and return encoded token
        :param data: 
        :return: encoded token
        """
        return jwt.encode({'data': data}, 'book_store', 'HS256')

    def decoder(self, token):
        """
        Decode the given token and return encoded token
        :param token: 
        :return: encoded token
        """
        return jwt.decode(token, 'book_store', 'HS256')


class VerifyToken:

    def verify_token(self, request):
        """
        Given request, extract token and decode it to verify
        :param request:
        :return: boolen
        """
        bearer_token = request.META["HTTP_AUTHORIZATION"]
        token_data = JwtCode().decoder(bearer_token)
        if token_data:
            return token_data.get('data')
        return False
