----------------
-- TSP PROGRAM FOR PERFORMING INVERTER MEASUREMENT
-- Sweeps over an input voltgae range and measures an output voltage


-------- PARAMETERS --------
VinStart = -1
VinEnd = 1
VinStep = 0.1


-------- MAIN PROGRAM --------
reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)

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

-- SMUA setup
smua.measure.delayfactor = 1.0
smua.measure.nplc = 10
smua.source.func = smua.OUTPUT_DCVOLTS
smua.source.autorangev = smua.AUTORANGE_ON
-- Compliance here relates to gate leakage
smua.source.limiti = 1e-8

-- SMUB setup
smub.measure.nplc = 10
smub.sense = smub.SENSE_LOCAL
smub.measure.autorangev = smub.AUTORANGE_ON
smub.source.limiti = 1e-6

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCVOLTS
display.screen = display.SMUA_SMUB

-- MEASUREMENT ROUTINE
V = VinStart
smua.source.levelv = V
smua.source.output = smua.OUTPUT_ON
delay(1)

while V <= VinEnd do
        smua.source.levelv = V
        smua.source.output = smua.OUTPUT_ON
        delay(0.2)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.v(smub.nvbuffer1)
        V = V + VinStep
        smua.source.output = smua.OUTPUT_OFF
end

waitcomplete()
-------- END --------