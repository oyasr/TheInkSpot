
def check_password_strength(password):
    if not (password.isalnum() and any(c.isupper() for c in password) and any(c.isdigit() for c in password)):
        return False
    else:
        return True