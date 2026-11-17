// usage: node analyze.cjs <prefix> <base> <arm>...
// Paired per-task medians (over reps) of cost, output tokens, API calls; majority-of-3 grades; hidden-test scores; sign test.
const fs=require("fs");const [pfx,base,...arms]=process.argv.slice(2);
const SIZE=p=>p<=11?"small":p<=13?"long":p<=17?"medium":p<=19?"large":"huge";
const med=a=>{a=[...a].sort((x,y)=>x-y);const n=a.length;return n?(n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2):NaN};
const mean=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:NaN;
const binom=(k,n)=>{let c=1,s=0;const t=[];for(let i=0;i<=n;i++){t.push(c);c=c*(n-i)/(i+1)}const m=Math.min(k,n-k);for(let i=0;i<=m;i++)s+=t[i];return Math.min(1,2*s/2**n)};
const runs={};
for(const f of fs.readdirSync("out").filter(f=>f.startsWith(pfx)&&f.endsWith(".jsonl"))){
 const m=f.slice(pfx.length).match(/^(.+)_p(\d+)_r(\d+)\.jsonl$/);if(!m)continue;
 let res,words=0;const ids=new Set();
 for(const l of fs.readFileSync("out/"+f,"utf8").split("\n")){let j;try{j=JSON.parse(l)}catch{continue}
  if(j.type==="result")res=j;
  if(j.type==="assistant"){ids.add(j.message.id);for(const c of j.message.content)if(c.type==="text")words+=c.text.split(/\s+/).filter(Boolean).length}}
 if(!res||res.is_error)continue;
 const rd=n=>{try{return JSON.parse(fs.readFileSync("out/"+f.replace(".jsonl",n),"utf8"))}catch{return null}};
 const gs=(t=>[`.${t}.json`,`.${t}2.json`,`.${t}3.json`])(process.env.GTAG||"grade").map(rd).filter(Boolean);
 let facts=null,clear=null;
 if(gs.length){const n=gs[0].criteria.length;let ok=0;for(let i=0;i<n;i++)if(gs.filter(g=>g.criteria[i]).length*2>gs.length)ok++;facts=ok/n;clear=gs.filter(g=>g.clear).length*2>gs.length?1:0}
 const v=rd(".verify.json");
 (runs[m[1]+"|"+m[2]]??=[]).push({cost:res.total_cost_usd,out:res.usage.output_tokens,api:ids.size,words,score:v?v.passed/v.total:null,facts,clear});
}
const M=(s,p,k)=>{const a=(runs[s+"|"+p]||[]).map(r=>r[k]).filter(x=>x!==null);return ["score","facts","clear"].includes(k)?mean(a):med(a)};
const prompts=[...new Set(Object.keys(runs).map(k=>+k.split("|")[1]))].sort((a,b)=>a-b);
for(const s of arms){
 console.log(`\n== ${s} vs ${base}`);
 const rows=[];
 for(const p of prompts){if(!runs[s+"|"+p]||!runs[base+"|"+p])continue;
  const r={p,size:SIZE(p),n:runs[base+"|"+p].length+"/"+runs[s+"|"+p].length};
  for(const k of ["cost","out","api","words"]){r[k+"B"]=M(base,p,k);r[k+"S"]=M(s,p,k);r[k]=100*(r[k+"S"]/r[k+"B"]-1)}
  for(const k of ["score","facts","clear"]){r[k+"B"]=M(base,p,k);r[k+"S"]=M(s,p,k)}
  rows.push(r);
  const f=x=>isNaN(x)?" -  ":x.toFixed(2);
  console.log(`p${String(p).padEnd(3)}${r.size.padEnd(7)}${r.n} cost ${r.costB.toFixed(2)}→${r.costS.toFixed(2)} ${r.cost.toFixed(0).padStart(4)}% | out ${r.out.toFixed(0).padStart(4)}% | api ${r.apiB}→${r.apiS} | words ${r.wordsB}→${r.wordsS} | tests ${f(r.scoreB)}→${f(r.scoreS)} | facts ${f(r.factsB)}→${f(r.factsS)} | clear ${f(r.clearB)}→${f(r.clearS)}`)}
 const grp=(name,sel)=>{const a=rows.filter(sel);if(!a.length)return;const neg=a.filter(r=>r.cost<0).length;
  const pf=(k)=>{const v=a.map(r=>r[k+"B"]).filter(x=>!isNaN(x)),w=a.map(r=>r[k+"S"]).filter(x=>!isNaN(x));return v.length?(100*mean(v)).toFixed(1)+"→"+(100*mean(w)).toFixed(1):"-"};
  console.log(`  ${name.padEnd(22)} tasks ${a.length}: median cost ${med(a.map(r=>r.cost)).toFixed(1)}% (cheaper on ${neg}/${a.length}, sign p=${binom(neg,a.length).toFixed(3)}) | out ${med(a.map(r=>r.out)).toFixed(1)}% | api ${med(a.map(r=>r.api)).toFixed(1)}% | words ${med(a.map(r=>r.words)).toFixed(1)}% | tests ${pf("score")} | facts ${pf("facts")} | clear ${pf("clear")}`)};
 grp("small (no/light tools)",r=>r.size==="small");grp("long answers",r=>r.size==="long");grp("medium",r=>r.size==="medium");grp("large",r=>r.size==="large");grp("huge",r=>r.size==="huge");
 grp("HEADLINE medium+large+huge",r=>["medium","large","huge"].includes(r.size));grp("all",()=>true);
}
let tot=0;for(const a of Object.values(runs))for(const r of a)tot+=r.cost;console.log("\nruns",Object.values(runs).flat().length,"spend $"+tot.toFixed(2));
