from read_config import *

a = read_config()["pits"]

# pit =   dict((tuple(el),0) for el in read_config()["goal"])
wall =   dict((tuple(el),0) for el in read_config()["walls"])
wall[(5,9)] = 1
print max(wall, key=wall.get)
print wall
if (5,9) in wall:
    print True