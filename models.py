from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NBAStats(db.Model):
    PLAYER_ID = db.Column(db.String(255), primary_key=True)
    RANK = db.Column(db.Integer)
    PLAYER = db.Column(db.String(255))  # Assuming 'PLAYER' is a String column, adjust the type if needed
    TEAM_ID = db.Column(db.String(255))
    TEAM = db.Column(db.String(255))
    GP = db.Column(db.Integer)
    MIN = db.Column(db.Integer)
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
    PTS = db.Column(db.Integer)
    EFF = db.Column(db.Integer)

