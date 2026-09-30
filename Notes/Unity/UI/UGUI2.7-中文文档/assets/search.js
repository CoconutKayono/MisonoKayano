const input=document.getElementById('search'),results=document.getElementById('search-results'),status=document.getElementById('search-status'),chapters=document.getElementById('chapter-list');
const escapeHTML=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let timer;
input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(search,120);});
function search(){
 const q=input.value.trim().toLowerCase();results.replaceChildren();
 if(!q){status.textContent='支持中文与英文全文搜索，离线可用。';chapters.hidden=false;return;}
 const terms=q.split(/\s+/);const found=window.DOCS.map(d=>{const title=(d.title+' '+d.english).toLowerCase(),text=d.text.toLowerCase();return{d,score:terms.every(t=>(title+' '+text).includes(t))?terms.reduce((n,t)=>n+(title.includes(t)?4:1),0):0};}).filter(x=>x.score).sort((a,b)=>b.score-a.score);
 status.textContent=`找到 ${found.length} 篇文档`;chapters.hidden=true;
 for(const {d} of found){const a=document.createElement('a');a.href=d.url;const pos=Math.max(0,d.text.toLowerCase().indexOf(terms[0])-35);let excerpt=d.text.slice(pos,pos+150);if(pos>0)excerpt='…'+excerpt;if(pos+150<d.text.length)excerpt+='…';a.innerHTML='<small>'+escapeHTML(d.group)+'</small><strong>'+escapeHTML(d.title)+'</strong><p>'+escapeHTML(excerpt)+'</p>';results.append(a);}
}
