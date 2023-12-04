import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text  # Import the text function

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'nba.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Create Table for NBA DATA
class NBAStats(db.Model):
    __tablename__ = 'nba_stats'

    RANK = db.Column(db.Integer, primary_key=True)
    PLAYER = db.Column(db.String(255))
    TEAM = db.Column(db.String(255))
    GP = db.Column(db.Integer)
    MIN = db.Column(db.Integer)
    PTS = db.Column(db.Integer)
    FGM = db.Column(db.Integer)
    FGA = db.Column(db.Integer)
    FG_PCT = db.Column(db.Float)
    FG3M = db.Column(db.Integer)
    FG3A = db.Column(db.Integer)
    FG3_PCT = db.Column(db.Float)
    FTM = db.Column(db.Integer)
    FTA = db.Column(db.Integer)
    FT_PCT = db.Column(db.Float)
    OREB = db.Column(db.Integer)
    DREB = db.Column(db.Integer)
    REB = db.Column(db.Integer)
    AST = db.Column(db.Integer)
    STL = db.Column(db.Integer)
    BLK = db.Column(db.Integer)
    TOV = db.Column(db.Integer)
    
    EFF = db.Column(db.Integer)

# Flask route to render the 'layout.html' template
@app.route('/')
def index():
    return render_template('layout.html')

# Flask route to render the 'players.html' template
@app.route('/players')
def players():
    all_players = NBAStats.query.all()
    return render_template('players.html', players=all_players)

# Flask route to render the 'teams.html' template
@app.route('/teams')
def teams():
    return render_template('teams.html')

# Flask route to render the 'quiz.html' template
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
