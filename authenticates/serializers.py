from rest_framework import serializers
from .models import Profile, List_group, User_list_group
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, exceptions



class ProfileSerializer(serializers.ModelSerializer):
	#model = UserSerializer()
	
	class Meta:
		model = Profile
		fields = ['gender', 'mobile_no', 'about', 'location', 'user_id_id']
	

class UserSerializer(serializers.ModelSerializer):
	profiles = ProfileSerializer(many=True)
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'profiles']
	def create(self, validated_data):
		print(validated_data)
		profile_data = validated_data.pop('profiles')
		profile_data = dict(profile_data[0])
		print(profile_data)
		print(type(profile_data))
		print("printed the profile data.........")
		print(validated_data)
		validated_data['password'] = make_password(validated_data['password'])
		users,_ = User.objects.get_or_create(**validated_data)#.values('id')[0]['id']
		#user_data = dict(users)
		print(users)
		#print(user_data)
		print(type(users))
		#print(type(user_data))
		#user_id = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.filter(username = users[0]).values('id')[0])
		user_id = User.objects.all()
		user_id = user_id.filter(username = validated_data['username']).values('id')[0]['id']
		print(user_id)
		profile_data['user_id_id'] = user_id#.query_set['id']#['id']
		profile_data['signup_confirmation'] = True
		Profile.objects.create( **profile_data)
		#profile = ProfileSerializer(data = profile_data)
		return users

class ListGroupSerializer(serializers.ModelSerializer):
	# admin_id = serializers.SlugRelatedField(
 #        many=False, read_only=True,
 #        slug_field='id')
	class Meta:
		model = List_group
		fields = ['name', 'admin', 'is_group']

	def create(self, validated_data):
		#	print(admin)
		print(validated_data)
		user_id = User.objects.all()
		#user_id = user_id.filter(username = validated_data['admin']).values('id')[0]['id']
		#validated_data['admin'] = user_id
		lists, _ = List_group.objects.get_or_create(**validated_data)
		#print(lists)
		return lists

class JoinListGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = User_list_group
		fields = ['is_working_group', 'email_access', 'mobile_access', 'is_group', 'groups_id', 'user_id']
	
	def create(self, validated_data):
		print(validated_data)
		user_lg, _ = User_list_group.objects.get_or_create(**validated_data)
		return user_lg

class ProfileViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('gender', 'mobile_no', 'photo','about', 'location', 'user_id_id')

'''
class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'password')
	# username = serializers.CharField()
	# password = serializers.CharField()

	def validate(self, validated_data):

		data = validated_data
		print(data)
		username = data.get('username', None)
		password = data.get('password', None)
		if username and password:
			print(True)
			user = authenticate(request, username=username, password=password)
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
		else:
			mesg = "must provide both username and password"
			raise exceptions.ValidationError(mesg)


		# if user is not None:
		#     if user.is_active:
		#         login(request, user)

		#         return Response(status=status.HTTP_200_OK)
		#     else:
		#         return Response(status=status.HTTP_404_NOT_FOUND)
		# else:
		#     return Response(status=status.HTTP_404_NOT_FOUND)
'''




