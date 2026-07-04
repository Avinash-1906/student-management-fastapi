from bson import ObjectId


def create_student(student_dict, collection):
    return collection.insert_one(student_dict)


def get_all_students(query, skip, limit, collection):
    return list(
        collection.find(query).skip(skip).limit(limit)
    )


def get_student(student_id, collection):
    return collection.find_one(
        {"_id": ObjectId(student_id)}
    )


def update_student(student_id, student_dict, collection):
    return collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student_dict}
    )


def delete_student(student_id, collection):
    return collection.delete_one(
        {"_id": ObjectId(student_id)}
    )