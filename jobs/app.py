from flask import Flask, render_template, g
import sqlite3

from flask.signals import signals_available

PATH = 'db/jobs.sqlite'

app = Flask(__name__)


def open_connection(): 
  connection = getattr(g,'_connection', None)
  if(connection is None):
    connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
  return connection

def execute_sql():
  connection = open_connection()
  sql = ""
  values = ()
  commit = False
  single = False
  cursor = connection.execute(sql,values)
  if(commit): 
    results = connection.commit()
  else: 
    results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close
  return results

@app.teardown_appcontext
def close_connection(exception): 
  connection = getattr(g,'_connection',None)
  if(connection is not None): connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
  return render_template('index.html')