from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, PointItem, PointLog, Reward, RewardExchange
from init_db import seed_initial_data
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')  # 用于 flash 消息
# Render 会注入 DATABASE_URL（PostgreSQL），本地未设置时回退到 SQLite。
database_url = os.getenv('DATABASE_URL', 'sqlite:///points.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True
}

# 初始化数据库
db.init_app(app)

# 首次部署可能未手动初始化，启动时自动确保表存在，避免访问页面时报 500。
with app.app_context():
    db.create_all()
    seed_initial_data()


# ==================== 辅助函数 ====================

def get_total_points():
    """计算当前总积分"""
    # 获得的总积分
    earned_points = db.session.query(db.func.sum(PointLog.points)).scalar() or 0
    # 消耗的总积分
    spent_points = db.session.query(db.func.sum(RewardExchange.cost_points)).scalar() or 0
    return earned_points - spent_points


# ==================== 首页 ====================

@app.route('/')
def index():
    """首页 - 显示总积分和积分记录"""
    total_points = get_total_points()
    # 获取所有积分记录，按时间倒序
    logs = PointLog.query.order_by(PointLog.created_at.desc()).all()
    return render_template('index.html', 
                         total_points=total_points, 
                         logs=logs)


# ==================== 积分项目管理 ====================

@app.route('/items')
def items():
    """积分项目管理页面"""
    items = PointItem.query.order_by(PointItem.created_at.desc()).all()
    return render_template('items.html', items=items)


@app.route('/items/add', methods=['POST'])
def add_item():
    """新增积分项目"""
    name = request.form.get('name', '').strip()
    points = request.form.get('points', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name or not points:
        flash('项目名称和积分不能为空', 'error')
        return redirect(url_for('items'))
    
    try:
        points = int(points)
    except ValueError:
        flash('积分必须是数字', 'error')
        return redirect(url_for('items'))
    
    new_item = PointItem(
        name=name,
        points=points,
        description=description,
        enabled=True
    )
    db.session.add(new_item)
    db.session.commit()
    
    flash(f'积分项目「{name}」创建成功！', 'success')
    return redirect(url_for('items'))


@app.route('/items/edit/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    """编辑积分项目"""
    item = PointItem.query.get_or_404(item_id)
    
    name = request.form.get('name', '').strip()
    points = request.form.get('points', '').strip()
    description = request.form.get('description', '').strip()
    enabled = request.form.get('enabled') == 'on'
    
    if not name or not points:
        flash('项目名称和积分不能为空', 'error')
        return redirect(url_for('items'))
    
    try:
        points = int(points)
    except ValueError:
        flash('积分必须是数字', 'error')
        return redirect(url_for('items'))
    
    item.name = name
    item.points = points
    item.description = description
    item.enabled = enabled
    db.session.commit()
    
    flash(f'积分项目「{name}」更新成功！', 'success')
    return redirect(url_for('items'))


@app.route('/items/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """删除积分项目"""
    item = PointItem.query.get_or_404(item_id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    
    flash(f'积分项目「{name}」已删除', 'success')
    return redirect(url_for('items'))


# ==================== 积分记录 ====================

@app.route('/add-record')
def add_record():
    """新增积分记录页面（加分）"""
    # 只显示启用的正分项目
    items = PointItem.query.filter(PointItem.enabled==True, PointItem.points > 0).order_by(PointItem.name).all()
    return render_template('add_record.html', items=items)


@app.route('/subtract-record')
def subtract_record():
    """扣分记录页面"""
    # 只显示启用的负分项目
    items = PointItem.query.filter(PointItem.enabled==True, PointItem.points < 0).order_by(PointItem.name).all()
    return render_template('subtract_record.html', items=items)


@app.route('/add-record/submit', methods=['POST'])
def submit_record():
    """提交积分记录"""
    item_id = request.form.get('item_id')
    
    if not item_id:
        flash('请选择积分项目', 'error')
        return redirect(url_for('add_record'))
    
    item = PointItem.query.get_or_404(item_id)
    
    # 创建积分记录
    log = PointLog(
        item_id=item.id,
        item_name=item.name,
        points=item.points
    )
    db.session.add(log)
    db.session.commit()
    
    # 温馨提示文案
    messages = [
        f'太棒了！「{item.name}」+{item.points} 分 🌟',
        f'今天也很棒哦！「{item.name}」+{item.points} 分 💕',
        f'继续加油！「{item.name}」+{item.points} 分 ✨',
        f'你真棒！「{item.name}」+{item.points} 分 🎉',
        f'好厉害！「{item.name}」+{item.points} 分 💪'
    ]
    import random
    flash(random.choice(messages), 'success')
    
    return redirect(url_for('index'))


@app.route('/logs/add-manual', methods=['POST'])
def add_manual_log():
    """手动添加积分记录"""
    item_name = request.form.get('item_name', '').strip()
    points = request.form.get('points', '').strip()
    
    if not item_name or not points:
        flash('项目名称和积分不能为空', 'error')
        return redirect(url_for('index'))
    
    try:
        points = int(points)
    except ValueError:
        flash('积分必须是数字', 'error')
        return redirect(url_for('index'))
    
    # 创建积分记录
    log = PointLog(
        item_name=item_name,
        points=points
    )
    db.session.add(log)
    db.session.commit()
    
    if points > 0:
        flash(f'成功添加「{item_name}」+{points} 分！', 'success')
    else:
        flash(f'成功添加「{item_name}」{points} 分！', 'success')
    
    return redirect(url_for('index'))


@app.route('/logs/edit/<int:log_id>', methods=['POST'])
def edit_log(log_id):
    """编辑积分记录"""
    log = PointLog.query.get_or_404(log_id)
    
    item_name = request.form.get('item_name', '').strip()
    points = request.form.get('points', '').strip()
    
    if not item_name or not points:
        flash('项目名称和积分不能为空', 'error')
        return redirect(url_for('index'))
    
    try:
        points = int(points)
    except ValueError:
        flash('积分必须是数字', 'error')
        return redirect(url_for('index'))
    
    log.item_name = item_name
    log.points = points
    db.session.commit()
    
    flash(f'积分记录「{item_name}」更新成功！', 'success')
    return redirect(url_for('index'))


@app.route('/logs/delete/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    """删除积分记录"""
    log = PointLog.query.get_or_404(log_id)
    item_name = log.item_name
    db.session.delete(log)
    db.session.commit()
    
    flash(f'积分记录「{item_name}」已删除', 'success')
    return redirect(url_for('index'))


# ==================== 奖励兑换 ====================

@app.route('/rewards')
def rewards():
    """奖励兑换页面"""
    total_points = get_total_points()
    rewards = Reward.query.filter_by(enabled=True).order_by(Reward.cost_points).all()
    return render_template('rewards.html', 
                         total_points=total_points, 
                         rewards=rewards)


@app.route('/rewards/exchange/<int:reward_id>', methods=['POST'])
def exchange_reward(reward_id):
    """兑换奖励"""
    reward = Reward.query.get_or_404(reward_id)
    total_points = get_total_points()
    
    # 检查积分是否足够
    if total_points < reward.cost_points:
        flash(f'积分不足，还差 {reward.cost_points - total_points} 分哦~', 'error')
        return redirect(url_for('rewards'))
    
    # 创建兑换记录
    exchange = RewardExchange(
        reward_id=reward.id,
        reward_name=reward.name,
        cost_points=reward.cost_points
    )
    db.session.add(exchange)
    db.session.commit()
    
    remaining = total_points - reward.cost_points
    flash(f'成功兑换「{reward.name}」！消耗 {reward.cost_points} 分，剩余 {remaining} 分 🎁', 'success')
    return redirect(url_for('rewards'))


@app.route('/rewards/add', methods=['POST'])
def add_reward():
    """新增奖励"""
    name = request.form.get('name', '').strip()
    cost_points = request.form.get('cost_points', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name or not cost_points:
        flash('奖励名称和所需积分不能为空', 'error')
        return redirect(url_for('rewards'))
    
    try:
        cost_points = int(cost_points)
    except ValueError:
        flash('所需积分必须是数字', 'error')
        return redirect(url_for('rewards'))
    
    new_reward = Reward(
        name=name,
        cost_points=cost_points,
        description=description,
        enabled=True
    )
    db.session.add(new_reward)
    db.session.commit()
    
    flash(f'奖励「{name}」创建成功！', 'success')
    return redirect(url_for('rewards'))


@app.route('/rewards/edit/<int:reward_id>', methods=['POST'])
def edit_reward(reward_id):
    """编辑奖励"""
    reward = Reward.query.get_or_404(reward_id)
    
    name = request.form.get('name', '').strip()
    cost_points = request.form.get('cost_points', '').strip()
    description = request.form.get('description', '').strip()
    enabled = request.form.get('enabled') == 'on'
    
    if not name or not cost_points:
        flash('奖励名称和所需积分不能为空', 'error')
        return redirect(url_for('rewards'))
    
    try:
        cost_points = int(cost_points)
    except ValueError:
        flash('所需积分必须是数字', 'error')
        return redirect(url_for('rewards'))
    
    reward.name = name
    reward.cost_points = cost_points
    reward.description = description
    reward.enabled = enabled
    db.session.commit()
    
    flash(f'奖励「{name}」更新成功！', 'success')
    return redirect(url_for('rewards'))


@app.route('/rewards/delete/<int:reward_id>', methods=['POST'])
def delete_reward(reward_id):
    """删除奖励"""
    reward = Reward.query.get_or_404(reward_id)
    name = reward.name
    db.session.delete(reward)
    db.session.commit()
    
    flash(f'奖励「{name}」已删除', 'success')
    return redirect(url_for('rewards'))


# ==================== 兑换记录 ====================

@app.route('/exchanges')
def exchanges():
    """兑换记录页面"""
    exchanges = RewardExchange.query.order_by(RewardExchange.exchanged_at.desc()).all()
    total_spent = db.session.query(db.func.sum(RewardExchange.cost_points)).scalar() or 0
    return render_template('exchanges.html', 
                         exchanges=exchanges,
                         total_spent=total_spent)


# ==================== 运行应用 ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
