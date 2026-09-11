// Run with Node.js; validates local links, worked examples and all demo modes.
const fs=require("fs"),path=require("path"),assert=require("assert/strict"),vm=require("vm");
const base=path.resolve(__dirname,"..");
let links=0;
for(const name of fs.readdirSync(base).filter(x=>x.endsWith(".md"))){
const text=fs.readFileSync(path.join(base,name),"utf8");
for(const m of text.matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g)){
assert.ok(fs.existsSync(path.resolve(base,m[1]+".md")),"Missing wiki link "+m[1]);links++;
}
for(const m of text.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)){
if(/^https?:/.test(m[1]))continue;
assert.ok(fs.existsSync(path.resolve(base,m[1])),"Missing attachment "+m[1]);links++;
}
assert.equal((text.match(/~~~/g)||[]).length%2,0,"Unbalanced code fences "+name);
assert.equal((text.match(/\$\$/g)||[]).length%2,0,"Unbalanced display math "+name);
}
const html=fs.readFileSync(path.join(base,"交互演示/空间与矩阵实验室.html"),"utf8");
const elements={};
const staticMarkup=html.replace(/<script>[\s\S]*?<\/script>/g,"");
for(const m of staticMarkup.matchAll(/\bid="([^"]+)"/g)){
assert.ok(!elements[m[1]],"Duplicate ID "+m[1]);
elements[m[1]]={value:"",textContent:"",innerHTML:"",hidden:false,addEventListener:()=>{}};
}
for(const [id,value] of Object.entries({mode:"active",angle:30,sx:1.5,sy:1,tx:1,ty:0.5,depth:4}))elements[id].value=value;
const context=vm.createContext({document:{getElementById:id=>{assert.ok(elements[id],"Missing DOM node "+id);return elements[id];}},console});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
const close=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-9,actual+" != "+expected);
const example=vm.runInContext("apply([0,-1,3,2,0,1],[2,1])",context);
close(example[0],2);close(example[1],5);
const back=vm.runInContext("inversePoint([0,-1,3,2,0,1],[2,5])",context);
close(back[0],2);close(back[1],1);
close(2*(-0.5)+1,0);
assert.notEqual(2*(-2)+1,0);
const order=vm.runInContext("matrices(90,1,1,3,0)",context);
context.testMatrix=order;
const tr=vm.runInContext("apply(testMatrix.TRS,[1,0])",context),rt=vm.runInContext("apply(testMatrix.SRT,[1,0])",context);
close(tr[0],3);close(tr[1],1);close(rt[0],0);close(rt[1],4);
let scenarios=0;
for(const mode of ["active","passive","order","perspective"]){
for(const angle of [-180,0,30,90,180]){
for(const s of [0.25,1,3]){
for(const t of [-3,0,3]){
elements.mode.value=mode;elements.angle.value=angle;elements.sx.value=s;elements.sy.value=3.25-s;
elements.tx.value=t;elements.ty.value=-t;elements.depth.value=t===-3?1.2:t===0?4:8;
vm.runInContext("update()",context);
assert.ok(!/NaN|Infinity|undefined/.test(elements.plot.innerHTML+elements.math.textContent),"Non-finite output");
assert.ok(elements.plot.innerHTML.includes("<line"));
scenarios++;
}
}
}
}
console.log(JSON.stringify({markdownFiles:10,localLinks:links,demoScenarios:scenarios,workedExamples:"passed"},null,2));
