from app.repositories.feedback_repo import create_feedback

def submit_feedback(db, data):
    return create_feedback(db, data)