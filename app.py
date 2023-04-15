from flask import Flask, render_template, request, redirect
import plotly.express as px
from database import Vehicle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.utils import secure_filename

app = Flask(__name__)

def getdb():
    engine = create_engine('sqlite:///project.sqlite')
    DBSession = sessionmaker(bind=engine)
    session = scoped_session(DBSession)
    return session

def load_gapminder():
    df = px.data.gapminder()
    return df

@app.route('/')
def index():
    name = "Sample Project One"
    return render_template('index.html', title=name)

@app.route('/home', methods=['GET', 'POST'])
def home():
    df = load_gapminder()
    fig1 = None
    if request.method=='POST':
        country = request.form.get('country')
        year = request.form.get('year')
        if len(country) == 0 and len(year) != 0:
            year = int(year)
            result = df.query("year == @year")
            fig1 = px.sunburst(result, path=['continent', 'country'], values='pop')
            fig1 = fig1.to_html()
        elif len(year) == 0 and len(country) != 0:
            result = df.query("country == @country")
            fig1 = px.area(result, x='year', y='pop')
            fig1 = fig1.to_html()
        elif len(country) != 0 and len(year) != 0:
            year = int(year)
            result = df.query("country == @country").query("year == @year")
        else:
            result = df
        return render_template('home.html',
                               result=result.to_html(),
                               fig1 = fig1)
    return render_template('home.html')

@app.route('/vehicle/add', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        image = request.files.get('file')
        # validate the data
        if len(name) == 0 or len(contact) == 0 or image is None:
            print("Please fill all the fields")
            return redirect('/vehicle/add')
        # save the file in a folder
        filename = secure_filename(image.filename)
        filepath = 'static/uploads/'+filename
        image.save(filepath)
        print('file saved')
        # save the data in the database
        db = getdb()
        db.add(Vehicle(name=name, contact=contact, image=filepath))
        db.commit()
        db.close()
        print('data saved')
        return redirect('/vehicle/add') 

    return render_template('vehicle.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
 