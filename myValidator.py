from myScanner import *
from myParser import *

file = open("docker-compose/compose1.yaml")

input_string = file.read()
file.close()

print(input_string)
scanner = Scanner(input_string)
for token in scanner.tokens:
    print(token)

parser = Parser(scanner)
parser.start()
  
