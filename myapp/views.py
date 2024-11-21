from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Trees, Letters, Ornaments

# 사용자 생성 및 로그인 뷰
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Users 테이블에 사용자 추가
            user_instance = Users.objects.create(
                user_id=user.id,
                username=user.username,
                created_at=user.date_joined,
            )
            
            # Users가 등록된 후, 자동으로 트리 생성
            tree = Trees.objects.create(
                tree_name="Default Tree",  # 기본 트리 이름 설정 (원하는대로 변경 가능)
                user_id=user.id  # 해당 사용자에 대한 트리 생성
            )
            
            return redirect('user_tree')  # 트리 페이지로 리디렉션
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 트리와 편지 보기
def user_tree(request):
    if not request.user.is_authenticated:
        return redirect('login')  # 로그인하지 않은 경우 로그인 페이지로 리디렉션

    trees = Trees.objects.filter(user__user_id=request.user.id)
    ornaments = Ornaments.objects.filter(tree__user__user_id=request.user.id)
    return render(request, 'user_tree.html', {'trees': trees, 'ornaments': ornaments})

# 편지 추가
def add_letter(request, tree_id):
    tree = Trees.objects.get(id=tree_id)
    if request.method == 'POST':
        content = request.POST['content']
        letter = Letters.objects.create(tree=tree, content=content, author_name=request.user.username)
        # Ornament 생성 (임의로 위치를 정함)
        Ornaments.objects.create(tree=tree, position_x=1.0, position_y=1.0, letter=letter)
        return redirect('user_tree')
    return render(request, 'add_letter.html', {'tree': tree})
