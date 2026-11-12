import re
d='aura3/'
s=open(d+'aura-demo.src.html').read()
s=s.replace('__HERO__',open(d+'hero.b64').read().strip()).replace('__HOJAS__',open(d+'hojas.b64').read().strip())
import json
s=s.replace('__BOTTLES__',json.dumps(json.load(open(d+'bottles.json'))))
s=s.replace('__BOT__',open(d+'bot.json').read())
open(d+'aura-demo.html','w').write(s)
js=re.search(r'<script>(.*)</script>',s,re.S).group(1); open('check.js','w').write(js)
for m in re.finditer(r'&&',js): print('&& at', js[max(0,m.start()-60):m.start()+20].replace('\n',' ')[:90])
