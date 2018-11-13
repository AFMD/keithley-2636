----------------
-- TSP PROGRAM FOR PERFORMING INVERTER MEASUREMENT
-- Sweeps over an input voltgae range and measures an output voltage


-------- PARAMETERS --------
VinStart = 0
VinEnd = 120
VinStep = 1

DIR = 1

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
smua.source.rangev = 200
-- Compliance here relates to gate leakage?
smua.source.limiti = 1e-7

-- SMUB setup
-- source 0A current and measure voltage
smub.measure.nplc = 10
smub.sense = smub.SENSE_LOCAL
smub.source.func = smub.OUTPUT_DCAMPS
smub.measure.autorangev = smub.AUTORANGE_ON
smub.source.limitv = 150
smub.source.leveli = 0

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCVOLTS
display.smub.measure.func = display.MEASURE_DCVOLTS
display.screen = display.SMUA_SMUB

-- MEASUREMENT ROUTINE
smua.source.levelv = VinStart * VinStep
smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON
delay(30)

for V = VinStart, VinEnd do
        smua.source.levelv = V * VinStep
        delay(2)
        smua.measure.v(smua.nvbuffer1)
        smub.measure.v(smub.nvbuffer1)
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF

waitcomplete()
-------- END --------
