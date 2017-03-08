reset()
display.clear()
srcVoltage = display.prompt("000.00", "V", "Enter source voltage", 5, -20, 20)
measEnable = display.menu("Measurements?", "ENABLE DISABLE")
if measEnable == "ENABLE" then
	numMeas = display.prompt("0000", " Rdgs", "Enter the number of readings", 10, 0, 9999)
	smua.measure.count = numMeas
	smua.nvbuffer.clear()
end
smua.source.levelv = tonumber(srcVoltage)
smua.source.output = smua.OUTPUT_ON
if measEnable == "ENABLE" then
	display.setcusor(1,1)
	display.settext("$BPlease wait.$R$NMeasure operation in progress.")
	smua.measure.i(smua.nvbuffer1)
	display.clear()
	display.settext("Operation Finished$NSource-Measure Complete")
else
	display.settext("Operation Finished$NSource Complete")
end
delay(5)
display.screen = display.SMUA