from typing import List

class User:
    def __init__(self, username: str, email: str):
        """
        TODO:
        - Store username
        - Store email
        """
        self.username = username
        self.email = email
    def get_display_name(self) -> str:
        """
        TODO:
        Return:
        "User: <username>"
        """
        return f"User: {self.username}"
    def can_access(self, resource: str) -> bool:
        """
        TODO:
        Regular users cannot access any resources.
        """
        return False

class AdminUser(User):
    def __init__(self, username: str, email: str, permissions: List[str]):
        """
        TODO:
        - Call parent constructor
        - Store permissions
        """
        super().__init__(username,email)
        self.permissions = permissions
    def get_display_name(self) -> str:
        """
        TODO:
        Return:
        "Admin: <username> (permissions: <number_of_permissions>)"
        """
        return f"Admin: {self.username} (permissions: {len(self.permissions)})"
    def can_access(self, resource: str) -> bool:
        """
        TODO:
        Admin can access a resource if it's in permissions list
        """
        if resource in self.permissions:
            return True
        else:
            return False

if __name__ == "__main__":
    user = User("dana", "dana@example.com")
    admin = AdminUser("karin", "karin@example.com", ["reports", "settings"])
    print(user.get_display_name())
    print(admin.get_display_name())
    print(user.can_access("reports"))   # Expected: False
    print(admin.can_access("reports"))  # Expected: True
    print(admin.can_access("billing"))  # Expected: False