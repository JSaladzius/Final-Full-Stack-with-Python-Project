from app import app, db, login_manager, bcrypt
from app.forms import LoginForm , RegistrationForm , AddNoteForm, AddCategoryForm
from flask import flash, redirect, render_template, request, url_for, session
from flask_login import current_user ,login_required,login_user,logout_user
import secrets
from PIL import Image
import os

from app.db_models.User import User
from app.db_models.Category import Category
from app.db_models.Note import Note


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=['GET','POST'])
def home():
    form = LoginForm()
    return render_template("base.html", title="LOG iN", form=form)


@app.route("/login" , methods=['GET','POST'])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form=LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('No luck. Check email or password', 'warning')
    return render_template("login.html", title="LOG iN", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('log_in'))


@app.route("/register" , methods=['GET', 'POST'])
def register():
    db.create_all
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, email = form.email.data, password = encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash('Register successfull')
        return redirect(url_for('log_in'))
    return render_template('register.html', form = form)


@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    categories = Category.query.all()
    return render_template ("main.html", categories=categories)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    category = Category.query.get_or_404(id)    
    try:
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('main'))
    except:
        flash("NOPE, not deleted")
        return redirect(url_for('main'))
    

@app.route('/edit/<int:id>', methods =['GET' , 'POST'])
def edit_category(id):
    categories = Category.query.all()
    category = Category.query.get_or_404(id)
    form = AddCategoryForm()
    if form.validate_on_submit():
        category.category_name = form.name.data
        db.session.add(category)
        db.session.commit()
        print('category updated!!!!')
        return redirect(url_for('main'))
    form.name.data = category.category_name
    return render_template('edit_category.html' , form=form, categories=categories )


@app.route('/add', methods =['GET' , 'POST'])
def add_category():
    categories = Category.query.all()
   
    form = AddCategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(category_name = form.name.data)
        db.session.add(category)
        db.session.commit()
        print('Category added')
        return redirect(url_for('main'))
    return render_template ("addCategory.html",form=form , categories=categories)


@app.route('/notes/<int:id>', methods=['GET', 'POST'])
def notes(id):
    session['selected_category_id'] = id
    notes = Note.query.filter_by(id_category = id).all()
    categories = Category.query.all()
    pictures = url_for('static', filename=f'/images/{notes}')
    return render_template ("notes.html" , id_category = id, notes=notes , 
                             categories=categories)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route('/add_note/<int:id>', methods=['GET', 'POST'])
def add_note(id):
    category_id = id
    form = AddNoteForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        if form.picture.data:
            print(form.picture.data, 'YEAHHHHHHHHHHHHH')
            note = Note.query.all()
            new_picture = save_picture(form.picture.data)
            
        
        note = Note(name = form.name.data , 
                    text = form.text.data,
                    id_category = category_id,
                    picture = new_picture
                    )
        db.session.add(note)
        db.session.commit()
        flash('Note added')
        return redirect(url_for('main')) 
    return render_template ("add_note.html", form=form, category_id = category_id)


