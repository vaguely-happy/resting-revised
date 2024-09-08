multiline
<drac2>
ch = character()
classes    = load_json(get_gvar("2c66c52a-69a4-46e4-86db-9d7281f41b42"))
outstring = ""
hit_dice = {}

for (cls, lvl) in ch.levels:
	cls_info = classes.get(cls, {})
	size = cls_info.get("hit_die", 0)
	if not hit_dice.get(size):
		hit_dice[size] = {'str': "", 'int': 0}
	if size:
		hit_dice[size]['str'] += f"+{cls}Level"
		hit_dice[size]['int'] += lvl
		
for size, num in hit_dice.items():
	cc_name = f"Hit Dice (d{size})"
	cc = ch.create_cc_nx(cc_name, minVal=0, maxVal=num.int, reset="long")
	if ch.get_cc_max(cc_name) != num.int:
		ch.edit_cc(cc_name, maxVal=num.int)
		

		
outstring += f'''{ctx.prefix}game lr'''
return outstring

</drac2>
