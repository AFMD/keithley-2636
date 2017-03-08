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
-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1mA
smua.source.limiti = 1e-3
smua.measure.rangei = 1e-3
-- Set Vd
smua.source.levelv = 1.0
--Channel 2 (sweep Vg)
smub.source.func = smub.OUTPUT_DCVOLTS

-- Measurement
smua.source.output = smua.OUTPUT_ON
smub.source.output = smub.OUTPUT_ON

for j = 1, 5 do
	smub.source.levelv = j
	print(smua.measure.i(smua.nvbuffer1))
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF