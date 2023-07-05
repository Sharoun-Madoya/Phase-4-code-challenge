from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)
db = SQLAlchemy()

hero_power = db.Table(
    'hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('heros.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'), primary_key=True),
    db.Column("strength", db.String),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column("updated_at", db.DateTime, onupdate=db.func.now())
)

class Hero(db.Model):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String)
    super_name =db.Column(db.String)
    
    powers = db.relationship(
        'Power',
        secondary=hero_power,
        back_populates='heros'
    )
    # powers = db.relationship('Power', backref='hero')

    def __repr__(self):
        return f"<Hero {self.id}: {self.name} is {self.super_name}>"

class Power(db.Model):
    __tablename__= 'powers'

    id = db.Column(db.Integer, primary_key= True)
    name =db.Column(db.String)
    description = db.Column(db.String)

    heros = db.relationship(
        'Hero',
        secondary=hero_power,
        back_populates='powers'
    )
    # heros=db.relationship('HeroPower', backref='power' )

    def __repr__(self):
        return f'Power {self.id}: {self.name} does {self.description}'







# class HeroPower(db.Model):
#     __tablename__= 'heropowers'

#     id = db.Column(db.Integer, primary_key= True)
#     strength = db.Column(db.String)

#     hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
#     power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

# add any models you may need. 