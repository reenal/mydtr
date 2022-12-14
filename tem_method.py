ΘH  #is the winding hottest-spot temperature, °C
ΘA #is the average ambient temperature during the load cycle to be studied, °C
ΔΘBO #is the bottom fluid rise over ambient, °C
ΔΘWO/BO #is the temperature rise of oil at winding hot-spot location over bottom oil, °C
ΔΘH/WO #is the winding hot-spot temperature rise over oil next to hot-spot location, °C


ΘH = ΘA + ΔΘBO + ΔΘWO/BO  + ΔΘH/WO


ΘAO #is the average fluid temperature in tank and radiator, °C
ΘBO #is the bottom fluid temperature, °C
ΘTO #is the top fluid temperature, °C
ΔΘT/B #is the temperature rise of fluid at top of radiator over bottom fluid, °C


ΘBO = ΘAO - ΔΘT/B/2
ΘTO = ΘAO + ΔΘT/B/2


#Average winding temperature

K #is the ratio of load L to rated load, per unit
KW #is the temperature correction for losses of winding
PE #is the eddy loss of windings at rated load, W
PW #is the winding I2R loss at rated load, W
QGEN,W #is the heat generated by windings, W-min
Δt #is the time increment for calculation, min


QGEN,W =K**2 *⎡(PW* KW )+ PE/KW ⎤ * Δt


KW  #is the temperature correction for losses of winding
ΘK #is the temperature factor for resistance correction, °C
ΘW,1 #is the average winding temperature at the prior time, °C
ΘW,R #is the average winding temperature at rated load tested, °C


KW = (ΘW,1 + ΘK) /(ΘW,R + ΘK)



PE #is the eddy loss of windings at rated load, W
PW #is the winding I2R loss at rated load, W
QLOST,W #is the heat lost by winding, W-min
ΘDAO,1 #is the average temperature of fluid in cooling ducts at the prior time, °C
ΘDAO,R # °C is the average temperature of fluid in cooling ducts at rated load, °C
ΘW,1 #is the average winding temperature at the prior time, °C
ΘW,R #is the average winding temperature at rated load tested,°C
Δt # is the time increment for calculation, min

QLOST,W = [ (ΘW,1  - ΘDAO,1)/ (ΘW,R - ΘDAO,R )] * (PW + PE)*Δt


MWCpW #is the winding mass times specific heat, W-min/°C
PE #is the eddy loss of windings at rated load, W
PW #is the winding I2R loss at rated load, W
ΘDAO,R #is the average temperature of fluid in cooling ducts at rated load, °C
ΘW,R #is the average winding temperature at rated load tested, °C
τW #is the winding time constant, min


MWCpW = [ (PW+PE)* τW ] /  (ΘW,R - ΘDAO,R)



MWCpW #is the winding mass times specific heat, W-min/°C
QGEN,W #is the heat generated by windings, W-min
QLOST,W #is the heat lost by winding, W-min
ΘW,1 #is the average winding temperature at the prior time, °C
ΘW,2 #is the average winding temperature at the next instant of time, °C

ΘW,2 = QGEN,W - QLOST,W + (MWCpW * ΘW,1) / MWCpW



