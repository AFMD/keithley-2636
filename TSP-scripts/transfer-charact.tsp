reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 800)

-- PARAMETERS
Vchan = 0.1
Vgmin = 0
Vgmax = 10
Vgstep = 3
setTime = 60

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

-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1uA
smua.source.limiti = 10e-6
smua.measure.rangei = 10e-6
smub.source.limiti = 10e-9
smua.measure.nplc = 1.00

-- Measurement
smua.source.levelv = 0.0
smub.source.levelv = 0.0
smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

--Discharge gate dielectric
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUB
smub.source.limiti = 1e-6
smua.source.levelv = 0.0
smub.source.levelv = 0.0
delay(10)
smub.source.limiti = 10e-9

-- Measure with increasing gate
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUB
smua.source.levelv = Vchan
for Vg = Vgmin, Vgmax do
    smub.source.levelv = Vg * Vgstep
    delay(setTime)
    smua.measure.i(smua.nvbuffer1)
    smub.measure.i(smub.nvbuffer1)
end

--Discharge gate dielectric
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUB
smub.source.limiti = 1e-6
smua.source.levelv = 0.0
smub.source.levelv = 0.0
delay(120)
smub.source.limiti = 10e-9

-- Measure with decreasing gate
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUB
smua.source.levelv = Vchan
for Vg = Vgmin, Vgmax do
    smub.source.levelv = (-1) * Vg * Vgstep
    delay(setTime)
    smua.measure.i(smua.nvbuffer1)
    smub.measure.i(smub.nvbuffer1)
end

--Discharge gate dielectric
smub.source.limiti = 1e-6
smua.source.levelv = 0.0
smub.source.levelv = 0.0
delay(10)
smub.source.limiti = 10e-9


smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
