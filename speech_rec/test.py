readFromPotMeter =  None
maxValue = 1000
halfValue = maxValue / 2

while True:
    readFromPotMeter = read(etEllerAnnet)
    if readFromPotMeter >= halfValue:
        turnLedOn
    else:
        turnLedOff