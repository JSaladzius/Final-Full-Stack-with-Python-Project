from app import app, db, login_manager, bcrypt
from app.forms import LoginForm , RegistrationForm , AddNoteForm, AddCategoryForm , SearchForm
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
@login_required
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
@login_required
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
@login_required
def notes(id):
    if id:
        session['selected_category_id'] = id
        notes = Note.query.filter_by(id_category = id).all()
        categories = Category.query.all()
        # pictures = url_for('static', filename=f'/images/{notes}')
    else:
        notes = Note.query.all()


    return render_template ("notes.html" , id_category = id, notes=notes, 
                             categories=categories)

@app.route('/all_notes', methods=['GET', 'POST'])
@login_required
def all_notes():  
    categories = Category.query.all()
    notes = Note.query.all()
    return render_template ("notes.html" , notes=notes, 
                             categories=categories)






# @app.route('/display/<filename>')
# @login_required
# def display_image(filename):
#     print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='images/' + filename), code=301)


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


@app.route('/noting/<int:id>' , methods=['GET', 'POST'])
def noting(id):

    category= Category.query.filter_by(id=id).first()
    category_name = category.category_name

    form = AddNoteForm()
    categories = Category.query.all()

    category= Category.query.filter_by(id=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data, 'YEAHHHHHHHHHHHHH')
            note = Note.query.all()
            new_picture = save_picture(form.picture.data)
            note = Note(name = form.name.data , 
                    text = form.text.data,
                    id_category = id,
                    picture = new_picture
                    )

        else:
            note = Note(name = form.name.data , 
                    text = form.text.data,
                    id_category = id,
                    picture = ''
                    )
        db.session.add(note)
        db.session.commit()
        flash('Note added')
        return redirect(url_for('main'))

        

    return render_template ("add_note.html", form=form, categories=categories , name=category_name)



# @app.route('/add_note/<int:id>', methods=['GET', 'POST'])
# @login_required
# def add_note(id):
#     categories = Category.query.all()
#     category_id = id
#     category= Category.query.filter_by(id=category_id).first()
#     category_name = category.category_name
#     notes = Note.query.all()
#     note = Note.query.get_or_404(id)
#     form = AddNoteForm()
#     if request.method == 'POST' and form.validate_on_submit():
        
#         if form.picture.data:
#             print(form.picture.data, 'YEAHHHHHHHHHHHHH')
#             note = Note.query.all()
#             new_picture = save_picture(form.picture.data)
#             note = Note(name = form.name.data , 
#                     text = form.text.data,
#                     id_category = category_id,
#                     picture = new_picture
#                     )
#         else:
#             note = Note(name = form.name.data , 
#                     text = form.text.data,
#                     id_category = category_id,
#                     picture = ''
#                     )
#         db.session.add(note)
#         db.session.commit()
#         flash('Note added')
#         return redirect(url_for('main')) 
#     return render_template ("add_note.html", form=form, category_id = category_id, categories=categories, name=category_name)




def delete_picture(note_id):
    note_id = note_id
    note = Note.query.filter_by(id = note_id).first()
    picture_to_delete = note.picture
    if picture_to_delete:
        picture_to_delete = os.path.join(app.static_folder, 'images', picture_to_delete)
        if picture_to_delete and os.path.exists(picture_to_delete):
            os.remove(picture_to_delete)


@app.route('/edit_note/<int:id>', methods =['GET' , 'POST'])
@login_required
def edit_note(id):
    
    categories = Category.query.all()
    notes = Note.query.all()
    note = Note.query.get_or_404(id)
    form = AddNoteForm()
    if form.validate_on_submit():
        if form.picture.data:
            delete_old_picture = delete_picture(id)
            new_picture = save_picture(form.picture.data)
            note.picture = new_picture

        # note = Note(name = form.name.data , 
        #             text = form.text.data,
        #             picture = new_picture,
        #             id_category = id
        #             )    
        note.name = form.name.data
        note.text = form.text.data
       
        db.session.add(note)
        db.session.commit()
        flash('note updated!!!!')
        return redirect(url_for('main'))
    form.name.data = note.name
    form.text.data = note.text
    form.picture.data = note.picture
    
    return render_template('edit_note.html' , form=form, notes=notes ,categories=categories)




@app.route("/delete_note/<int:id>")
@login_required
def delete_note(id):
    print(id , "current id #####")
    note = Note.query.get_or_404(id)    
    try:
        delete_picture(id)
        db.session.delete(note)
        db.session.commit()
        flash("Note , deleted")
        return redirect(url_for('main'))
    except:
        flash("NOPE, not deleted")
        return redirect(url_for('main'))
    


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)



@app.route('/search', methods=["POST"])
def search():
    categories = Category.query.all()
    form = SearchForm()
    notes = Note.query
    if form.validate_on_submit():
        note_searched = form.searched.data
        notes_filtered = notes.filter(Note.name.like('%' + note_searched + '%'))
        notes_ordered = notes_filtered.order_by(Note.name).all()
        return render_template("notes.html" , form=form, searched = note_searched , notes=notes_ordered , categories=categories)