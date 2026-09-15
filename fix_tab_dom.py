import re

with open('index.html', 'r') as f:
    html = f.read()

# We want to move the closing `</div>` of `view-physical` from before `tab-walk` to after `tab-walk`.

target = """
                    </div>
                </div>
            </div>
            
                <div id="tab-walk" class="tab-content">
"""
# Note: The first `</div>` closes coach-panel. The second `</div>` closes tab-tracker. The third `</div>` closes view-physical.
# So we just want to remove the third `</div>` and put it after tab-walk.

# Actually, let's just find `tab-walk` and the previous `</div>`.
pattern = r'(                    </div>\n                </div>\n            </div>)\n            \n                <div id="tab-walk" class="tab-content">'
replacement = r'                    </div>\n                </div>\n            \n                <div id="tab-walk" class="tab-content">'

if target in html:
    html = html.replace(target, replacement)
    
    # now append </div> before NUTRITION VIEW
    html = html.replace("            <!-- 3. NUTRITION VIEW -->", "            </div>\n            <!-- 3. NUTRITION VIEW -->")
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("Fixed dom")
else:
    print("Not found")

