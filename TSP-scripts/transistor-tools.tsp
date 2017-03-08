reset()
display.clear()

-- Beep in excitement, but only once
beeper.enable = beerper.OFF
beeper.beep(2, 2400)

-- CONTACT CHECK
-- Set speed to fast
smua.contact.speed = smua.CONTACT_FAST
-- Set threshold to 10000000 ohms
smua.contact.threshold = 10000000
-- Check contacts against threshold
if not smua.contact.check() then
	-- Set speed to slow
	smua.contact.speed = smua.CONTACT_SLOW
	-- Get aggregate resistance readings
	rhi, rlo = smua.contact.r()
	-- Return contact resistances to the host.
	print (rhi, rlo)
	--terminate execution
	exit()
end
-- CONTACT CHECK FINISHED
	
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
display.screen = display.SMUA
display.smua.measure.func = display.MEASURE_DCAMPS
smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

for V = 1, 100 do
	smub.source.levelv = V * 0.01
	smua.measure.i(smua.nvbuffer1)	
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF

-- Output measurement readings from buffer
printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)
printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)