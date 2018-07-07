#  line intersection detection
#  line1: (x1, y1) to (x2, y2)
#  line2: (x3, y3) to (x4, y4)
def Intercept(x1, y1, x2, y2, x3, y3, x4, y4, d):
    denom = ((y4-y3) * (x2-x1)) - ((x4-x3) * (y2-y1))
    if (denom != 0):
        ua = (((x4-x3) * (y1-y3)) - ((y4-y3) * (x1-x3))) / denom
        if ((ua >= 0) and (ua <= 1)):
            ub = (((x2-x1) * (y1-y3)) - ((y2-y1) * (x1-x3))) / denom
            if ((ub >= 0) and (ub <= 1)):
                x = x1 + (ua * (x2-x1))
                y = y1 + (ua * (y2-y1))
                #print("interception detected")
                return (x, y, d)
    return None


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0
