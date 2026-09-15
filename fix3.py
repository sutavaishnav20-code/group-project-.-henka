with open('index.html', 'r') as f:
    text = f.read()

target = '                    </div>\n                </div>\n            </div>\n\n            \n                <div id="tab-walk" class="tab-content">'
rep = '                    </div>\n                </div>\n\n            \n                <div id="tab-walk" class="tab-content">'

if target in text:
    text = text.replace(target, rep)
    text = text.replace("            <!-- 3. NUTRITION VIEW -->", "            </div>\n            <!-- 3. NUTRITION VIEW -->")
    with open('index.html', 'w') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Not found")
