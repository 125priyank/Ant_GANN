import json
bsfile = 'F:\\Render_output\\content\\save\\'
with open('{}save1190.json'.format(bsfile)) as fp: 
    data = json.load(fp)

tmp = {'ant': data['ant'][:1000], 'food' : data['food'][:1000]}
tmp2 = {'ant': data['ant'][1000:2000], 'food' : data['food'][1000:2000]}
with open('{}sv1000.json'.format(bsfile), 'w') as fp:
    json.dump(tmp, fp)

with open('{}sv2000.json'.format(bsfile), 'w') as fp:
    json.dump(tmp2, fp)