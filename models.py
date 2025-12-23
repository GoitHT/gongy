from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class PointItem(db.Model):
    """积分项目表 - 定义可获得积分的行为模板"""
    __tablename__ = 'point_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 项目名称
    points = db.Column(db.Integer, nullable=False)  # 积分分值
    description = db.Column(db.String(200))  # 项目说明
    enabled = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<PointItem {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'points': self.points,
            'description': self.description,
            'enabled': self.enabled,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class PointLog(db.Model):
    """积分记录表 - 记录每次积分变化"""
    __tablename__ = 'point_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('point_items.id'))  # 关联的项目ID
    item_name = db.Column(db.String(100), nullable=False)  # 项目名称（冗余存储，避免项目删除后找不到）
    points = db.Column(db.Integer, nullable=False)  # 获得的积分
    created_at = db.Column(db.DateTime, default=datetime.now)  # 记录时间
    
    # 关联
    item = db.relationship('PointItem', backref='logs')
    
    def __repr__(self):
        return f'<PointLog {self.item_name} +{self.points}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'points': self.points,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Reward(db.Model):
    """奖励表 - 定义可兑换的奖励"""
    __tablename__ = 'rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 奖励名称
    cost_points = db.Column(db.Integer, nullable=False)  # 所需积分
    description = db.Column(db.String(200))  # 奖励说明
    enabled = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Reward {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cost_points': self.cost_points,
            'description': self.description,
            'enabled': self.enabled,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class RewardExchange(db.Model):
    """奖励兑换记录表 - 记录每次兑换"""
    __tablename__ = 'reward_exchanges'
    
    id = db.Column(db.Integer, primary_key=True)
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))  # 关联的奖励ID
    reward_name = db.Column(db.String(100), nullable=False)  # 奖励名称
    cost_points = db.Column(db.Integer, nullable=False)  # 消耗的积分
    exchanged_at = db.Column(db.DateTime, default=datetime.now)  # 兑换时间
    
    # 关联
    reward = db.relationship('Reward', backref='exchanges')
    
    def __repr__(self):
        return f'<RewardExchange {self.reward_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'reward_id': self.reward_id,
            'reward_name': self.reward_name,
            'cost_points': self.cost_points,
            'exchanged_at': self.exchanged_at.strftime('%Y-%m-%d %H:%M:%S')
        }
