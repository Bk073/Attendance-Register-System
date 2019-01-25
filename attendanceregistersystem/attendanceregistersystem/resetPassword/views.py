from django.shortcuts import render
from djoser.email import PasswordResetEmail
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm

# class PasswordResetEmail(BaseEmailMessage):
#     template_name = 'email/password_reset.html'

#     def get_context_data(self):
#         context = super(PasswordResetEmail, self).get_context_data()

#         user = context.get('user')
#         context['uid'] = utils.encode_uid(user.pk)
#         context['token'] = default_token_generator.make_token(user)
#         context['url'] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
#         return context

from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# class PasswordResetView(PasswordResetConfirmView):
class PasswordResetView(APIView):
    permission_classes=(AllowAny,)
    def get (self, request, uid, token):
        post_data = {'uid': uid, 'token': token}
        return Response(post_data)
    

# class PasswordResetView(PasswordResetConfirmView):

def reset_confirm(request, uid, token):
    return password_reset_confirm(request,
        token=token, post_reset_redirect=reverse('password_reset_confirm'))
