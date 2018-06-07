import json
f = open('code_name.json', encoding='utf-8')
text = f.read()
j = json.loads(text)


'''
f = open('code_all.txt')
l1 = f.read().split('\n')
d1 = {}
d2 = {}
for i in l1:
    name = i.split(',')[0]
    code = i.split(',')[1]
    d1[name] = code
    d2[code] = name

import json

f1 = open('code_name.json','w',encoding='utf-8')
f1.write(json.dumps(d2,ensure_ascii=False))
f1.close()
f2 = open('name_code.json','w',encoding='utf-8')
f2.write(json.dumps(d1,ensure_ascii=False))
f2.close()'''
