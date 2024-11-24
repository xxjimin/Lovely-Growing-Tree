from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Tree, Letter, Ornament


# 홈 페이지 - 회원가입 및 검색
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Tree

# 홈 페이지 - 회원가입 및 검색
def home(request):
    if request.method == "POST":
        if request.POST.get('type') == 'register':
            username = request.POST["username"]
            password = request.POST["password"]

            # 사용자 중복 확인
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('home')

            # 사용자 등록 및 세션에 사용자 ID 저장
            user = User.objects.create(username=username, password=password)
            request.session["user_id"] = user.user_id
            messages.success(request, "User registered successfully!")
            return redirect('create_tree', user_id=user.user_id)

        elif request.POST.get('type') == 'search':
            search_username = request.POST["search_username"]
            try:
                # 사용자 및 트리 조회
                user = User.objects.get(username=search_username)
                tree = Tree.objects.get(user=user)
                return redirect('tree_detail', tree_id=tree.tree_id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('home')
            except Tree.DoesNotExist:
                messages.error(request, "The user does not have a tree.")
                return redirect('home')

    # 로그인된 사용자 정보 처리
    if request.session.get("user_id"):
        user = User.objects.get(user_id=request.session.get("user_id"))
        # 트리가 있다면 트리 ID를 세션에 저장
        try:
            tree = Tree.objects.get(user=user)
            request.session["tree_id"] = tree.tree_id
        except Tree.DoesNotExist:
            pass

    return render(request, "home.html")


# 로그인 페이지
# 로그인 페이지
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # 사용자 확인
        try:
            user = User.objects.get(username=username, password=password)
            request.session["user_id"] = user.user_id
            request.session["username"] = user.username  # 사용자 이름을 세션에 저장
            messages.success(request, "Login successful!")

            # 로그인 후 해당 사용자의 트리로 리다이렉트
            user_tree = Tree.objects.get(user=user)
            return redirect('tree_detail', tree_id=user_tree.tree_id)

        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
        except Tree.DoesNotExist:
            messages.error(request, "User does not have a tree.")
            return redirect('create_tree', user_id=user.user_id)

    return render(request, "login.html")





# 로그아웃
def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# 회원가입 페이지
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create(username=username, password=password)

        # 세션에 사용자 ID 저장
        request.session["user_id"] = user.user_id

        messages.success(request, "User registered successfully!")
        return redirect('create_tree', user_id=user.user_id)

    return render(request, "register.html")


# 트리 목록 보기
def tree_list(request):
    if not request.session.get("user_id"):
        messages.error(request, "You must be logged in to view trees.")
        return redirect('login')

    trees = Tree.objects.all()
    return render(request, 'tree/tree_list.html', {'trees': trees})


# 트리 생성 페이지
def create_tree(request, user_id):
    if request.method == "POST":
        tree_name = request.POST["tree_name"]
        user = User.objects.get(user_id=user_id)

        # 트리 생성
        tree = Tree.objects.create(tree_name=tree_name, user=user)
        messages.success(request, "Tree created successfully!")

        # 생성한 트리 상세 페이지로 리다이렉트
        return redirect('tree_detail', tree_id=tree.tree_id)

    return render(request, "create_tree.html")



# 트리 상세 보기 및 편지 작성
import random

from django.conf import settings
from django.templatetags.static import static

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Tree, Letter
from django.conf import settings
from django.templatetags.static import static
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
import random
from .models import Tree, Letter, Ornament

def tree_detail(request, tree_id):
    # 트리 객체를 가져옵니다.
    tree = get_object_or_404(Tree, tree_id=tree_id)
    letters = Letter.objects.filter(tree=tree)

    # 트리 이미지 URL을 media 경로로 설정 (정적 파일 처리)
    tree_image_url = settings.STATIC_URL + 'tree_image.png'   # static 폴더에 위치한 이미지 경로

    # POST 요청일 때 편지 작성 및 랜덤 좌표 추가 처리
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        content = request.POST.get("content")

        if not author_name or not content:
            messages.error(request, "Author name and content cannot be empty.")
            return redirect('tree_detail', tree_id=tree_id)

        # 편지 생성
        letter = Letter.objects.create(tree=tree, author_name=author_name, content=content)

                
        min_x = 150
        max_x = 350
        min_y = 150
        max_y = 350

        # 초록색 영역 내에서 랜덤 좌표 생성
        random_x = random.uniform(min_x, max_x)
        random_y = random.uniform(min_y, max_y)

        # 장식 생성 (편지에 해당하는 좌표를 가진 Ornament 객체)
        Ornament.objects.create(tree=tree, letter=letter, position_x=random_x, position_y=random_y)

        messages.success(request, "Letter added successfully!")
        return redirect('tree_detail', tree_id=tree_id)

    # 트리 소유자 확인
    logged_in_user_id = request.session.get("user_id")
    is_owner = logged_in_user_id == tree.user.user_id

    # 트리에 연결된 모든 Ornament를 가져옵니다 (편지 마커 위치)
    ornaments = Ornament.objects.filter(tree=tree)

    # 편지를 볼 수 있는 권한 체크 (트리 소유자가 아닌 경우 편지 목록을 숨김)
    return render(request, "tree/tree_detail.html", {
        'tree': tree,
        'letters': letters if is_owner else None,
        'restricted': not is_owner,
        'tree_image_url': tree_image_url,
        'ornaments': ornaments,  # 장식 정보 (편지 마커 위치) 추가
    })
    
    # 로그아웃
def logout(request):
    request.session.flush()  # 세션 삭제
    messages.success(request, "Logged out successfully!")
    return redirect('home')


