reset()
display.clear()

-- Beep in excitement
beeper.beep(0.1, 659.25)
beeper.beep(0.1, 587.33)
beeper.beep(0.2, 349.23)
beeper.beep(0.2, 392.00)
beeper.beep(0.1, 523.25)
beeper.beep(0.1, 493.88)
beeper.beep(0.2, 293.66)
beeper.beep(0.2, 329.63)
beeper.beep(0.1, 493.88)
beeper.beep(0.1, 440.00)
beeper.beep(0.2, 261.63)
beeper.beep(0.2, 329.63)
beeper.beep(0.5, 440.00)

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
smua.source.limiti = 1e-4
smua.measure.rangei = 1e-4
smub.source.limiti = 1e-5
smua.measure.nplc = 10.00

-- Measurement
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

smub.source.output = smua.OUTPUT_ON
smua.source.output = smub.OUTPUT_ON

smua.source.levelv = -10

for Vg = -10, 10 do
    smub.source.levelv = Vg * 5
    delay(0.1)
    smua.measure.i(smua.nvbuffer1)
    smub.measure.i(smub.nvbuffer1)
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
