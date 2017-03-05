from tims_insanity.utils.classes import BaseClass
import tims_insanity.utils.descriptors as des
import tims_insanity.utils.types as ty


damageTypes = {'physical': {'SLASHING', 'BLUNT', 'PIERCING', 'NONE'},
               'magical':  {'FIRE', 'POISON', 'ICE', 'NONE'}}


class Attack(BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    damage_type_phys = des.SetValue(set=damageTypes['physical'])
    damage_value_phys = des.PositiveNumber()
    damage_type_mag = des.SetValue(set=damageTypes['magical'])
    damage_value_mag = des.PositiveNumber()
    special_text = des.String()


list_of_attacks = ty.generate_type_listof(ty=Attack)
list_of_attacks_empty = list_of_attacks()


class Resistance(BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    damage_type_phys = des.SetValue(set=damageTypes['physical'])
    damage_value_phys = des.PositiveNumber()
    damage_type_mag = des.SetValue(set=damageTypes['magical'])
    damage_value_mag = des.PositiveNumber()
    special_text = des.String()


class Item(BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    price = des.PositiveNumber()
    weight = des.PositiveNumber()
    special_text = des.String()


class Equipable(Item, BaseClass):
    pass


class Weapon(Equipable, BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    price = des.PositiveNumber()
    weight = des.PositiveNumber()
    special_text = des.String()
    attacks = des.CustomTyped(ty=list_of_attacks)
    level = des.PositiveInteger()
    exp = des.PositiveNumber()


atk1 = Attack(0, 'swipe', 'SLASHING', 5.0, 'NONE', 0.0, 'simple but effective sword swipe')
wep = Weapon(1, 'short sword', 1.0, 5.0, 'simple short sword', list_of_attacks_empty, 1, 0.0)
wep.attacks.append(atk1)

print(repr(wep.__dict__))
