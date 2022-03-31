"""
loads and stores mongodb instance for project wide access
"""


import mongo_loader


techtrix_db = mongo_loader.get_cluster0()
