reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 700)

-- PARAMETERS
Vchan = -0.2

Vgmin = -100
Vgmax = 100
Vgstep = -0.01


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

-- COMPLIANCE
smua.source.limiti = 10e-6
--smua.measure.rangei = 10e-6
smub.source.limiti = 10e-8
smua.measure.nplc = 1.00

-- MEASUREMENT

display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUB

smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

smua.source.levelv = Vchan
smub.source.levelv = Vgmin * (Vgstep)
delay(2)

for Vg = Vgmin, Vgmax do
    smub.source.levelv = Vg * (Vgstep)
    delay(0.2)
    smua.measure.i(smua.nvbuffer1)
    smub.measure.i(smub.nvbuffer1)
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
