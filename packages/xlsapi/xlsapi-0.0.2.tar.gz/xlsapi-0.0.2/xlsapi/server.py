from flask import (
  Flask,
  render_template,
  jsonify
)

app = Flask(__name__, template_folder="./templates")

@app.route('/')
def home():
  """
  This function just responds to the browser URL localhost:5000

  :return: the rendered template 'home.html'
  """
  return render_template('home.html')

@app.route("/ajax/")
def some_json():
    return jsonify(success=True)

def getApp():
  """
  This function returns the app object for unit testing.

  :return: app object
  """
  return app

def run():
  """
  This function starts a local test server with the XLSAPI.
  """
  app.config['ENV'] = 'development'    
  app.config['TESTING'] = True
  app.run(debug=True)