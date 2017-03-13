reset()
display.clear()

-- Beep in excitement, but only once
beeper.beep(0.2, 200)
beeper.beep(0.2, 600)
beeper.beep(0.5, 1200)
	
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
-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1mA
smua.source.limiti = 1e-3
smua.measure.rangei = 1e-3
smua.measure.nplc = 10.00
-- Set Vd
smua.source.levelv = 0.0
--Channel 2 (sweep Vg)
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.levelv = 0.0

-- Measurement
display.screen = display.SMUB
smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

for V = 1, 50 do
	smub.source.levelv = V * 0.01
	delay(0.2)
	smua.measure.i(smua.nvbuffer1)
	smub.measure.v(smub.nvbuffer1)
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
