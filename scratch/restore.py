import os, re

# 1. Restore Cory SVG and transparent CSS
for root, dirs, files in os.walk("."):
    if "node_modules" in root or ".git" in root or "scratch" in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace img src
            content = re.sub(
                r'(<button[^>]*class=["\'][^>]*?(?:floating-ai|cory-trigger)[^>]*?["\'][^>]*>\s*<img[^>]*src=)["\'][^"\']*?["\']',
                r'\1"../assets/corychaticon.svg"',
                content,
                flags=re.IGNORECASE | re.DOTALL
            )
            
            def repl_main(m):
                block = m.group(0)
                block = re.sub(r'border:\s*3px solid #[0-9a-fA-F]+;', 'border: none;', block)
                block = re.sub(r'background:\s*#[0-9a-fA-F]+;', 'background: transparent;', block)
                block = re.sub(r'box-shadow:[^;]+;', 'box-shadow: none;', block)
                return block
                
            content = re.sub(r'\.(?:floating-ai|cory-trigger)\s*{[^}]+}', repl_main, content)
            
            def repl_hover(m):
                block = m.group(0)
                block = re.sub(r'background:\s*#[0-9a-fA-F]+;', 'background: transparent;', block)
                return block
                
            content = re.sub(r'\.(?:floating-ai|cory-trigger):(hover|focus-visible)\s*(?:,\s*\.(?:floating-ai|cory-trigger):(hover|focus-visible)\s*)?{[^}]+}', repl_hover, content)

            def repl_img(m):
                block = m.group(0)
                block = re.sub(r'width:[^;]+;', 'width: 100%;', block)
                block = re.sub(r'height:[^;]+;', 'height: 100%;', block)
                return block
                
            content = re.sub(r'\.(?:floating-ai|cory-trigger)\s+img\s*{[^}]+}', repl_img, content)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

print("Cory styles restored")
