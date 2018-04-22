from flask import render_template, flash, redirect, url_for, request, g, current_app
from app.main.forms import EditProfileForm
from app.main import bp
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.models import User
from flask_babel import _, get_locale


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())
    # Flask-Babel 支持的简体中文为 zh_Hans_CN，而 moment.js 支持的中文为 zh_cn
    if g.locale == 'zh_Hans_CN':
        g.locale = 'zh_cn'


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title=_('首页'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('修改已经保存成功！'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    else:
        pass
    return render_template('edit_profile.html', title=_('编辑个人页面'), form=form)
