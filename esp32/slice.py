response = ""

with open('esp32/response.txt') as f:
    response = f.read()

res = response.split('\n\n')
print('Header: \r\n%s\r\n\r\nBody: \r\n%s' % (res[0], res[1]))