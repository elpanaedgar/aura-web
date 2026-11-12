const {chromium}=require('playwright'); const fs=require('fs');
const bt=JSON.parse(fs.readFileSync('aura3/bottles.json','utf8'));
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const out=await p.evaluate(async(src)=>{
  const img=await new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=src;});
  function make(S,pad,round){ const c=document.createElement('canvas');c.width=c.height=S;const x=c.getContext('2d');
    const g=x.createLinearGradient(0,0,0,S); g.addColorStop(0,'#FCF0EC'); g.addColorStop(1,'#EEDDF0'); x.fillStyle=g; x.fillRect(0,0,S,S);
    const rg=x.createRadialGradient(S/2,S*.46,0,S/2,S*.46,S*.45); rg.addColorStop(0,'rgba(255,255,255,.95)'); rg.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=rg; x.fillRect(0,0,S,S);
    x.strokeStyle='#C8A46A'; x.lineWidth=S*.008; x.beginPath(); x.arc(S/2,S*.47,S*(.5-pad)*.78,0,Math.PI*2); x.stroke();
    const h=S*(1-pad*2)*.82, w=h*img.width/img.height; x.shadowColor='rgba(96,52,72,.25)'; x.shadowBlur=S*.03; x.shadowOffsetY=S*.015;
    x.drawImage(img,(S-w)/2,(S-h)/2+S*.01,w,h); return c.toDataURL('image/png'); }
  return {i512:make(512,.08), i192:make(192,.08), a180:make(180,.08), m512:make(512,.18), f32:make(64,.04)};
}, bt.lavanda);
for (const [k,f] of [['i512','icon-512.png'],['i192','icon-192.png'],['a180','apple-touch-icon.png'],['m512','maskable-512.png'],['f32','favicon.png']]) fs.writeFileSync('deploy/aura/icons/'+f,Buffer.from(out[k].split(',')[1],'base64'));
await b.close();})();
