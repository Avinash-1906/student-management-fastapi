from database import student_collection, user_collection, idempotency_collection

def get_student_collection():
    return student_collection

def get_user_collection():
    return user_collection

def get_idempotency_collection():
    return idempotency_collection

