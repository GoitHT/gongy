"""
数据库初始化脚本
运行此脚本创建数据库并添加初始数据
"""
from app import app
from models import db, PointItem, Reward

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表创建成功")
        
        # 检查是否已有数据
        if PointItem.query.first() is not None:
            print("! 数据库已包含数据，跳过初始化")
            return
        
        # 添加初始积分项目（正向加分）
        initial_items = [
            # 作息类
            PointItem(name="8:30起床", points=1, description="早起的鸟儿有虫吃", enabled=True),
            PointItem(name="00:20之前睡觉", points=2, description="早睡早起身体好", enabled=True),
            
            # 学习类
            PointItem(name="学习满4小时", points=1, description="学习时长达标", enabled=True),
            PointItem(name="学习满5小时", points=3, description="学习很努力", enabled=True),
            PointItem(name="学习满6小时", points=5, description="学习非常努力", enabled=True),
            PointItem(name="学习大于7小时", points=10, description="学习超级努力！", enabled=True),
            
            # 正确率类
            PointItem(name="言语正确率70以上", points=2, description="言语理解题做得好", enabled=True),
            PointItem(name="资料正确率80以上", points=2, description="资料分析题做得好", enabled=True),
            PointItem(name="数量正确率60以上", points=2, description="数量关系题做得好", enabled=True),
            PointItem(name="判断推理正确率70以上", points=2, description="判断推理题做得好", enabled=True),
            PointItem(name="政治理论正确率60以上", points=2, description="政治理论题做得好", enabled=True),
            PointItem(name="常识正确率60以上", points=2, description="常识题做得好", enabled=True),
            
            # 任务类
            PointItem(name="做一篇申论", points=2, description="申论练习完成", enabled=True),
            PointItem(name="拥有好心情、好心态", points=1, description="保持积极心态", enabled=True),
            PointItem(name="复习错题", points=2, description="查漏补缺", enabled=True),
            PointItem(name="两餐按时且规律", points=1, description="按时吃饭身体好", enabled=True),
            
            # 娱乐控制类
            PointItem(name="抖音使用三小时内", points=5, description="控制娱乐时间", enabled=True),
            PointItem(name="抖音使用五小时内", points=3, description="娱乐时间较长", enabled=True),
            PointItem(name="小红书使用两小时内", points=2, description="控制刷手机时间", enabled=True),
            PointItem(name="小红书使用三小时内", points=1, description="手机使用时间较长", enabled=True),
            
            # 模拟考试类
            PointItem(name="模拟套卷65分以上", points=3, description="考试成绩不错", enabled=True),
            PointItem(name="模拟套卷70分以上", points=7, description="考试成绩很好", enabled=True),
            PointItem(name="模拟套卷75分以上", points=12, description="考试成绩优秀！", enabled=True),
            
            # 日常打卡类
            PointItem(name="每天发一张自拍照/ootd", points=1, description="分享日常生活", enabled=True),
            PointItem(name="每天晚上打视频", points=1, description="保持联系", enabled=True),
            PointItem(name="起床学习打卡", points=1, description="学习打卡", enabled=True),
            
            # 健身类
            PointItem(name="每天去健身房", points=2, description="坚持运动", enabled=True),
            PointItem(name="连续一周不间断去健身房", points=5, description="运动习惯养成", enabled=True),
            PointItem(name="每周瘦5斤", points=3, description="减重效果显著", enabled=True),
            PointItem(name="每周瘦3斤", points=1, description="减重有进展", enabled=True),
            
            # 扣分项目（负分）
            PointItem(name="撒谎", points=-5, description="诚实很重要", enabled=True),
            PointItem(name="学习少于四个小时", points=-11, description="学习时长不够", enabled=True),
            PointItem(name="学习少于三个小时", points=-13, description="学习时长严重不足", enabled=True),
            PointItem(name="学习少于两个小时", points=-15, description="学习时长太少", enabled=True),
            PointItem(name="连续请假超过3天", points=-10, description="请假太多", enabled=True),
            PointItem(name="连续请假超过2天", points=-15, description="请假太频繁", enabled=True),
            PointItem(name="自暴自弃（态度消极）", points=-10, description="保持积极心态", enabled=True),
            PointItem(name="超过00:20睡觉", points=-13, description="熬夜了", enabled=True),
            PointItem(name="超过01:00睡觉", points=-10, description="严重熬夜", enabled=True),
            PointItem(name="学习期间摸鱼一次", points=-11, description="学习不专心", enabled=True),
            PointItem(name="学习期间摸鱼两次", points=-12, description="学习太不专心", enabled=True),
            PointItem(name="学习期间摸鱼三次以上", points=-15, description="学习完全不专心", enabled=True),
            PointItem(name="抖音使用超过6小时", points=-12, description="娱乐时间过长", enabled=True),
            PointItem(name="抖音使用超过7小时", points=-15, description="娱乐时间太长", enabled=True),
            PointItem(name="抖音使用超过8小时", points=-10, description="娱乐时间严重超标", enabled=True),
            PointItem(name="姨妈期吃辣的冰的", points=-13, description="注意身体", enabled=True),
            PointItem(name="平时吃辣的冰的", points=-11, description="少吃刺激性食物", enabled=True),
            PointItem(name="热量摄入超标", points=-13, description="控制饮食", enabled=True),
            PointItem(name="连续一周不去健身房", points=-15, description="缺乏运动", enabled=True),
        ]
        
        for item in initial_items:
            db.session.add(item)
        
        print(f"✓ 添加 {len(initial_items)} 个初始积分项目")
        
        # 添加初始奖励
        initial_rewards = [
            Reward(name="请假半天卡", cost_points=60, description="可以请假半天", enabled=True),
            Reward(name="请假一天卡", cost_points=110, description="可以请假一整天", enabled=True),
            Reward(name="小零食盲盒", cost_points=80, description="随机零食惊喜", enabled=True),
            Reward(name="十盏美食一顿", cost_points=90, description="十盏美食任选", enabled=True),
            Reward(name="奶茶一杯", cost_points=60, description="喜欢的奶茶店任选", enabled=True),
            Reward(name="小蛋糕一个", cost_points=70, description="甜品店任选", enabled=True),
            Reward(name="冰粉一个", cost_points=6, description="解暑神器", enabled=True),
            Reward(name="和小猪见一面", cost_points=999, description="最珍贵的奖励❤️", enabled=True),
            Reward(name="和好如初卡", cost_points=200, description="消除误会的魔法卡", enabled=True),
            Reward(name="随心所欲卡", cost_points=300, description="想做什么都可以", enabled=True),
            Reward(name="美甲报销卡", cost_points=150, description="做美甲费用报销", enabled=True),
            Reward(name="盲盒小玩偶", cost_points=200, description="可爱的盲盒玩偶", enabled=True),
        ]
        
        for reward in initial_rewards:
            db.session.add(reward)
        
        print(f"✓ 添加 {len(initial_rewards)} 个初始奖励")
        
        # 提交到数据库
        db.session.commit()
        print("\n✓ 数据库初始化完成！")
        print("\n现在可以运行 python app.py 启动应用了")

if __name__ == '__main__':
    init_database()
