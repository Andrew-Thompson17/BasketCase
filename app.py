import os
from flask import Flask, render_template, send_from_directory, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy import text  # Import the text function
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO

from matplotlib.colors import LinearSegmentedColormap
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

#Create Table for PLAYER DATA
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
    id = db.Column(db.Integer, primary_key=True)

#Create table for regular season team data
class TeamsRegularSeason(db.Model):
    __tablename__ = 'teams_regular_season'

    rank = db.Column(db.Integer)
    team_name = db.Column(db.String(255))
    games_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float)
    minutes = db.Column(db.Integer)
    points = db.Column(db.Integer)
    field_goals_made = db.Column(db.Integer)
    field_goals_attempted = db.Column(db.Integer)
    field_goal_percentage = db.Column(db.Float)
    three_pointers_made = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_point_percentage = db.Column(db.Float)
    free_throws_made = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throw_percentage = db.Column(db.Float)
    offensive_rebounds = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    total_rebounds = db.Column(db.Integer,primary_key=True)
    assists = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    opponent_blocks = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    personal_fouls_drawn = db.Column(db.Integer)
    plus_minus = db.Column(db.Float)
    id = db.Column(db.Integer, primary_key=True)

#Create table for playoff team data
class TeamsPlayoff(db.Model):
    __tablename__ = 'teams_playoff'

    rank = db.Column(db.Integer)
    team_name = db.Column(db.String(255))
    games_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float)
    minutes = db.Column(db.Integer)
    points = db.Column(db.Integer)
    field_goals_made = db.Column(db.Integer)
    field_goals_attempted = db.Column(db.Integer)
    field_goal_percentage = db.Column(db.Float)
    three_pointers_made = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_point_percentage = db.Column(db.Float)
    free_throws_made = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throw_percentage = db.Column(db.Float)
    offensive_rebounds = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    total_rebounds = db.Column(db.Integer,primary_key=True)
    assists = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    opponent_blocks = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    personal_fouls_drawn = db.Column(db.Integer)
    plus_minus = db.Column(db.Float)
    id = db.Column(db.Integer, primary_key=True)

team_name_mapping = {
    'MIL': 'Milwaukee Bucks',
    'BOS': 'Boston Celtics',
    'PHI': 'Philadelphia 76ers',
    'DEN': 'Denver Nuggets',
    'CLE': 'Cleveland Cavaliers',
    'MEM': 'Memphis Grizzlies',
    'SAC': 'Sacramento Kings',
    'NYK': 'New York Knicks',
    'BKN': 'Brooklyn Nets',
    'PHX': 'Phoenix Suns',
    'GSW': 'Golden State Warriors',
    'LAC': 'LA Clippers',
    'MIA': 'Miami Heat',
    'LAL': 'Los Angeles Lakers',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'ATL': 'Atlanta Hawks',
    'TOR': 'Toronto Raptors',
    'CHI': 'Chicago Bulls',
    'OKC': 'Oklahoma City Thunder',
    'DAL': 'Dallas Mavericks',
    'UTA': 'Utah Jazz',
    'IND': 'Indiana Pacers',
    'WAS': 'Washington Wizards',
    'ORL': 'Orlando Magic',
    'POR': 'Portland Trail Blazers',
    'CHA': 'Charlotte Hornets',
    'HOU': 'Houston Rockets',
    'SAS': 'San Antonio Spurs',
    'DET': 'Detroit Pistons',
}

# Flask route to render the 'layout.html' template
@app.route('/')
def index():
    return render_template('home.html')

# Flask route to render the 'players.html' template
@app.route('/players')
def players():
    all_players = NBAStats.query.all()
    
    return render_template('players.html', players=all_players)

# Flask route to render the 'teams.html' template
@app.route('/teams')
def teams():
    # Get scatterplot data from the database
    scatterplot_data = db.session.query(
        TeamsRegularSeason.team_name,
        TeamsRegularSeason.wins,
        TeamsRegularSeason.plus_minus
    ).all()

    # Separate the scatterplot data into lists for Chart.js
    team_names = [data[0] for data in scatterplot_data]
    wins = [data[1] for data in scatterplot_data]
    plus_minus = [data[2] for data in scatterplot_data]

    # Combine wins and plus_minus into a zipped list
    data_zipped = zip(wins, plus_minus)

    table_data = TeamsRegularSeason.query.all()

    # Pass the data to the template
    return render_template('teams.html', team_names=team_names, data_zipped=data_zipped, table_data=table_data)

@app.route('/teams_playoff')
def teams_playoff():
    # Get playoff scatterplot data from the database
    playoff_data = db.session.query(
        TeamsPlayoff.team_name,
        TeamsPlayoff.wins,
        TeamsPlayoff.plus_minus
    ).all()

    # Separate the playoff scatterplot data into lists for Chart.js
    team_names_playoff = [data[0] for data in playoff_data]
    wins_playoff = [data[1] for data in playoff_data]
    plus_minus_playoff = [data[2] for data in playoff_data]

    # Combine wins and plus_minus into a zipped list for playoff
    data_zipped_playoff = zip(wins_playoff, plus_minus_playoff)

    # Get regular season scatterplot data from the database
    regular_data = db.session.query(
        TeamsRegularSeason.team_name,
        TeamsRegularSeason.wins,
        TeamsRegularSeason.plus_minus
    ).all()

    # Separate the regular season scatterplot data into lists for Chart.js
    team_names_regular = [data[0] for data in regular_data]
    wins_regular = [data[1] for data in regular_data]
    plus_minus_regular = [data[2] for data in regular_data]

    # Combine wins and plus_minus into a zipped list for regular season
    data_zipped_regular = zip(wins_regular, plus_minus_regular)

    # Get table data for playoff
    table_data_playoff = TeamsPlayoff.query.all()

    # Get table data for regular season
    table_data_regular = TeamsRegularSeason.query.all()

    # Pass the data to the template
    return render_template('teams_playoff.html',
                           team_names_playoff=team_names_playoff,
                           data_zipped_playoff=data_zipped_playoff,
                           table_data_playoff=table_data_playoff,
                           team_names_regular=team_names_regular,
                           data_zipped_regular=data_zipped_regular,
                           table_data_regular=table_data_regular)


@app.route('/player_details/<player_name>')
def player_details(player_name):
    player = NBAStats.query.filter_by(PLAYER=player_name).first()

    if not player:
        return render_template('error.html', error_message='Player not found')

    # Get the full team name using the mapping
    full_team_name = team_name_mapping.get(player.TEAM)

    # Perform a custom join based on team names
    team_alias = aliased(TeamsRegularSeason)
    team = db.session.query(team_alias).filter_by(team_name=full_team_name).first()
    league_averages = {
        'FG_PCT': db.session.query(func.avg(NBAStats.FG_PCT)).scalar(),
        'FG3_PCT': db.session.query(func.avg(NBAStats.FG3_PCT)).scalar(),
        'FGM': db.session.query(func.avg(NBAStats.FGM)).scalar(),
        'FG3M': db.session.query(func.avg(NBAStats.FG3M)).scalar(),
        'FTM': db.session.query(func.avg(NBAStats.FTM)).scalar(),
        'FT_PCT': db.session.query(func.avg(NBAStats.FT_PCT)).scalar(),
    }

    player_chart = create_radar_chart(player)
    heatmap_data = create_heatmap(player)

    return render_template('player_details.html', player=player, player_chart=player_chart, heatmap_data=heatmap_data, league_averages=league_averages, team=team)

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
    
    start_color = '#4BC0C0CC' 
    end_color = '#FF6384CC'
    
    cmap = LinearSegmentedColormap.from_list('custom', [start_color, end_color], N=256)

    # Create the heatmap
    correlation_matrix = pd.DataFrame([heatmap_data])
    plt.figure(figsize=(8, 6))
    heatmap = sns.heatmap(correlation_matrix, annot=True, cmap=cmap, linewidths=.5)

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
