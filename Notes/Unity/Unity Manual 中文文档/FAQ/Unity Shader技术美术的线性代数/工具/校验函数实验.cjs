// Usage: node 校验函数实验.cjs <node_modules directory> <Chromium/Edge executable>
const assert=require("node:assert/strict"),path=require("node:path"),{pathToFileURL}=require("node:url");
const deps=process.argv[2],exe=process.argv[3];
if(!deps||!exe)throw Error("Pass node_modules directory and browser executable.");
const {chromium}=require(path.resolve(deps,"playwright"));
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:exe});
try{
const page=await browser.newPage({viewport:{width:1360,height:1000}});
const errors=[];page.on("pageerror",e=>errors.push(String(e)));
await page.goto(pathToFileURL(path.resolve(__dirname,"../交互演示/空间与矩阵实验室.html")).href);
const results=await page.evaluate(()=>{
const {definitions:d,defaults,evaluate:e}=FunctionLab;
const near=(a,b)=>{if(Math.abs(a-b)>1e-9)throw Error(a+" != "+b);};
near(e("remap",0.5),0.5);near(e("remap",0),-1/3);
near(e("remap",0,{...defaults("remap"),limit:true}),0);
near(e("remap",0.2,{inA:0.8,inB:0.2,outA:0,outB:1,limit:false}),1);
near(e("step",0.5),1);near(e("step",0.499999),0);
near(e("smooth",0.4),0.15625);near(e("smooth",0.5),0.5);
near(e("levels",0.5),2/3);near(e("levels",1),1);
near(e("posterize",0.999),0.75);near(e("posterize",1),1);
near(e("clamp",-1),0);near(e("clamp",2),1);
near(e("lerp",1.5),1.2);near(e("affine",0.2),0.2);
near(e("invert",1.5),-0.5);near(e("floor",-0.2),-1);
near(e("frac",-0.2,{frequency:1,phase:0}),0.8);
near(e("abs",0.2),0.3);near(e("power",0.5),0.25);near(e("power",-0.2),0);
near(e("sine",0),0.5);
for(let n=2;n<=12;n++){
const values=new Set(Array.from({length:1001},(_,i)=>e("levels",i/1000,{n}).toFixed(9)));
if(values.size!==n)throw Error("Wrong level count "+n);
}
let evaluated=0;
for(const [key,def]of Object.entries(d)){
const variants=[defaults(key)];
for(const p of def.params){
for(const val of p.check?[true,false]:[p.min,p.max])variants.push({...defaults(key),[p.key]:val});
}
for(const p of variants){
if(def.valid&&def.valid(p))continue;
for(let i=0;i<=300;i++){
if(!Number.isFinite(e(key,-1+i/100,p)))throw Error("Non-finite "+key);
evaluated++;
}
}
}
return {operations:Object.keys(d).length,numericalCases:evaluated,quantizationCounts:"N=2..12 passed"};
});
const keys=await page.evaluate(()=>Object.keys(FunctionLab.definitions));
for(const key of keys){
await page.selectOption("#fnOperation",key);
assert.equal(await page.locator("#fnError").isVisible(),false);
for(const field of ["ramp","radial","sphere","waves"]){
await page.selectOption("#fnField",field);
assert(!/NaN|Infinity/.test(await page.locator("#fnReadout").innerText()));
}
}
await page.selectOption("#fnOperation","levels");await page.selectOption("#fnField","ramp");
const grayscale=await page.evaluate(()=>{
const c=document.getElementById("fnAfter"),d=c.getContext("2d").getImageData(0,0,c.width,c.height).data,s=new Set();
for(let i=0;i<d.length;i+=4)s.add(d[i]);return [...s].sort((a,b)=>a-b);
});
assert.deepEqual(grayscale,[0,85,170,255]);
const before=await page.locator("#fnBefore").evaluate(c=>c.toDataURL());
const after=await page.locator("#fnAfter").evaluate(c=>c.toDataURL());
await page.locator("#fn-n").fill("6");
assert.equal(await page.locator("#fnBefore").evaluate(c=>c.toDataURL()),before);
assert.notEqual(await page.locator("#fnAfter").evaluate(c=>c.toDataURL()),after);
await page.selectOption("#fnOperation","remap");await page.locator("#fn-inB").fill("0.2");
assert(await page.locator("#fnError").isVisible());
await page.getByRole("button",{name:"重置当前操作",exact:true}).click();assert(!await page.locator("#fnError").isVisible());
await page.selectOption("#fnOperation","smooth");await page.locator("#fn-high").fill("0.2");assert(await page.locator("#fnError").isVisible());
await page.getByRole("button",{name:"卡通明暗分阶",exact:true}).click();
await page.locator("#fnProbeNumber").fill("0.999");
assert((await page.locator("#fnReadout").innerText()).includes("1.000"));
for(const name of ["拉开灰度对比","卡通明暗分阶","柔边圆形遮罩","重复圆环"]){
await page.getByRole("button",{name,exact:true}).click();assert(!await page.locator("#fnError").isVisible());
}
await page.selectOption("#fnOperation","step");
const box=await page.locator("#fnCurve").boundingBox();
await page.mouse.click(box.x+box.width*0.8,box.y+box.height*0.5);
assert(Number(await page.locator("#fnProbe").inputValue())>0.7);
await page.setViewportSize({width:390,height:844});
assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
await page.getByRole("button",{name:"空间与矩阵",exact:true}).click();
for(const mode of ["active","passive","order","perspective"]){
await page.selectOption("#mode",mode);assert(await page.locator("#plot").isVisible());
}
await page.getByRole("button",{name:"函数与灰度",exact:true}).click();
assert(await page.locator("#fnCurve").isVisible());
assert.equal(await page.evaluate(()=>{const ids=[...document.querySelectorAll("[id]")].map(n=>n.id);return ids.length===new Set(ids).size;}),true);
assert.deepEqual(errors,[]);
console.log(JSON.stringify({...results,previewCases:56,grayscale:"4 exact gray levels",invalidInputs:"handled",legacyModes:4,mobileOverflow:false,browserErrors:0},null,2));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
