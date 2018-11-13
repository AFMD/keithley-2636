----------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current

-- INPUT sweep start and end points with ABSOLUTE step size


-------- PARAMETERS --------
Vchan = -50

VgStart = 100
VgEnd = -100
VgStep = 1


-------- MAIN PROGRAM --------
reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)

-- Clear buffers
smua.nvbuffer1.clear()
smub.nvbuffer1.clear()
-- Prepare buffers
smua.nvbuffer1.collectsourcevalues = 1
smub.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smub.nvbuffer1.appendmode = 1
smua.measure.count = 1
smub.measure.count = 1

-- SMUA setup
smua.measure.delayfactor = 1.0
smua.measure.nplc = 10
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti = 10e-5
smua.measure.rangei = 10e-5

-- SMUB setup
smub.measure.delayfactor = 1.0
smub.measure.nplc = 10
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti = 10e-8

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA_SMUB

-- MEASUREMENT ROUTINE

smua.source.levelv = Vchan
smua.source.output = smua.OUTPUT_ON

Vg = VgStart
smub.source.levelv = Vg
smub.source.output = smub.OUTPUT_ON
delay(3)

-- Forward Vg scan
if VgStart < VgEnd then
    while Vg <= VgEnd do
        smub.source.levelv = Vg
        smub.source.output = smub.OUTPUT_ON
        delay(0.2)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.i(smub.nvbuffer1)

        smub.source.output = smub.OUTPUT_OFF
        Vg = Vg + VgStep
    end

-- Reverse scan
elseif VgStart > VgEnd then
    while Vg >= VgEnd do
        smub.source.levelv = Vg
        smub.source.output = smub.OUTPUT_ON
        delay(0.2)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.i(smub.nvbuffer1)

        smub.source.output = smub.OUTPUT_OFF
        Vg = Vg - VgStep
    end

else
    error("Invalid sweep parameters.")
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
waitcomplete()

beeper.beep(1, 600)
beeper.beep(1, 600)
beeper.beep(1, 600)
beeper.beep(1, 600)
-------- END --------
