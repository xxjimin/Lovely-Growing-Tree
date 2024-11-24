from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Tree, Letter


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

    return render(request, "home.html")


# 로그인 페이지
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # 사용자 확인
        try:
            user = User.objects.get(username=username, password=password)
            request.session["user_id"] = user.user_id
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
def tree_detail(request, tree_id):
    tree = get_object_or_404(Tree, tree_id=tree_id)
    letters = Letter.objects.filter(tree=tree)

    # 편지 작성은 로그인 필요 없음
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        content = request.POST.get("content")

        if not author_name or not content:
            messages.error(request, "Author name and content cannot be empty.")
            return redirect('tree_detail', tree_id=tree_id)

        # 편지 생성
        Letter.objects.create(tree=tree, author_name=author_name, content=content)
        messages.success(request, "Letter added successfully!")
        return redirect('tree_detail', tree_id=tree_id)

    # 트리 소유자만 상세 내용 접근 가능
    logged_in_user_id = request.session.get("user_id")
    if logged_in_user_id != tree.user.user_id:
        # 트리 내용 숨기고 편지 작성 폼만 렌더링
        return render(request, "tree/tree_detail.html", {'tree': tree, 'letters': None, 'restricted': True})

    # 트리 내용과 편지 목록 보여줌
    return render(request, "tree/tree_detail.html", {'tree': tree, 'letters': letters, 'restricted': False})
