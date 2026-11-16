const fs=require('fs'),path=require('path');
for(const id of process.argv.slice(2)){let s=[];
  for(const l of fs.readFileSync(path.join(__dirname,'out',id+'.jsonl'),'utf8').split('\n')){if(!l.trim())continue;let j;try{j=JSON.parse(l)}catch{continue}
    if(j.type==='assistant')for(const c of j.message.content){if(c.type==='tool_use')s.push(c.name+(c.input.description?`("${c.input.description}")`:c.input.command?`<${c.input.command.slice(0,40)}>`:''));if(c.type==='text')s.push('TEXT:'+c.text.trim())}}
  console.log(`=== ${id}\n${s.join('\n')}\n`)}
