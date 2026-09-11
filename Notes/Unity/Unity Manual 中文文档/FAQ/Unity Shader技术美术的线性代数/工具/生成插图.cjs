// Run with Node.js. Regenerates only this tutorial's five SVG figures.
const fs = require("fs");
const path = require("path");
const out = path.resolve(__dirname, "../图片");
fs.mkdirSync(out, {recursive:true});
const C={ink:"#17324d",grid:"#dce5ed",red:"#bd3b48",green:"#14856e",blue:"#316db5",orange:"#b65a08",muted:"#687c90"};
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");
function svg(title, body, w=960,h=500){
return '<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'" role="img"><title>'+esc(title)+'</title><defs>'+
Object.entries(C).map(([k,c])=>'<marker id="'+k+'" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L7,3 Z" fill="'+c+'"/></marker>').join("")+
'</defs><rect width="100%" height="100%" fill="#fbfcfe"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="18" fill="'+C.ink+'">'+body+'</g></svg>';
}
const txt=(x,y,s,color=C.ink,size=18)=>'<text x="'+x+'" y="'+y+'" fill="'+color+'" font-size="'+size+'">'+esc(s)+'</text>';
function line(x1,y1,x2,y2,k="ink",width=2,dash=false,arrow=false){
return '<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+C[k]+'" stroke-width="'+width+'"'+(dash?' stroke-dasharray="7 5"':'')+(arrow?' marker-end="url(#'+k+')"':'')+'/>';
}
function plot(ox,oy,s){
const p=([x,y])=>[ox+x*s,oy-y*s];
return {
p,
line:(a,b,k="ink",w=2,dash=false,arrow=false)=>line(...p(a),...p(b),k,w,dash,arrow),
text:(a,t,k="ink",dx=8,dy=-8)=>txt(p(a)[0]+dx,p(a)[1]+dy,t,C[k]),
dot:(a,k="orange")=>'<circle cx="'+p(a)[0]+'" cy="'+p(a)[1]+'" r="6" fill="'+C[k]+'"/>',
grid:(xmin,xmax,ymin,ymax)=>{
let r="";
for(let i=xmin;i<=xmax;i++)r+=line(...p([i,ymin]),...p([i,ymax]),"grid",1);
for(let i=ymin;i<=ymax;i++)r+=line(...p([xmin,i]),...p([xmax,i]),"grid",1);
r+=line(...p([xmin,0]),...p([xmax,0]),"muted",1.5,false,true);
r+=line(...p([0,ymin]),...p([0,ymax]),"muted",1.5,false,true);
return r;
},
poly:(points,k="blue",dash=false)=>'<polygon points="'+points.map(q=>p(q).join(",")).join(" ")+'" fill="'+(dash?"none":C[k])+'" fill-opacity="0.1" stroke="'+C[k]+'" stroke-width="2"'+(dash?' stroke-dasharray="6 4"':'')+'/>'
};
}
function save(n,t,b,w,h){fs.writeFileSync(path.join(out,n),svg(t,b,w,h));}
{
const p=plot(90,430,65);
let b=txt(30,38,"同一个点，两份地址",C.ink,24)+p.grid(0,6,0,5);
b+=p.text([6,0],"世界 x")+p.text([0,5],"世界 y", "ink",10,-12);
b+=p.dot([3,1],"blue")+p.text([3,1],"o = (3,1)","blue",12,24);
b+=p.line([3,1],[3,3],"red",3,false,true)+p.text([3,2],"bₓ = (0,2)","red",16,0);
b+=p.line([3,1],[2,1],"green",3,false,true)+p.text([2,1],"bᵧ = (−1,0)","green",-110,30);
b+=p.line([3,3],[3,5],"red",2,true,true)+p.line([3,5],[2,5],"green",2,true,true);
b+=p.dot([2,5])+p.text([2,5],"P","orange",-24,-12);
b+=txt(570,115,"局部地址：Pₒ = (2,1)")+txt(570,160,"世界地址：P𝑤 = (2,5)");
b+=txt(570,225,"从 o 出发：")+txt(570,265,"走 2 次红色 x 轴",C.red)+txt(570,305,"再走 1 次绿色 y 轴",C.green);
b+=txt(570,375,"P = o + 2bₓ + bᵧ")+txt(570,415,"点没变，描述它的尺子变了。");
save("01-坐标系.svg","同一个点在局部与世界坐标中的表示",b);
}
{
let b=txt(30,36,"看两根基向量，就能看懂整个方格",C.ink,24);
const specs=[
["拉伸：x × 2",[[2,0],[0,1]],"面积 × 2"],
["逆时针 90°",[[0,1],[-1,0]],"长度与直角保持"],
["错切：x′ = x + y",[[1,0],[1,1]],"面积不变，直角改变"],
["镜像：x′ = −x", [[-1,0],[0,1]],"方向性翻转"]
];
specs.forEach(([name,cols,note],i)=>{
const x=240*(i%2), y=i<2?0:250; // changed below to two broad columns
const left=(i%2)*470, top=Math.floor(i/2)*270;
const p=plot(left+175,top+245,58);
const tr=([a,b])=>[a*cols[0][0]+b*cols[1][0],a*cols[0][1]+b*cols[1][1]];
b+=txt(left+30,top+80,name,C.ink,21)+p.grid(-2,3,-1,2);
b+=p.poly([[0,0],[1,0],[1,1],[0,1]],"muted",true);
b+=p.poly([[0,0],[1,0],[1,1],[0,1]].map(tr));
b+=p.line([0,0],cols[0],"red",3,false,true)+p.line([0,0],cols[1],"green",3,false,true);
b+=p.text(cols[0],"x′","red")+p.text(cols[1],"y′","green",8,-12);
b+=txt(left+30,top+320,note,C.muted,17);
});
save("02-基向量变换.svg","拉伸旋转错切镜像对基向量与单位方格的作用",b,960,620);
}
{
let b=txt(30,38,"顺序变了，终点也变了",C.ink,24);
for(let i=0;i<2;i++){
let p=plot(70+i*470,395,65);
b+=txt(30+i*470,80,i===0?"TRp：先转 90°，再右移 3":"RTp：先右移 3，再转 90°",C.ink,20);
b+=p.grid(0,5,0,4);
const a=[1,0],mid=i===0?[0,1]:[4,0],end=i===0?[3,1]:[0,4];
b+=p.dot(a,"blue")+p.text(a,"p = (1,0)","blue",0,30);
b+=p.line(a,mid,"blue",2,true,true)+p.dot(mid,"blue");
b+=p.line(mid,end,"orange",2,true,true)+p.dot(end);
b+=p.text(end,i===0?"(3,1)":"(0,4)","orange",10,-12);
b+=txt(30+i*470,465,i===0?"(1,0) → (0,1) → (3,1)":"(1,0) → (4,0) → (0,4)",C.ink,19);
}
b+=txt(30,505,"虚线连接运算前后的位置，只表示步骤，不表示旋转的真实运动轨迹。",C.muted,17);
save("03-变换顺序.svg","旋转与平移顺序的数值对照",b,960,535);
}
{
let b=txt(30,38,"透视：等高物体，距离越远，投影越小",C.ink,24);
const p=plot(90,345,150);
b+=p.line([0,0],[5,0],"muted",2,false,true);
b+=p.dot([0,0],"ink")+p.text([0,0],"相机","ink",-25,35);
b+=p.line([1,-0.4],[1,1.4],"muted",2,true)+p.text([1,1.4],"成像平面 z=1","ink",-65,-12);
b+=p.line([2,0],[2,1],"blue",5)+p.text([2,1],"z=2，高=1","blue",-40,-20);
b+=p.line([4,0],[4,1],"green",5)+p.text([4,1],"z=4，高=1","green",-40,-20);
b+=p.line([0,0],[2,1],"blue",2,true)+p.line([0,0],[4,1],"green",2,true);
b+=p.dot([1,0.5],"blue")+p.dot([1,0.25],"green");
b+=p.text([1,0.5],"1/2","blue",-55,-2)+p.text([1,0.25],"1/4","green",12,3);
b+=txt(35,435,"教学模型：向 +z 观察，f = 1；投影高度 = f × 高度 / 深度。",C.ink,20);
b+=txt(35,475,"示意成像平面放在相机前方；不是 Unity 的完整投影矩阵。",C.muted,18);
save("04-透视.svg","相似三角形解释近大远小",b,960,505);
}
{
let b=txt(30,38,"法线要保持垂直，而不只是跟着拉长",C.ink,24);
for(let i=0;i<2;i++){
const p=plot(240+470*i,330,75);
b+=txt(30+470*i,85,i===0?"变换前":"x 拉宽 2 倍后",C.ink,22);
b+=p.grid(-2,2,-1,2);
const t=i===0?[1,1]:[2,1],n=i===0?[-1,1]:[-0.5,1];
b+=p.line([-t[0],-t[1]],t,"blue",4,false,true)+p.text(t,i===0?"t=(1,1)":"t′=(2,1)","blue",-50,-16);
b+=p.line([0,0],n,"green",3,false,true)+p.text(n,i===0?"n=(−1,1)":"正确 (−0.5,1)","green",-95,-15);
if(i===1){
b+=p.line([0,0],[-2,1],"red",3,false,true)+p.text([-2,1],"错误 (−2,1)","red",-10,35);
}
b+=txt(30+470*i,440,i===0?"n · t = 0":"正确点积 = 0；错误点积 = −3",C.ink,19);
}
b+=txt(30,488,"为方便核对，这里画出未归一化的向量；实际着色时还需归一化。",C.muted,17);
save("05-法线逆转置.svg","逆转置保证法线与缩放后的切向量垂直",b,960,520);
}
console.log("Generated 5 SVG figures in "+out);

