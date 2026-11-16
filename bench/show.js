const fs=require('fs'),path=require('path');const dir=path.join(__dirname,'out');
for(const id of process.argv.slice(2)){let text='';
  for(const l of fs.readFileSync(path.join(dir,id+'.jsonl'),'utf8').split('\n')){if(!l.trim())continue;let j;try{j=JSON.parse(l)}catch{continue}
    if(j.type==='assistant')for(const c of j.message.content){if(c.type==='text')text+=c.text+'\n';if(c.type==='tool_use')text+=`[${c.name}]\n`}}
  console.log(`=== ${id}\n${text.trim()}\n`)}
