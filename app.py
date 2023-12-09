import os
from flask import Flask, render_template, send_from_directory, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text  # Import the text function
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO


import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import quote
import traceback

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

# app.py
@app.route('/player_details/<player_name>')
def player_details(player_name):
    player = NBAStats.query.filter_by(PLAYER=player_name).first()

    if not player:
        return render_template('error.html', error_message='Player not found')

    league_averages = {
        'FG_PCT': db.session.query(func.avg(NBAStats.FG_PCT)).scalar(),
        'FG3_PCT': db.session.query(func.avg(NBAStats.FG3_PCT)).scalar(),
        # Add more statistics as needed
    }

    player_chart = create_radar_chart(player)
    heatmap_data = create_heatmap(player)

    return render_template('player_details.html', player=player, player_chart=player_chart, heatmap_data=heatmap_data)

def create_heatmap(player):
    # Convert player stats to DataFrame
    player_stats = NBAStats.query.filter_by(PLAYER=player.PLAYER).first()
    heatmap_data = {
        'PTS': player_stats.PTS,
        'AST': player_stats.AST,
        'REB': player_stats.REB,
        'STL': player_stats.STL,
        'BLK': player_stats.BLK,
    }

    # Create the heatmap
    correlation_matrix = pd.DataFrame([heatmap_data])
    plt.figure(figsize=(8, 6))
    heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)

    # Change the color of the category labels
    heatmap.set_xticklabels(heatmap.get_xticklabels(), color='white')
    heatmap.set_yticklabels(heatmap.get_yticklabels(), color='white')

    # Change the color of the heatmap title
    heatmap.set_title(f'{player.PLAYER} Game Impact Heatmap', color='white')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.close()

    # Encode the plot as base64 for embedding in HTML
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    return plot_data


# Function to create radar chart
def create_radar_chart(player):
    categories = ['PTS', 'AST', 'REB', 'STL', 'BLK']
    player_stats = [getattr(player, category) for category in categories]

    num_categories = len(categories)
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
    player_stats += player_stats[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, player_stats, color='b', alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels=categories)

    # Add a title to the radar chart
    ax.set_title(f'{player.PLAYER} Radar Chart', color='white', fontsize=16)

    # Save the radar chart to a file or return it as an image
    chart_filename = f"{player.PLAYER.replace(' ', '_')}_radar_chart.png"
    chart_filepath = os.path.join('static', chart_filename)
    plt.savefig(chart_filepath, bbox_inches='tight', pad_inches=0, transparent=True) 
    plt.close()

    return chart_filename




if __name__ == '__main__':
    app.run(debug=True)
