import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'auric.settings'
django.setup()

from django.contrib.auth.models import User

# Update existing admin user
try:
    u = User.objects.get(username='admin')
    u.username = 'arjunaju'
    u.set_password('Njr1011@psg')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Updated: username=arjunaju, password set.')
except User.DoesNotExist:
    # Create fresh
    u = User.objects.create_superuser('arjunaju', 'admin@auric.com', 'Njr1011@psg')
