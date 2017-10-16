reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)

-- PARAMETERS

Vdmin = 0
Vdmax = 100
Vdstep  = 1


-- Clear buffers and make sure the right thing is recorded
smua.nvbuffer1.clear()
smua.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smua.measure.count = 1

-- Measurement Setup
-- To adjust the delay factor.
smua.measure.delayfactor = 1.0
-- Set Vd
smua.source.levelv = 0.0
--Channel 2 (sweep Vg)

-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1uA
smua.source.limiti = 10e-6
smua.measure.rangei = 10e-6
smua.measure.nplc = 1.0

-- Measurement
smua.source.levelv = Vdmin * Vdstep
smua.source.output = smua.OUTPUT_ON
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA
delay(2)

for Vd = Vdmin, Vdmax do
        smua.source.levelv = Vd * Vdstep
        delay(0.5)
        smua.measure.i(smua.nvbuffer1)
end
smua.source.output = smua.OUTPUT_OFF
