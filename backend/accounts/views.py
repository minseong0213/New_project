import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import User

# Create your views here.
def home(request):
    if request.method == 'GET':
        return JsonResponse({ "message": "Hello!" })

@method_decorator(csrf_exempt, name= 'dispatch')
def register(request):
    if request.method == 'GET':
        return JsonResponse({'message': "회원가입 완료"}, status=200)

    elif request.method == 'POST':
        params = json.loads(request.body)
        username = params.get('username')
        useremail = params.get('useremail') 
        password = params.get('password')
        re_password = params.get('re_password')
        #유효성 처리 
        res_data={}

        if password!=re_password:
            return JsonResponse({"message":"비밀번호 다름"})
        
        try:
            user = User.objects.get(useremail=useremail)
            if user:
                res_data['status'] = '0' # 기존 가입된 회원 
                return JsonResponse({"message":"가입된 회원입니다."})
        except User.DoesNotExist:
            user = User(
                username = username,
                useremail = useremail,
                password = make_password(password),
            )
            user.save()
            #session 생성
            user = User.objects.get(useremail=useremail)
            request.session['user'] = user.id
            res_data['data'] = '1'#회원가입완료 
            res_data['message'] = '회원가입완료'
            return JsonResponse(res_data)
        

def login(request):
        if request.method == "GET":
            return JsonResponse({"message":'로그인페이지'})
        
        elif request.method == "POST":
            params = json.loads(request.body)
            username = params.get('username')
            password = params.get('password')

            #유효성 처리

            res_data= {}
            if not (username and password):
                return JsonResponse({"message":"모든칸을 입력해주세요"})
            
            else:
                #기존 DB에 있는 유저 모델 가져옴
                user = User.objects.get(username = username) 
                if check_password(password, user.password):
                    request.session['user'] = user.id
                    return JsonResponse({"message":'유저맞음'})
                
                else:
                    return JsonResponse ({"message":'비밀번호 틀림'})
 
def logout(request):
    if request.method == "GET":
        if request.session.get('user') == None:
            return JsonResponse({"message":"로그인 안되어있다"})
        
        del(request.session['user'])
        return JsonResponse({"message":"성공적인 로그아웃"})
        
    




