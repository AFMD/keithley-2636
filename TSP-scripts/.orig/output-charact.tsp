reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 700)

-- PARAMETERS
Vdmin = 0
Vdmax = 50
Vdstep = -1

Vgmin = 0
Vgmax = 5
Vgstep = -10


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
smua.source.limiti = 1e-5
smua.measure.rangei = 10e-6
smub.source.limiti = 1e-7
smua.measure.nplc = 1.00

-- MEASUREMENT

display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

for Vg = Vgmin, Vgmax do
    smub.source.levelv = Vg * (Vgstep)
    smua.source.levelv = Vdmin * Vdstep
    delay(20)
    for Vd = Vdmin, Vdmax do
        smua.source.levelv = Vd * Vdstep
        delay(0.4)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.i(smub.nvbuffer1)
    end
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
