from django.db import models
from django.contrib.auth.models import AbstractUser
from clubs.models import Club

class RoleUser(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 0, "Admin"
        BOARD_MEMBER = 1, "Board Member"
        E_BOARD = 2, "E-Board"
        VIEWER = 3, "Viewer"

    username = models.CharField(max_length=50, unique=True)

    role = models.IntegerField(choices=Roles, default=3)

    club = models.ForeignKey(Club, on_delete=models.SET_DEFAULT, related_name="users", null=True, default=None)

    email = models.EmailField(unique=True, max_length=100, default=None)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    def has_admin_role(self):
        if self.role == RoleUser.Roles.ADMIN:
            return True
        return False
    
    def has_board_role(self):
        if self.role == RoleUser.Roles.BOARD_MEMBER or self.role == RoleUser.Roles.ADMIN:
            return True
        return False
    
    def has_e_board_role(self):
        if self.role == RoleUser.Roles.E_BOARD or self.role == RoleUser.Roles.ADMIN:
            return True
        return False

    def __str__(self) -> str:
        return f'{self.username} ({self.get_role_display()})'