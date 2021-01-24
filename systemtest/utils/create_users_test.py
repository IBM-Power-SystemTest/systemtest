from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group
from systemtest.users.models import Job, Departament

User = get_user_model()

users_list = (
    {
        'username': 'alanv',
        'first_name': 'Alan',
        'last_name': 'Vazquez',
        'is_superuser': True,
        'is_staff': True
    },
    {
        'username': 'TA',
        'first_name': 'TA',
        'department': Departament.objects.get(pk=1),
        'job': Job.objects.get(pk=1)
    },
    {
        'username': 'IPIC',
        'first_name': 'IPIC',
        'department': Departament.objects.get(pk=2),
        'job': Job.objects.get(pk=6)
    },
    {
        'username': 'IPIC NCM',
        'first_name': 'IPIC NCM',
        'department': Departament.objects.get(pk=2),
        'job': Job.objects.get(pk=7)
    }
)

for user_data in users_list:
    user_data['password'] = user_data.get('password', 'passw0rd')
    user_data['last_name'] = user_data.get('first_name', 'Test')
    user_data['last_name'] = user_data.get('last_name', 'Test')
    user_data['email'] = user_data.get('email', 'admin@test.com')

    User.objects.create_user(**user_data)

