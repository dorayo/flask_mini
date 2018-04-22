from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):
    # validators 有很多种，这里 DataRequired 用来进行非空验证
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'))
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('密码确认'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('注册'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('用户已存在，请更换用户名'))

    def validate_email(self, email=email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('用户已存在，请更换邮箱'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('重置密码'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('请输入新密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('请再次输入新密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('确认重置'))
