from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open_time = TimeField("Opening Time (e.g. 15:30)", validators=[DataRequired()], format='%H:%M')
    close_time = TimeField("Closing Time (e.g. 22:00)", validators=[DataRequired()], format='%H:%M')
    coff_rate = SelectField(u'Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi_rate = SelectField(u'Wifi Strength Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power = SelectField(u'Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open(file="cafe-data.csv", newline="", mode='a',encoding='utf-8') as csv_file:
            # print(form.data)                              # returns dictionary
            # print(form.data.values())                       # returns dict obj list
            new_cafe = list(form.data.values())[:-2]        # form.data returns a dictionary so use values() to only get the list of values
            # print(new_cafe)
            writer = csv.writer(csv_file)
            writer.writerow(new_cafe)
        return render_template('add.html',form =CafeForm(formdata=None))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # newline='' -> sometimes while writing some platforms adds "\r\n" for newline instead of '\n' but csv module has its
    # own convention of adding new rows. newline='' replaces that will empty string as it is safe to use( it does'nt alter
    # csv files
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
