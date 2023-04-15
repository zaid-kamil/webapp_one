from flask import Flask, render_template, request, redirect
import plotly.express as px
app = Flask(__name__)


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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
 