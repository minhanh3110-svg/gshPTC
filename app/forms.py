from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class RegistrationForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Đăng ký')

class SampleForm(FlaskForm):
    code = StringField('Mã mẫu', validators=[DataRequired(), Length(max=20)])
    name = StringField('Tên mẫu', validators=[DataRequired(), Length(max=100)])
    type = SelectField('Loại mẫu', choices=[
        ('water', 'Mẫu nước'),
        ('soil', 'Mẫu đất'),
        ('air', 'Mẫu không khí'),
        ('other', 'Khác')
    ])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Lưu mẫu')

class TestResultForm(FlaskForm):
    test_name = StringField('Tên xét nghiệm', validators=[DataRequired(), Length(max=100)])
    result_value = StringField('Kết quả', validators=[DataRequired()])
    status = SelectField('Trạng thái', choices=[
        ('pending', 'Đang xử lý'),
        ('completed', 'Hoàn thành'),
        ('failed', 'Thất bại')
    ])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Lưu kết quả')

class EnvironmentLogForm(FlaskForm):
    temperature = FloatField('Nhiệt độ (°C)', validators=[DataRequired()])
    humidity = FloatField('Độ ẩm (%)', validators=[DataRequired()])
    location = StringField('Vị trí', validators=[DataRequired(), Length(max=50)])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Lưu thông số') 