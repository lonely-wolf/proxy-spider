from Config import MongoClient,pexels_data

def save_data(photo):
    pexels_data.update_one(
        {'photo_id':photo['id']},
        {'$set':photo},
        upsert = True
    )