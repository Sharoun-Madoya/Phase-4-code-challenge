from flask import Flask
from models import db, Power, Hero, hero_power
import random 
from random import choice as rc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Seeding Powers
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

with app.app_context():
    db.create_all()

    for power_data in powers_data:
        power = Power(**power_data)
        db.session.add(power)

    db.session.commit()

# Seeding Heroes
heroes_data = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

with app.app_context():
    for hero_data in heroes_data:
        hero = Hero(**hero_data)
        db.session.add(hero)

    db.session.commit()

# Adding Powers to Heroes


with app.app_context():
    heroes = Hero.query.all()
    powers = Power.query.all()

    for hero in heroes:
        num_powers = random.randint(1, 3)
        random_powers = random.sample(powers, num_powers)

        combination = set()
        strengths = ["Strong", "Weak", "Average"]
        for _ in range(30):
            strength = rc(strengths)
            power = rc(random_powers)
            hero_power_combination = (hero.id, power.id)

            if hero_power_combination in combination:
                continue

            combination.add(hero_power_combination)

            hero_power_data = {
                "hero_id": hero.id,
                "power_id": power.id,
                "strength": strength
            }
            statement = db.insert(hero_power).values(hero_power_data)
            db.session.execute(statement)

    db.session.commit()


        # for power in random_powers:
        #     hero_p = hero_power(hero=hero, power=power, strength=random.choice(strengths))
        #     db.session.add(hero_p)

print("🦸‍♀️ Done seeding!")










# strength = [strong, Weak, Average]
#   for strength in HeroPower

# puts "🦸‍♀️ Seeding powers..."
# Power.create([
#   { name: "super strength", description: "gives the wielder super-human strengths" },
#   { name: "flight", description: "gives the wielder the ability to fly through the skies at supersonic speed" },
#   { name: "super human senses", description: "allows the wielder to use her senses at a super-human level" },
#   { name: "elasticity", description: "can stretch the human body to extreme lengths" }
# ])

# puts "🦸‍♀️ Seeding heroes..."
# Hero.create([
#   { name: "Kamala Khan", super_name: "Ms. Marvel" },
#   { name: "Doreen Green", super_name: "Squirrel Girl" },
#   { name: "Gwen Stacy", super_name: "Spider-Gwen" },
#   { name: "Janet Van Dyne", super_name: "The Wasp" },
#   { name: "Wanda Maximoff", super_name: "Scarlet Witch" },
#   { name: "Carol Danvers", super_name: "Captain Marvel" },
#   { name: "Jean Grey", super_name: "Dark Phoenix" },
#   { name: "Ororo Munroe", super_name: "Storm" },
#   { name: "Kitty Pryde", super_name: "Shadowcat" },
#   { name: "Elektra Natchios", super_name: "Elektra" }
# ])

# puts "🦸‍♀️ Adding powers to heroes..."

# strengths = ["Strong", "Weak", "Average"]
# Hero.all.each do |hero|
#   rand(1..3).times do
#     # get a random power
#     power = Power.find(Power.pluck(:id).sample)

#     HeroPower.create!(hero_id: hero.id, power_id: power.id, strength: strengths.sample)
#   end
# end

# puts "🦸‍♀️ Done seeding!"


