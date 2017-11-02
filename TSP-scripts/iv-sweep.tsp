reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)


-- TRANSFER CHARACTERISTICS
-- Clear buffers and make sure the right thing is recorded
smua.nvbuffer1.clear()
smub.nvbuffer1.clear()
smua.nvbuffer1.collectsourcevalues = 1
smub.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smub.nvbuffer1.appendmode = 1
smua.measure.count = 1
smub.measure.count = 1


-- Measurement Setup
-- To adjust the delay factor.
smua.measure.delayfactor = 1.0
-- Set Vd
smua.source.levelv = 0.0
--Channel 2 (sweep Vg)
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.levelv = 0.0
-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1uA
smua.source.limiti = 1e-6
smua.measure.rangei = 1e-6
smub.source.limiti = 1e-7
smua.measure.nplc = 1.0

-- Measurement
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

<<<<<<< Updated upstream
smua.source.output = smub.OUTPUT_ON
smua.source.levelv = -50
delay(5)
=======
-- Set display
display.screen = display.SMUA

-- Sweep (channel, start V, end V, settling time, points)
SweepVLinMeasureI(smua, -50, 50, 1E-3, 1000)
>>>>>>> Stashed changes

for Vd = -500, 500 do
        smua.source.levelv = Vd * (0.1)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.v(smub.nvbuffer1)
        delay(0.1)
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
