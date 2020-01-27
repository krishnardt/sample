from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, JoinListGroupSerializer, ListGroupSerializer, ProfileViewSerializer#, LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout#, password_reset
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import List_group, Profile, User_list_group
from django.http import JsonResponse
import json
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail
from auth_api.settings import EMAIL_HOST_USER


# Create your views here.

'''
class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
'''

'''
sample code
'''
class HelloView(APIView):
    #permission_classes = (IsAuthenticated,)
    # permission_classes = [IsAuthenticated, ]
    def get(self, request):
        print(request.data)
        content = {'message': 'Hello, World!'}
        return Response(content)



'''
user signup class view
data format is:
{"username":"krishna",
"first_name":"Krish",
 "last_name":"Na",
 "email":"krishnardt365@gmail.com", 
"password":"12345",
"profiles":
[{"gender":"Male", 
"mobile_no":"+91960637709",
 "about":"sd ad asf ",
 "location":"Hyderabad"}]}
'''
class RegisterView(APIView):
	def post(self, request, format = None):
		print(request.data)
		print(request.session.items())
		#profiles_data = request.data['profiles']
		#print(profiles_data)
		# data = {"username":"krishna",
		# 	"first_name":"Krish",
		# 	 "last_name":"Na",
		# 	 "email":"krishnardt365@gmail.com", 
		# 	"password":"12345",
		# 	"profiles":[
		# 	{"gender":"Male", 
		# 	"mobile_no":"+91960637709",
		# 	 "about":"sd ad asf ",
		# 	"location":"Hyderabad"},],}
		serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			print("serializer is is_valid.............")
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




'''
login of user
data format is:
{"username":"krishna", "password":"1234@qwer"}

'''
class LoginView(APIView):
	authentication_classes = (JSONWebTokenAuthentication,)
	def post(self, request, format=None):
		print(request.data)
		
		#serializer = LoginSerializer(data = request.data)
		data = request.data
		# if serializer.is_valid():
		# 	print("serializer is is_valid.............")
		# 	serializer.save()
		# 	return Response(serializer.data, status=status.HTTP_201_CREATED)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		#serializer.is_valid(raise_exception=True)
		#user = serializer.validated_data['username']
		username = data.get('username', None)
		password = data.get('password', None)
		user = authenticate(request, username = username, password=password)
		request.user = user
		if username and password:
			if user:
				print("User active")
				if user.is_active:
					data['username'] = username
				else:
					mesg = "user account is deactivated..."
					raise exceptions.ValidationError(mesg)
			else:
				mesg = "Credentials doesnt match with any account..."
				raise exceptions.ValidationError(mesg)
			login(request, user)
			print(request.session.items())
		else:
			mesg = "must provide both username and password"
			raise exceptions.ValidationError(mesg)
		
		token, created = Token.objects.get_or_create(user=user)
		return Response({"token":token.key}, status=200)
        



class LogoutView(APIView):
	authentication_classes=(TokenAuthentication,)
	def post(self, request, format=None):
		print(request.session.items())
		logout(request)
		return Response(status=204)

		
'''
insert group or list into table List_group
data format:
{"name":"CVIT2018",
"admin":["krishnardt365@gmail.com"],
"is_group":"True"
}
'''
@method_decorator(login_required, name='dispatch')
class ListGroupView(LoginRequiredMixin, APIView):
	def post(self, request, format = None):
		print(request.POST)
		data = request.data
		#print(data['admin'][0])
		user_id = User.objects.all()
		print(user_id)
		user_id = user_id.filter(email = data['admin'][0]).values('id')[0]['id']
		
		del data['admin']
		data['admin'] = user_id
		print(data)
		serializer = ListGroupSerializer(data = data)
		if serializer.is_valid():
			print("serializer is is_valid.............")
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''
to display the total no of groups present

'''
@method_decorator(login_required, name='dispatch')
class ListGroups(LoginRequiredMixin, APIView):
	def get(self, request, format=None):
		#listGroups = [group for group in List_group.objects.all()]
		listGroups = list(List_group.objects.all().values('name', 'is_group'))
		print(listGroups)
		return HttpResponse(json.dumps(listGroups))#JsonResponse({listGroups})

# class PasswordChange(APIView):
# 	authentication_classes=(TokenAuthentication,)
# 	def post(self, request, format=None):
# 		password_reset(request)
# 		return Response(status=204)


'''
to update profile..
data format:
{"gender":"Female", "about":"sd ad asf "}
'''
@method_decorator(login_required, name='dispatch')
class UpdateProfile(LoginRequiredMixin, APIView):
	def post(self, request, format=None):
		print(request.session.items())
		#'_auth_user_id'
		id = request.session['_auth_user_id']
		data = request.data
		print(data.items())
		print(data.keys())
		try:
			user_data = Profile.objects.get(user_id_id = id)#.values('gender', 'location')
			#print(dict(user_data))
			# fields = [f.name for f in Profile._meta.fields]
			# print(fields)
			# print(user_data)

			if 'gender' in data.keys():
				user_data.gender = data['gender']
			if 'mobile_no' in data.keys():
				user_data.mobile_no = data['mobile_no']
			if 'about' in data.keys():
				user_data.about = data['about']
			if 'location' in data.keys():
				user_data.location = data['location']
			user_data = user_data.save()
			return Response("updated data....", status=204)
		except:
			return Response("failed to update...", status = 401)

		print(user_data)


'''
{
	"is_working_group":"True",
	"email_access":"True",
	"mobile_access":"False",
	"is_group":"True",
	"groups_id_id":["CVIT2018"]
}
'''
@method_decorator(login_required, name='dispatch')
class SelectListGroupsView(LoginRequiredMixin, APIView):
	def post(self, request, format=None):
		print(request.POST)
		data = request.data
		#print(data['admin'][0])
		# user_id = User.objects.all()
		# print(user_id)
		# user_id = user_id.filter(id = data['user_id_id'][0]).values('id')[0]['id']
		user_id = int(request.session['_auth_user_id'])

		group_id = List_group.objects.all()
		print(group_id)
		group_id = group_id.filter(name = data['groups_id_id'][0]).values('id')[0]['id']
		
		#del data['user_id_id']
		data['user_id'] = user_id

		del data['groups_id_id']
		data['groups_id'] = group_id


		print(data)
		serializer = JoinListGroupSerializer(data = data)
		if serializer.is_valid():
			print("serializer is is_valid.............")
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(login_required, name='dispatch')


class ShowMyGroupsList(LoginRequiredMixin, APIView):
	def get(self, request, format = None):
		user_id = int(request.session['_auth_user_id'])
		userListGroups = list(User_list_group.objects.filter(user_id=user_id).values('user_id_id', 'groups_id_id','is_working_group', 'email_access', 'mobile_access', 'is_group'))
		print(userListGroups)
		return HttpResponse(json.dumps(userListGroups))#JsonResponse({listGroups})


@method_decorator(login_required, name='dispatch')
class SendLinkView(LoginRequiredMixin, APIView):
	def post(self, request, format=None):
		data = request.data
		email = data['email']
		current_site = get_current_site(request)
		print(current_site.domain)
		print(current_site.name)
		print(email)
		subject = 'Please Activate Your Account'
		# message = render_to_string('activation_request.html', {
		#     'user': user,
		#     'domain': current_site.domain,
		#     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		#     'token': account_activation_token.make_token(user),
		# })
		#pro_link = str(current_site)+'/authorizer/temlpates/accountSignup.html'
		pro_link = str(current_site)+'/auth/register'
		print(pro_link)
		send_mail('Createaccount to  become %s user with the beow link........' % current_site.name,
			pro_link,
			
			EMAIL_HOST_USER, #'editor@%s' % current_site.domain,
			[email],#'darsisuhas666@gmail.com'
		fail_silently=False)
		return HttpResponse("send mail to the user......")

@method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, APIView):
	def get(self, request, format=None):
		id = request.session['_auth_user_id']
		data = Profile.objects.get(user_id = id).__dict__
		serializer = ProfileViewSerializer(data)
		data = serializer.data
		data['username'] = User.objects.filter(id = data['user_id_id']).values('username')[0]['username']
		del data['user_id_id']
		return HttpResponse(json.dumps(data)) 




'''
def sendLink(request):
    ''''''
    print("extra....")
    email = request.POST['email_id']
    print(email)
    current_site = get_current_site(request)
    print(current_site.domain)
    subject = 'Please Activate Your Account'
    # message = render_to_string('activation_request.html', {
    #     'user': user,
    #     'domain': current_site.domain,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user),
    # })
    #pro_link = str(current_site)+'/authorizer/temlpates/accountSignup.html'
    pro_link = str(current_site)+'/authorizer/accountlink'
    send_mail(
        'Createaccount to  become %s user with the beow link........' % current_site.name,
        pro_link,
        email, #'editor@%s' % current_site.domain,
        [email],
    fail_silently=False)
    #user.email_user(subject, message)
    return redirect('sentlink')
'''