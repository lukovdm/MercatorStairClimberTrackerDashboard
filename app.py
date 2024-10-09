from crypt import methods

from alembic.util.compat import importlib_resources
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory
from sqlalchemy import select, func

from models import db, User, StairClimb
from forms import RegisterForm, AddStairsForm
from config import Config
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def dashboard():
    res = db.session.execute(select(User).outerjoin(StairClimb).group_by(User.id).order_by(func.max(StairClimb.timestamp).desc()))
    users = [r[0] for r in res]
    forms = {user.id: AddStairsForm() for user in users}
    return render_template('dashboard.html', users=users, forms=forms)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        filename = None
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            form.profile_pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User(name=form.name.data, profile_pic=filename)
        db.session.add(user)
        db.session.commit()
        flash(f'Registration successful for {form.name.data}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/log_stairs/<int:user_id>', methods=['POST'])
def log_stairs(user_id):
    form = AddStairsForm()
    user = User.query.get_or_404(user_id)
    if form.validate_on_submit():
        climb = StairClimb(stairs_climbed=form.stairs_climbed.data, user_id=user.id)
        db.session.add(climb)
        db.session.commit()
        flash(f'{form.stairs_climbed.data} stairs added for {user.name}', 'success')
    return redirect(url_for('dashboard'))

@app.route('/profile_pics/<filename>', methods=['GET'])
def profile_pics(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
