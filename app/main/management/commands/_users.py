from django.contrib.auth.models import User, Group, Permission


def create_users():
    """
    * create admin accaount and moderators
    * create 'MODERATOR' group
    * add 'CAN MODERATE POST' permission to this group
    * add created users to this group
    """
    User.objects.create_superuser("admin", "bluszczowa4c@gmail.com", 'doZmiany')
    piotr = User.objects.create_user("Piotr", "pjkalista@gmail.com", 'doZmiany', is_staff=True)
    tymon = User.objects.create_user("Tymon", "tymonkalista@gmail.com", 'doZmiany', is_staff=True)
    kacper = User.objects.create_user("Kacper", "klinger1939@gmail.com", 'doZmiany', is_staff=True)
    panbarnaba = User.objects.create_user("Pan Barnaba", "kontakt@panbarnaba.pl", 'doZmiany', is_staff=True)

    moderate_group = Group.objects.create(name='moderator')
    proj_add_perm = Permission.objects.get(name='Can moderate posts')
    moderate_group.permissions.add(proj_add_perm)

    moderate_group.user_set.add(piotr)
    moderate_group.user_set.add(tymon)
    moderate_group.user_set.add(kacper)
