from app.repositories.login_repository.chat_repository import get_chats_from_class_by_db,store_chats_in_class_wise_into_db
    
def get_chats_from_class(class_id):
    try:
        return get_chats_from_class_by_db(class_id)
    except Exception as e:
        print(f" Error in get Old chats from class room : {e}")
        return []
    
def store_chats_in_class_wise(data,timestamp):
    try:
        return store_chats_in_class_wise_into_db(data,timestamp)
    except Exception as e:
        print(f" Error in Store messages in db : {e}")
        return []