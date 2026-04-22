const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    file = path.join(dir, file);
    const stat = fs.statSync(file);
    if (stat && stat.isDirectory() && !file.includes('node_modules') && !file.includes('.git')) {
      results = results.concat(walk(file));
    } else if (file.endsWith('.html')) {
      results.push(file);
    }
  });
  return results;
}

const files = walk('.');
let replacedCount = 0;

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  const regex = /(<button[^>]*?class=["'][^"']*?\bfloating-ai\b[^"']*?["'][^>]*?>\s*<img[^>]*?src=["']).*?(["'][^>]*?>\s*<\/button>)/g;
  const newContent = content.replace(regex, '$1../assets/corychaticon.svg$2');
  if (content !== newContent) {
    fs.writeFileSync(file, newContent, 'utf8');
    replacedCount++;
    console.log('Replaced in:', file);
  }
});

console.log('Total files updated:', replacedCount);
