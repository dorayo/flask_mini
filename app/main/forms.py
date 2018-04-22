from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from app.models import User
from flask_babel import _, lazy_gettext as _l


class EditProfileForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    about_me = TextAreaField(_l('关于我'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('用户已存在，请更换用户名'))
