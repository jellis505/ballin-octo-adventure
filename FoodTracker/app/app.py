from flask import Flask, render_template, request, redirect, abort
from flask.ext.script import Manager
from database_utils import insert_submission

app = Flask(__name__, static_folder="../static", static_url_path="/static")
app.debug = True

@app.route('/')
def index():
    return render_template('index.jinja2.html');

@app.route('/barowner', methods=['GET', 'POST'])
def barowner():
    if request.method == 'POST':
        process_barowner_sumbit();
        return render_template('index.jinja2.html')
    else:
        return render_template('barowner.jinja2.html');

def process_barowner_sumbit():
    form = request.form;
    single_submit = dict(
         Email=form['Email'],
         Phone=form['Phone'],
         Form_Type='Bar-Owner'
         );
    insert_submission(single_submit);
    return True;
    
@app.route('/bar-goer', methods=['GET','POST'])
def bargoer():
    if request.method == 'POST':
        process_bargoer_sumbit();
        return render_template('index.jinja2.html');
    else:
        return render_template('bar-goer.jinja2.html');

def process_bargoer_sumbit():
    form = request.form;
    single_submit = dict(
         Email=form['Email'],
         Phone=form['Phone'],
         Form_Type='Bar-Goer'
         );
    insert_submission(single_submit);
    return True;
      
manager = Manager(app);

if __name__ == "__main__":
    manager.run()