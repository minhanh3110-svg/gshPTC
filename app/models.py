from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    cultures = db.relationship('Culture', backref='researcher', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Culture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    plant_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    explant_type = db.Column(db.String(50))  # Loại mẫu cấy
    media_composition = db.Column(db.Text)  # Thành phần môi trường
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    subculture_date = db.Column(db.DateTime)  # Ngày cấy chuyền
    status = db.Column(db.String(20), default='active')
    contamination_status = db.Column(db.Boolean, default=False)
    researcher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    growth_records = db.relationship('GrowthRecord', backref='culture', lazy='dynamic')
    location = db.Column(db.String(50))  # Vị trí trong phòng nuôi cấy

class GrowthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    culture_id = db.Column(db.Integer, db.ForeignKey('culture.id'))
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    growth_status = db.Column(db.String(50))
    shoot_number = db.Column(db.Integer)  # Số chồi
    root_status = db.Column(db.String(50))  # Tình trạng rễ
    contamination_details = db.Column(db.Text)
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.String(100))

class MediaPreparation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(20), unique=True)
    media_type = db.Column(db.String(50))
    preparation_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    quantity = db.Column(db.Float)  # Số lượng (lít)
    ph_value = db.Column(db.Float)
    sterilization_date = db.Column(db.DateTime)
    prepared_by = db.Column(db.String(100))
    notes = db.Column(db.Text)

class EnvironmentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    room_name = db.Column(db.String(50))  # Tên phòng (nuôi cấy, chuẩn bị, etc.)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light_intensity = db.Column(db.Float)  # Cường độ ánh sáng
    co2_level = db.Column(db.Float)  # Nồng độ CO2
    air_flow_status = db.Column(db.String(20))  # Trạng thái luồng khí
    notes = db.Column(db.Text) 