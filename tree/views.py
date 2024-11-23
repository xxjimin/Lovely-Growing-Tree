from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Tree
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # User 모델에 사용자 등록
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
        user = User.objects.create(username=username, password=password)
        # 트리 생성 페이지로 리다이렉트
        return redirect('create_tree', user_id=user.user_id)
    
    return render(request, "register.html")
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Tree
from django.contrib import messages

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Tree

# views.py

def home(request):
    if request.method == "POST":
        if request.POST.get('type') == 'register':
            username = request.POST["username"]
            password = request.POST["password"]
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('home')
            
            user = User.objects.create(username=username, password=password)
            messages.success(request, "User registered successfully!")
            return redirect('create_tree', user_id=user.user_id)

        elif request.POST.get('type') == 'search':
            search_username = request.POST["search_username"]
            try:
                user = User.objects.get(username=search_username)
                tree = Tree.objects.get(user=user)  # User 객체로 Tree를 조회
                return redirect('tree_detail', tree_id=tree.tree_id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('home')
            except Tree.DoesNotExist:
                messages.error(request, "The user does not have a tree.")
                return redirect('home')

    return render(request, "home.html")



# Other views (register, create_tree) remain the same

from django.shortcuts import render, redirect
from .models import User, Tree
from django.contrib import messages

def tree_list(request):
    # This is just an example; you can modify it as needed
    trees = Tree.objects.all()
    return render(request, 'tree/tree_list.html', {'trees': trees})

# Other views (register, create_tree) remain the same

def create_tree(request, user_id):
    if request.method == "POST":
        tree_name = request.POST["tree_name"]
        user = User.objects.get(user_id=user_id)
        
        # Tree 모델에 트리 생성
        Tree.objects.create(tree_name=tree_name, user=user)
        messages.success(request, "Tree created successfully!")
        return redirect("tree_list")
    
    return render(request, "create_tree.html")

# views.py

from django.shortcuts import render, redirect
from .models import User, Tree, Letter
from django.contrib import messages

def write_letter(request, tree_id):
    tree = Tree.objects.get(tree_id=tree_id)
    if request.method == "POST":
        content = request.POST["content"]
        author = User.objects.get(user_id=request.session["user_id"])  # 세션에서 로그인된 사용자 가져오기
        
        # 편지 작성
        Letter.objects.create(content=content, author=author, tree=tree)
        messages.success(request, "편지가 성공적으로 작성되었습니다.")
        return redirect("tree_detail", tree_id=tree_id)  # 작성 후 트리 상세 페이지로 리다이렉트

    return render(request, "write_letter.html", {"tree": tree})

# views.py

from .models import User, Tree, Letter  # Letter 모델도 임포트

def tree_detail(request, tree_id):
    tree = Tree.objects.get(tree_id=tree_id)
    letters = Letter.objects.filter(tree=tree)

    if request.method == "POST":
        author = request.POST.get("author")
        content = request.POST.get("content")

        if not author or not content:
            messages.error(request, "Author and content cannot be empty.")
            return redirect('tree_detail', tree_id=tree_id)

        # Letter 생성
        Letter.objects.create(tree=tree, author_name=author_name, content=content)

        messages.success(request, "Letter added successfully!")
        return redirect('tree_detail', tree_id=tree_id)

    return render(request, "tree/tree_detail.html", {'tree': tree, 'letters': letters})


# register 뷰에서 로그인 처리
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

        return redirect('create_tree', user_id=user.user_id)

    return render(request, "register.html")


