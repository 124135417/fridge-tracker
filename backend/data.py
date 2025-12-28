from datetime import date, timedelta

TODAY = date.today()

items = [
    {"name": "鸡蛋", "date_in": TODAY - timedelta(days=21)},
    {"name": "牛奶", "date_in": TODAY - timedelta(days=14)},
    {"name": "牛排", "date_in": TODAY - timedelta(days=30)},
    {"name": "酸奶", "date_in": TODAY - timedelta(days=10)},
    {"name": "胡萝卜", "date_in": TODAY - timedelta(days=18)},
    {"name": "西兰花", "date_in": TODAY - timedelta(days=7)},
    {"name": "鸡胸肉", "date_in": TODAY - timedelta(days=25)},
    {"name": "培根", "date_in": TODAY - timedelta(days=40)},
    {"name": "豆腐", "date_in": TODAY - timedelta(days=12)},
    {"name": "蘑菇", "date_in": TODAY - timedelta(days=9)},
    {"name": "冻虾", "date_in": TODAY - timedelta(days=60)},
]
