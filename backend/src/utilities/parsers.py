import datetime

def userParser(user_list):
    return {
        "id": user_list[0],
        "display_name": user_list[1],
        "email": user_list[2],
        "height": user_list[4],
        "weight": user_list[5],
    }

def diet_goal_parser(diet_goal):
    return {
        "id": diet_goal[0],
        "start_date": datetime.datetime.strftime(diet_goal[2],'%m/%d/%Y'),
        "end_date": datetime.datetime.strftime(diet_goal[3],'%m/%d/%Y'),
        "active": diet_goal[4],
        "protein": diet_goal[5],
        "fats": diet_goal[6],
        "carbs": diet_goal[7],

    }


def tracked_item_parser(item):
    return {
        "entry_id":item[0],
        "item_id":item[1],
        "item_name":item[2],
        "item_type":item[3],
        "consumed_time": datetime.datetime.strftime(item[4],'%m/%d/%Y %H:%S'),
        "amount": item[5],
        "item_category": item[6],
        "protein": item[7],
        "carbs": item[8],
        "fats": item[9]
    }

