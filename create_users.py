from django.contrib.auth.models import User

def create_test_users():
    users = [
        {"username": "centro", "password": "diegofuentes"},
        {"username": "occidente", "password": "rolandocarpio"},
        {"username": "oriente", "password": "jhanniozardan"},
        {"username": "supervisor", "password": "alejandraparada"},
    ]

    for user_info in users:
        user, created = User.objects.get_or_create(username=user_info["username"])
        if created:
            user.set_password(user_info["password"])
            user.save()
            print(f"Usuario {user_info['username']} creado.")
        else:
            print(f"Usuario {user_info['username']} ya existe.")
