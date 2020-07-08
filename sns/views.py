from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message,Friend,Group,Good
from .forms import GroupCheckForm,GroupSelectForm,\
        SearchForm,FriendsForm,CreateGroupForm,PostForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def index(request):
    # publicのuserを取得
    (public_user, public_group) = get_public()

    # POST送信時の処理
    if request.method == 'POST':

        # Groupsのチェックを更新した時の処理
        if request.POST['mode'] == '__check_form__':
            # フォームの用意
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user,request.POST)
            # チェックされたGroup名をリストにまとめる
            glist = []
            for item in request.POST.getlist('groups'):
                glist.append(item)
            # Messageの取得
            messages = get_your_group_message(request.user, \
                    glist, None)

        # Groupsメニューを変更した時の処理   
        if request.POST['mode'] == '__search_form__':
            # フォームの用意
            searchform = SearchForm(request.POST)
            checkform = GroupCheckForm(request.user)
            # Groupのリストを取得
            gps = Group.objects.filter(owner=request.user)
            glist = [public_group]
            for item in gps:
                glist.append(item)
            # メッセージを取得
            messages = get_your_group_message(request.user, glist, \
                    request.POST['search'])

    # GETアクセス時の処理
    else:
        # フォームの用意
        searchform = SearchForm()
        checkform = GroupCheckForm(request.user)
        # Groupのリストを取得
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group]
        for item in gps:
            glist.append(item)
        # メッセージの取得
        messages = get_your_group_message(request.user, glist, None)

    # 共通処理
    params = {
            'login_user':request.user,
            'contents':messages,
            'check_form':checkform,
            'search_form':searchform,
        }
    return render(request, 'sns/index.html', params)

@login_required(login_url='/admin/login/')
def groups(request):
    # 自分が登録したFriendを取得
    friends = Friend.objects.filter(owner=request.user)
    
    # POST送信時の処理
    if request.method == 'POST':
        
        # Groupsメニュー選択肢の処理
        if request.POST['mode'] == '__groups_form__':
            # 選択したGroup名を取得
            sel_group = request.POST['groups']
            # Grooupを取得
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()
            # Groupに含まれるFriendを取得
            fds = Friend.objects.filter(owner=request.user) \
                .filter(group=gp)
            # FriendのUserをリストにまとめる
            vlist = []
            for item in fds:
                vlist.append(item.user.username)
            # フォームの用意
            groupsform = GroupSelectForm(request.user,request.POST)
            friendsform = FriendsForm(request.user, \
                    friends=friends, vals=vlist)
        
        # Friendsのチェック更新時の処理
        if request.POST['mode'] == '__friends_form__':
            # 選択したGroupの取得
            sel_group = request.POST['group']
            group_obj = Group.objects.filter(title=sel_group).first()
            # チェックしたFriendsを取得
            sel_fds = request.POST.getlist('friends')
            # FriendsのUserを取得
            sel_users = User.objects.filter(username__in=sel_fds)
            # Userのリストに含まれるユーザーが登録したFriendを取得
            fds = Friend.objects.filter(owner=request.user) \
                    .filter(user__in=sel_users)
            # すべてのFriendにGroupを設定し保存する
            vlist = []
            for item in fds:
                item.group = group_obj
                item.save()
                vlist.append(item.user.username)
            # メッセージを設定
            messages.success(request, ' チェックされたFriendを' + \
                    sel_group + 'に登録しました。')
            # フォームの用意
            groupsform = GroupSelectForm(request.user, \
                    {'groups':sel_group})
            friendsform = FriendsForm(request.user, \
                    friends=friends, vals=vlist)
    
    # GETアクセス時の処理  
    else:
        # フォームの用意
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, friends=friends, \
                vals=[])
        sel_group = '-'
    
    # 共通処理
    createform = CreateGroupForm()
    params = {
            'login_user':request.user,
            'groups_form':groupsform,
            'friends_form':friendsform,
            'create_form':createform,
            'group':sel_group,
        }
    return render(request, 'sns/groups.html', params)

@login_required(login_url='/admin/login/')
def add(request):
    # 追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    # Userが本人だった場合の処理
    if add_user == request.user:
        messages.info(request, "自分自身をFriendに追加することは\
                できません。")
        return redirect(to='/sns')
    # publicの取得
    (public_user, public_group) = get_public()
    # add_userのFriendの数を調べる
    frd_num = Friend.objects.filter(owner=request.user) \
            .filter(user=add_user).count()
    # ゼロより大きければ既に登録済み
    if frd_num > 0:
        messages.info(request, add_user.username + \
                ' は既に追加されています。')
        return redirect(to='/sns')
    
    # ここからFriendの登録処理
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    frd.group = public_group
    frd.save()
    # メッセージを設定
    messages.success(request, add_user.username + ' を追加しました！\
        groupページに移動して、追加したFriendをメンバーに設定して下さい。')
    return redirect(to='/sns')

@login_required(login_url='/admin/login/')
def creategroup(request):
    # Groupを作り、Userとtitleを設定して保存する
    gp = Group()
    gp.owner = request.user
    gp.title = request.POST['group_name']
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/sns/groups')

