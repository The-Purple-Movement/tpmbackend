from app.repositories.join_repo import create_join_request

def submit_join(db, data):
    return create_join_request(db, data)