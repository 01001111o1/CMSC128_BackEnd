import os


dirname = os.path.dirname(os.path.abspath(__file__))
filename = dirname.replace('\\','/')

print(filename)
print(filename + '/static/imgs/icons/qr-code-payment.png')