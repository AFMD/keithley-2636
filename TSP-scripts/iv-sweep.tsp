reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)

-- Clear buffers and make sure the right thing is recorded
smua.nvbuffer1.clear()
smua.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smua.measure.count = 1

SweepVLinMeasureI(smua, -1.4, 1, 1E-3, 1000)

