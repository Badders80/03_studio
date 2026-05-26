import re
with open('/etc/ImageMagick-6/policy.xml', 'r') as f:
    content = f.read()
content = re.sub(r'<policy domain="path" rights="none" pattern="@\*"/>', r'<!-- <policy domain="path" rights="none" pattern="@*"/> -->', content)
with open('policy.xml', 'w') as f:
    f.write(content)
