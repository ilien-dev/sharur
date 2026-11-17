// exit 0 when a stream-json log holds a successful result event; 1 otherwise (usage limit, API error, no result)
const fs=require("fs");let ok=false;
for(const l of fs.readFileSync(process.argv[2],"utf8").split("\n")){try{const j=JSON.parse(l);if(j.type==="result")ok=!j.is_error&&!/hit your .* limit/i.test(j.result||"")}catch{}}
process.exit(ok?0:1)
