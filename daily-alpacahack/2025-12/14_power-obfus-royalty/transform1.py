import re

data = open("distfiles/power_obfus_royalty.ps1", "r").read()

pattern = r'\[[cC][hH][aA][rR]\]\d+'

for _ in range(2):
    matches = re.findall(pattern, data)

    for match in matches:
        num = int(re.search(r'\d+', match).group())
        char = chr(num)
        data = data.replace(match, f'"{char}"')

    data = data.replace('"+"', "")

print(data)
