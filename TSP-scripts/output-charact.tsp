----------------
-- TSP PROGRAM FOR PERFORMING OFET OUTPUT MEASUREMENTS
-- Sweeps over channel and gate input voltages and measures channel current


-------- PARAMETERS --------
VdStart = 0
VdEnd = 2
VdStep = 0.1

VgStart = 0
VgEnd = 2
VgStep = 1

-------- MAIN PROGRAM --------
reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 700)

-- Clear buffers
smua.nvbuffer1.clear()
smub.nvbuffer1.clear()
-- Prepare buffers
smua.nvbuffer1.collectsourcevalues = 1
smub.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smub.nvbuffer1.appendmode = 1
smua.measure.count = 1
smub.measure.count = 1

--SMUA setup
smua.measure.delayfactor = 1.0
smua.measure.nplc = 10
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti = 1e-5
smua.measure.rangei = 10e-6

--SMUB setup
smub.measure.delayfactor = 1.0
smub.measure.nplc = 10
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti = 1e-7

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCVOLTS
display.screen = display.SMUA_SMUB

-- MEASUREMENT ROUTINE
Vg = VgStart
smub.source.levelv = Vg
smub.source.output = smub.OUTPUT_ON
delay(1)

while Vg <= VgEnd do
    smub.source.levelv = Vg
    smub.source.output = smub.OUTPUT_ON
    delay(1)
    
    Vd = VdStart
    smua.source.levelv = Vd
    smua.source.output = smua.OUTPUT_ON
    delay(1)
    
    while Vd <= VdEnd do
        smua.source.levelv = Vd
        smua.source.output = smua.OUTPUT_ON
        delay(0.4)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.i(smub.nvbuffer1)
        Vd = Vd + VdStep
        smua.source.output = smua.OUTPUT_OFF
    end
    
    smub.source.output = smub.OUTPUT_OFF
    Vg = Vg + VgStep
    
end

waitcomplete()
-------- END --------
