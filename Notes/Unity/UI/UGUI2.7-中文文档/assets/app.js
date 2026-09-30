const toggle=document.querySelector('.menu-toggle');
toggle?.addEventListener('click',()=>{const open=document.body.classList.toggle('menu-open');toggle.setAttribute('aria-expanded',String(open));});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('menu-open');toggle?.setAttribute('aria-expanded','false');}});
document.querySelector('.print')?.addEventListener('click',()=>window.print());
document.querySelectorAll('#sidebar details a.active').forEach(a=>{if(window.innerWidth>680)a.scrollIntoView({block:'center'});});
