from fastapi import HTTPException

class TodoError(HTTPException):
    # Base class for all todo errors
    pass

class TodoNotFoundError(TodoError):
    def __init__(self, todo_id: None):
        message = "Todo not found" if todo_id is None else f"Todo with id {todo_id} not found"
        super().__init__(status_code=404, detail=message)

class TodoCreationError(TodoError):
    def __init__(self, error: str):
        super().__init__(status_code=400, detail=f"Failed to create todo: {error}")

class UserError(HTTPException):
    # Base class for all user errors
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id: None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="Password mismatch")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid password")

class AuthenticationError(UserError):
    def __init__(self, message: str = "Authentication error"):
        super().__init__(status_code=401, detail=message)

class UserAlreadyExistsError(UserError):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"User with email {email} already exists")