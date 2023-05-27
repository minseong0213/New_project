import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User

# Create your views here.

@method_decorator(csrf_exempt, name= 'dispatch')
def register(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        username = params.get('username')
        useremail = params.get('useremail') 
        password = params.get('password')
        re_password = params.get('re_password')
        #유효성 처리 
        res_data={}

        if password!=re_password:
            return JsonResponse({"message":"비밀번호가 다릅니다."},status=400)
        
        try:
            user = User.objects.get(useremail=useremail)
            if user:
                res_data['status'] = '0' # 기존 가입된 회원 
                return JsonResponse({"message":"가입된 회원입니다."},status=200)
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
            res_data['message'] = '회원가입 완료'
            return JsonResponse({"message" : res_data},status = 200)
        

def login(request):        
        if request.method == "POST":
            params = json.loads(request.body)
            username = params.get('username')
            password = params.get('password')

            if not (username and password):
                return JsonResponse({"message":"유저이름과 비밀번호를 입력해주세요."},status=200)
            
            else:
                #기존 DB에 있는 유저 모델 가져옴
                user = User.objects.get(username = username) 
                if check_password(password, user.password):
                    request.session['user'] = user.id
                    return JsonResponse({"message":'유저가 맞습니다.'},status=200)
                
                else:
                    return JsonResponse ({"message":'비밀번호가 틀립니다.'},status=400)
 
def logout(request):
    if request.method == "GET":
        if request.session.get('user') == None:
            return JsonResponse({"message":"로그인이 안되었습니다."},status=400)
        
        del(request.session['user'])
        return JsonResponse({"message":"로그아웃이 되었습니다."},status=200)
    
def findpassword(request):
    if request.method == "POST":
        params = json.loads(request.body)
        username = params.get('username')
        password = User.objects.get(username=username).password
        return JsonResponse({"message" : "비밀번호를 찾았습니다.", "password": password},status=200)
    

def changepassword(request):
    if request.method == "POST":
        params = json.loads(request.body)
        username = params.get("username")
        password = params.get("password")
        user = User.objects.get(username = username)

        if check_password(password, user.password): #지금 내 패스워드가 맞는지 확인
            new_password = params.get('new_password')
            password_confirm = params.get('re_password')

            if check_password(new_password, user.password): #지금 내 패스워드와 변경할 패스워드가 같은지 확인
                return JsonResponse({"message": "현재 비밀번호와 동일합니다."},status=200)

            if new_password == password_confirm:
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({"message": "비밀번호가 변경되었습니다."},status=200)
            else:
                return JsonResponse({"message": "변경하실 비밀번호가 일치하지 않습니다."},status=400)
        else:
            return JsonResponse({"message": "현재 비밀번호가 틀립니다."} ,status=400)


def findid(request):
    if request.method == "POST":
        params = json.loads(request.body)
        useremail = params.get('useremail') 
        username = User.objects.get(useremail=useremail).username
        return JsonResponse({"message" : "유저아이디를 찾았습니다.", "username": username},status=200)
