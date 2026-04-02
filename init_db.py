"""
数据库初始化脚本
运行此脚本创建数据库并添加初始数据
"""
from models import db, PointItem, Reward

def seed_initial_data():
    """仅在无数据时写入初始积分项目和奖励，返回是否写入成功。"""
    if PointItem.query.first() is not None:
        return False

    # 添加初始积分项目（正向加分 + 扣分）
    initial_items = [
        # 加分项目
        PointItem(name="7:30起床", points=1, description="早起加分", enabled=True),
        PointItem(name="00:20之前睡觉", points=2, description="按时早睡", enabled=True),
        PointItem(name="连续7天早睡早起", points=10, description="持续作息达标", enabled=True),
        PointItem(name="按时吃早餐", points=3, description="早餐打卡", enabled=True),
        PointItem(name="拥有好心情、好心态", points=1, description="保持积极状态", enabled=True),
        PointItem(name="三餐按时且规律", points=1, description="规律饮食", enabled=True),
        PointItem(name="每天发一张自拍照/ootd", points=1, description="日常打卡", enabled=True),
        PointItem(name="每天晚上打视频", points=1, description="保持联系", enabled=True),
        PointItem(name="每天去健身房", points=2, description="坚持锻炼", enabled=True),

        # 扣分项目
        PointItem(name="撒谎", points=-5, description="诚信约束", enabled=True),
        PointItem(name="超过00:20睡觉", points=-3, description="轻度熬夜", enabled=True),
        PointItem(name="超过01:00睡觉", points=-10, description="重度熬夜", enabled=True),
        PointItem(name="来大姨妈期间吃辣的冰的", points=-3, description="生理期饮食不当", enabled=True),
        PointItem(name="平时吃辣的冰的", points=-1, description="饮食不当", enabled=True),
        PointItem(name="吃辣的", points=-1, description="饮食约束", enabled=True),
    ]

    for item in initial_items:
        db.session.add(item)

    # 添加初始奖励
    initial_rewards = [
        Reward(name="小零食盲盒", cost_points=80, description="随机零食惊喜", enabled=True),
        Reward(name="丰盛美食一顿", cost_points=90, description="丰盛美食奖励", enabled=True),
        Reward(name="奶茶一杯", cost_points=60, description="喜欢的奶茶店任选", enabled=True),
        Reward(name="小蛋糕一个", cost_points=70, description="甜品奖励", enabled=True),
        Reward(name="冰棍一个", cost_points=6, description="清凉小奖励", enabled=True),
        Reward(name="和小杨见一面", cost_points=999, description="最珍贵的奖励", enabled=True),
        Reward(name="和好如初卡", cost_points=200, description="消除误会的魔法卡", enabled=True),
        Reward(name="随心所欲卡", cost_points=300, description="想做什么都可以", enabled=True),
        Reward(name="盲盒小玩偶", cost_points=200, description="可爱的盲盒玩偶", enabled=True),
    ]

    for reward in initial_rewards:
        db.session.add(reward)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True


def init_database(app=None):
    """初始化数据库（可在脚本中调用，也可被应用启动复用）。"""
    if app is None:
        from app import app as flask_app
    else:
        flask_app = app

    with flask_app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表创建成功")

        seeded = seed_initial_data()
        if seeded:
            print("✓ 初始数据写入成功")
        else:
            print("! 数据库已包含数据，跳过初始化")

        print("\n✓ 数据库初始化完成！")
        print("\n现在可以运行 python app.py 启动应用了")

if __name__ == '__main__':
    init_database()
