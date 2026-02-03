multiline
<drac2>
arguments = &ARGS&
if not arguments: # recover would only be called if you want to actually recover.
	arguments = "1"
parsed = argparse(arguments)
mode = 'help'
hdused = False
n = '\n'
ch = character()
compact = parsed.last('h',parsed.last('compact',False))
counters = ch.consumables
counterNames = [x.name for x in counters]
hitDice = [f"d{x}" for x in range(20,0,-1)]
yourRace = get("race",ch.race)
Verdan = "ro<3" if yourRace.lower()=='verdan' else ""
spentDice = []
maxed = parsed.last('max',False)
periapt = 'periapt of wound closure' in get('attunedItems','').lower() or parsed.last('periapt',parsed.last('closure',False))
ownedHitDice = []
for hd in hitDice:
	if (hitdie := f"Hit Dice ({hd})") in counterNames:
		ownedHitDice.append(hitdie)
		if '-b' in arguments:
			arguments = arguments[:arguments.index('-b')]
		for arg in arguments:
			if 'd' in arg and hd == arg[arg.index('d'):]: # and arguments[arguments.index(arg)-1] != '-b': # not arg in parsed.get('b'):
				if 'b' in parsed:
					spentDice.append({"bonus":parsed.last('b'), "size":hd,"counter":f"Hit Dice ({hd})","numberSpent":min(int(arg.split('d')[0] if arg.split('d')[0] else arguments[arguments.index(arg)-1] if arguments.index(arg) and arguments[arguments.index(arg)-1].isdigit() else 1),ch.get_cc(f"Hit Dice ({hd})"))})
					parsed.ignore('b')
				else:
					spentDice.append({"size":hd,"counter":f"Hit Dice ({hd})","numberSpent":min(int(arg.split('d')[0] if arg.split('d')[0] else arguments[arguments.index(arg)-1] if arguments.index(arg) and arguments[arguments.index(arg)-1].isdigit() else 1),ch.get_cc(f"Hit Dice ({hd})"))})
if arguments and (arguments[0].isdigit()) and ownedHitDice and not spentDice:
	totalDice =  int(arguments[0])
	defaulthd = f"Hit Dice ({get('defaultHD',ownedHitDice[0][ownedHitDice[0].index('d'):-1])})"
	hitDieList = [defaulthd]+[die for die in ownedHitDice if die!=defaulthd]
	for hitdie in hitDieList:
		if totalDice <= 0:
			break
		if ch.cc_exists(hitdie) and ch.get_cc(hitdie):
			hd = hitdie[hitdie.index('d'):-1]
			if 'b' in parsed:
				spentDice.append({"size":hd,"counter":hitdie,"numberSpent":min(totalDice,ch.get_cc(hitdie)),"bonus":parsed.last('b')})
				parsed.ignore('b')
			else:
				spentDice.append({"size":hd,"counter":hitdie,"numberSpent":min(totalDice,ch.get_cc(hitdie))})
			totalDice -= ch.get_cc(hitdie)
spentDiceString = (', ' if len(spentDice)!=2 else ' and ').join([f"{'and ' if len(spentDice)>2 and spentDice[spentDice.index(die)]==spentDice[-1] else ''}{die.numberSpent} {die.size}" for die in spentDice]) or 0
hdRolls = [vroll(f"{die.numberSpent}{die.size.replace('d','*' if maxed else 'd')}{Verdan}{'*2[Periapt of Wound Closure]' if periapt else ''}{'+ ' + die.bonus if 'bonus' in die else ''}") for die in spentDice]
for die in spentDice:
	ch.mod_cc(die.counter,-die.numberSpent)
	hdused = True
hpGain = sum([Roll.total for Roll in hdRolls])
ch.modify_hp(hpGain,0,0)



outcommands = ""

outText = f'''{ctx.prefix}embed '''
if hdused:
	outText += (f''' -title "{name} spends hit dice"''')+(f''' -desc "{name} spends {spentDiceString} hit dice, recovering a total of {hpGain} hit points."''') if ownedHitDice else f''' -title "{name} hasn't set up hit dice yet." -desc "Take a  `!lr` to set up hit dice."'''
	outText += f''' -f "Healing|{n.join([str(Roll) for Roll in hdRolls])}|inline"''' if hpGain else ''
else:
	outText += (f''' -title "{name} Did not recover any hp"''')
outText += f''' -thumb {get("image")}'''
outcommands += outText + n		
return outcommands
</drac2>
