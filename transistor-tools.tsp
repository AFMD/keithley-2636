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
	
