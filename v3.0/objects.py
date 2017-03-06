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


class Resistance(BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    resistance_type_phys = des.SetValue(set=damageTypes['physical'])
    resistance_value_phys = des.PositiveNumber()
    resistance_type_mag = des.SetValue(set=damageTypes['magical'])
    resistance_value_mag = des.PositiveNumber()
    special_text = des.String()


list_of_resistances = ty.generate_type_listof(ty=Resistance)


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


class Armor(Equipable, BaseClass):
    uuid = des.PositiveInteger()
    name = des.String()
    price = des.PositiveNumber()
    weight = des.PositiveNumber()
    special_text = des.String()
    resistances = des.CustomTyped(ty=list_of_resistances)
    level = des.PositiveInteger()
    exp = des.PositiveNumber()


atk1 = Attack(0, 'swipe', 'SLASHING', 5.0, 'NONE', 0.0, 'simple but effective sword swipe')
atk2 = Attack(1, 'stab', 'PIERCING', 6.0, 'NONE', 0.0, 'simple but effective sword stab')
wep = Weapon(1, 'short sword', 1.0, 5.0, 'simple short sword', list_of_attacks(), 1, 0.0)
wep.attacks.append(atk1)
wep.attacks.append(atk2)


res1 = Resistance(0, 'heavy links', 'SLASHING', 5.0, 'NONE', 0.0, 'simple but effective against swiping')
res2 = Resistance(1, 'tight mesh', 'PIERCING', 6.0, 'NONE', 0.0, 'simple but effective against stabbing')
arm = Armor(1, 'chain mail', 3.0, 7.0, 'simple chainmail', list_of_resistances(), 1, 0.0)
arm.resistances.append(res1)
arm.resistances.append(res2)

for k, v in wep.__dict__.items():
    if not k == 'attacks':
        print(k, ':', repr(v))
    else:
        print('attacks : ')
        for a in v:
            for k1, v1 in a.__dict__.items():
                print('   ', k1, ':', repr(v1))

for k, v in arm.__dict__.items():
    if not k == 'resistances':
        print(k, ':', repr(v))
    else:
        print('resistances : ')
        for a in v:
            for k1, v1 in a.__dict__.items():
                print('   ', k1, ':', repr(v1))
