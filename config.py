"""
loads and stores mongodb instance for project wide access
"""


import mongo_loader


techtrix_db = mongo_loader.get_cluster0()


general_fees = 20
trending_searches = ["Robotics", "ROAD RASH", "BGMI"]
update_required = False
