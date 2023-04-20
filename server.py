# RESTful API
from flask import Flask, g, request, jsonify, Response, make_response
import sqlite3
import json
import urllib

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/api/items")  # default method is GET
def get_items(): # this is the counterpart of show_list() from homework 3
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    response = Response(json.dumps(tdlist),  mimetype='application/json')
    return response


@app.route("/api/items", methods=['POST'])
def add_item(): # this is the counterpart of add_entry() from homework 3
    db = get_db()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               [request.json['what_to_do'], request.json['due_date']])
    db.commit()
    return jsonify({"result": True})


@app.route("/api/item/<item>", methods=['PUT', 'DELETE'])
def update_item(item): # this is the counterpart of mark_as_done() from homework 3
    db = get_db()
    response = None
    
    if request.method == 'PUT':
        try:
            db.execute(f"UPDATE entries SET status='done' WHERE what_to_do='{urllib.parse.quote(item)}'")
            db.commit()
            response = Response(response="<h2>Success</h2>", status=200)
        except:
            response = Response(response="<h2>Error</h2>", status=500)

    elif request.method == 'DELETE':
        try:
            db.execute(f"DELETE FROM entries WHERE what_to_do='{item}'")
            db.commit()
            response = Response(response="<h2>Success</h2>", status=200)
        except:
            response = Response(response="<h2>Error</h2>", status=500)
            
    return response

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
