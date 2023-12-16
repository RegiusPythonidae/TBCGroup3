from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize, FileField
from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to


class AddProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    img = FileField("სურათის სახელი",
                    validators=[
                        FileRequired(),
                        FileAllowed(["jpeg", "jpg", "png"], message="მისაღებია მხოლოდ სურათები"),
                        FileSize(1024 * 1024 * 5, message="ფაილი უნდა იყოს მაქსიმუმ 5 მეგაბაიტი")
                    ])

    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი")
    password = PasswordField("შეიყვანეთ პაროლი", validators=[length(min=8, max=64, message="პაროლის უნდა იყოს მინიმუმ 8 ასო")])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password", message="პაროლები არ ემთხვევა")])
    gender = RadioField("მონიშნეთ სქესი", choices=["კაცი", "ქალი"])
    birthday = DateField("დაბადების თარიღი")
    country = SelectField("მონიშნეთ ქვეყანა", choices=["საქართველო", "გერმანია", "საფრანგეთი"])
    about = TextAreaField("თქვენს შესახებ")

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired()])

    submit = SubmitField("ავტორიზაცია")