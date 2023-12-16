from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path


from forms import AddProductForm, RegisterForm, LoginForm
from models import Product, ProductCategory, User
from ext import app


@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("search.html", products=products)


@app.route("/category/<int:category_id>")
def category(category_id):
    products = Product.query.filter(Product.category_id == category_id).all()
    return render_template("index.html", products=products)


@app.route("/view_product/<int:index>")
def view_product(index):
    product = Product.query.get(index)
    return render_template("product.html", product=product)


@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, img=form.img.data.filename)
        new_product.create()

        file_dir = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_dir)
        return redirect("/")
    return render_template("add_product.html", form=form)


@app.route("/edit_product/<int:index>", methods=["GET", "POST"])
@login_required
def edit_product(index):
    if current_user.role != "admin":
        return redirect("/")

    product = Product.query.get(index)
    form = AddProductForm(price=product.price, name=product.name, img=product.img)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.img = form.img.data.filename

        file_dir = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_dir)

        product.save()
        return redirect("/")
    return render_template("add_product.html", form=form)


@app.route("/delete_product/<int:index>")
@login_required
def delete_product(index):
    if current_user.role != "admin":
        return redirect("/")

    product = Product.query.get(index)
    product.delete()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data).first():
            flash("მომხმარებელი უკვე არსებობს, შეარჩიეთ სხვა სახელი")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/about_us")
def about():
    return render_template("about.html")