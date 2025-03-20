from django.core.management.base import BaseCommand
from django.db import IntegrityError
from pos.models import User


class Command(BaseCommand):
    help = 'Creates a superuser admin account'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            self.stdout.write(
                self.style.WARNING('Please change the default password immediately after login!')
            )
        
        except IntegrityError:
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {username}')) 