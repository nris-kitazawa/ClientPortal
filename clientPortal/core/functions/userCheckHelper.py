from django.contrib.auth.models import User

def is_admin_user(user_or_username):
    """
    ユーザーインスタンスまたはユーザー名でゲストグループ所属を判定
    """
    if isinstance(user_or_username, User):
        return user_or_username.groups.filter(name="admin").exists()
    elif isinstance(user_or_username, str):
        return User.objects.filter(username=user_or_username, groups__name="admin").exists()
    else:
        return False
    
def is_nris_user(user_or_username):
    """
    ユーザーインスタンスまたはユーザー名でゲストグループ所属を判定
    """
    if isinstance(user_or_username, User):
        return user_or_username.groups.filter(name="NRIS").exists()
    elif isinstance(user_or_username, str):
        return User.objects.filter(username=user_or_username, groups__name="NRIS").exists()
    else:
        return False
    
def is_guest_user(user_or_username):
    """
    ユーザーインスタンスまたはユーザー名でゲストグループ所属を判定
    """
    if isinstance(user_or_username, User):
        return user_or_username.groups.filter(name="guest").exists()
    elif isinstance(user_or_username, str):
        return User.objects.filter(username=user_or_username, groups__name="guest").exists()
    else:
        return False