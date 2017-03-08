reset()
-- Clear the display
display.clear()

-- Prompt the user for a voltage value to source
srcVoltage = display.prompt("000.00", "V", "Enter source voltage", 5, -20, 20)

-- Prompt the user to enable measurements
measEnable = display.menu("Measurements?", "ENABLE DISABLE")
if measEnable == "ENABLE" then
	numMeas = display.prompt("0000", " Rdgs", "Enter the number of readings", 10, 0, 9999)
	smua.measure.count = numMeas
	smua.nvbuffer.clear()
end

-- Convert user input to the source level.
smua.source.levelv = tonumber(srcVoltage)
smua.source.output = smua.OUTPUT_ON

if measEnable == "ENABLE" then
	-- Inform the user that measurements are in progress
	display.setcusor(1,1)
	display.settext("$BPlease wait.$R$NMeasure operation in progress.")
	smua.measure.i(smua.nvbuffer)
	display.clear()
	-- Inform the user that the Source Measure operation has finished
	display.settext("Operation Finished$NSource-Measure Complete")
else
	-- Inform the user that the Source operation has finished
	display.settext("Operation Finished$NSource Complete")
end

-- Wait 5 seconds then return to the main screen.
delay(5)
display.screen = display.SMUA