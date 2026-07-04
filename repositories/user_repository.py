def create_user(user_dict, collection):
    return collection.insert_one(user_dict)


def get_user_by_username(username, collection):
    return collection.find_one(
        {"username": username}
    )