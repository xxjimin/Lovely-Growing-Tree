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


# 트리 목록 보기
def tree_list(request):
    trees = Tree.objects.all()
    return render(request, 'tree/tree_list.html', {'trees': trees})


# 트리 생성 페이지
def create_tree(request, user_id):
    if request.method == "POST":
        tree_name = request.POST["tree_name"]
        user = User.objects.get(user_id=user_id)
        
        # 트리 생성
        Tree.objects.create(tree_name=tree_name, user=user)
        messages.success(request, "Tree created successfully!")
        return redirect("tree_list")
    
    return render(request, "create_tree.html")


# 트리 상세 보기 및 편지 작성
def tree_detail(request, tree_id):
    tree = Tree.objects.get(tree_id=tree_id)
    letters = Letter.objects.filter(tree=tree)

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

    return render(request, "tree/tree_detail.html", {'tree': tree, 'letters': letters})


# 편지 작성 페이지
def write_letter(request, tree_id):
    tree = Tree.objects.get(tree_id=tree_id)
    
    if request.method == "POST":
        content = request.POST["content"]
        author_name = request.POST["author_name"]  # author_name을 폼에서 받기
        
        if not content or not author_name:
            messages.error(request, "Content and author name cannot be empty.")
            return redirect('write_letter', tree_id=tree_id)
        
        # 편지 작성
        Letter.objects.create(content=content, author_name=author_name, tree=tree)
        messages.success(request, "편지가 성공적으로 작성되었습니다.")
        return redirect("tree_detail", tree_id=tree_id)

    return render(request, "write_letter.html", {"tree": tree})


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
