from . import views
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings 
from django.conf.urls.static import static
#from .views import sendLink, home_view, sendLinkPage, sent_link, accountlink, insert_data#, signup_view, activation_sent_view, activate
#from .apiViews import UserCreate, LoginView, HelloView

urlpatterns = [
	# path('home/', home_view, name='home'),
	# # path('signup/', signup_view, name="signup"),
 # #    path('sent/', activation_sent_view, name="activation_sent"),
 # #    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
 # #    path('profile/', ProfileView, name='profile'),
 # #    path('updateProfile/', updateProfileView, name='updateProfile'),
 # #    path('success/', successView, name='success'),
 # 	path('sendlinkpage', sendLinkPage, name='sendlinkpage' ),
 #    path('sendlink/', sendLink, name='sendlink'),
 #    path('sentlink', sent_link, name = 'sentlink'),
 #    path('accountlink', accountlink, name='accountlink'),
 #    path('insert_data', insert_data, name='insert_data'),
 #    path('users/', UserCreate.as_view(), name='user_create'),
 #    path("login/", LoginView.as_view(), name="login"),
 	path('account/', include('django.contrib.auth.urls')),
    path("hello/", views.HelloView.as_view(), name="hello"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('addlistgroup/', views.ListGroupView.as_view(), name='addlistgroup'),
    path('home/', views.ListGroups.as_view(), name = 'home'),
    path('updateAccount/', views.UpdateProfile.as_view(), name='update'),
    path('joinlistgroup/', views.SelectListGroupsView.as_view(), name='joinlistgroup'),
    path('myteams/', views.ShowMyGroupsList.as_view(), name='myteams'),
    path('signupmailer/',views.SendLinkView.as_view(), name='signupmailer'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #url(r'^api-token-auth/', obtain_jwt_token),
    #url(r'^login/', obtain_jwt_token),
    #path('password_reset/', view.PassordReset.as_view(), name = 'password_reset'),
]


if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)