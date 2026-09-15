const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/g);
if (scriptMatch) {
  scriptMatch.forEach((s, i) => {
     let content = s.replace('<script>', '').replace('</script>', '');
     try {
       new Function(content);
       console.log('Script ' + i + ' OK');
     } catch(e) {
       console.log('Script ' + i + ' Error: ', e);
     }
  });
}
