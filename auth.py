from datetime import datetime

# Data file to store user information
DATA_FILE = 'data.txt'

def user_exists(email):
    """Check if a user with the given email exists"""
    users = load_users()
    return any(user['email'] == email for user in users)

def register_user(email, password):
    """Register a new user"""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, 'a') as f:
        f.write(f"{email},{password},{created_at}\n")

def authenticate(email, password):
    """Authenticate a user with email and password"""
    users = load_users()
    for user in users:
        if user['email'] == email and user['password'] == password:
            return True
    return False

def get_user(email):
    """Get a user by email"""
    users = load_users()
    for user in users:
        if user['email'] == email:
            return user
    return None

def load_users():
    """Load all users from the data file"""
    users = []
    try:
        with open(DATA_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    email, password, created_at = line.strip().split(',')
                    users.append({
                        'email': email,
                        'password': password,
                        'created_at': created_at
                    })
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        pass
    return users 