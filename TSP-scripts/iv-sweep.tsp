----------------
-- TSP PROGRAM FOR PERFORMING IV SWEEP
-- Sweeps over an input voltgae range and measures an output current.

-- INPUT sweep start, sweep end, and absolute step size.


-------- PARAMETERS --------
Vstart = -50
Vend = 50
Vstep = 2


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

-- Measurement Setup
-- To adjust the delay factor.
smua.measure.delayfactor = 1
smua.measure.nplc = 10
-- SMUA setup
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti = 1e-5
smua.measure.rangei = 1e-5

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

-- Measurement routine
V = Vstart
smua.source.output = smua.OUTPUT_ON
smua.source.levelv = V
delay(1)

-- forwards scan direction
if Vstart < Vend then
    while V <= Vend do
            smua.source.levelv = V
            smua.source.output = smua.OUTPUT_ON
            delay(0.2)
            smua.measure.i(smua.nvbuffer1)
            V = V + Vstep
            smua.source.output = smua.OUTPUT_OFF
    end

-- reverse scan direction
elseif Vstart > Vend then
    while V >= Vend do
            smua.source.levelv = V
            smua.source.output = smua.OUTPUT_ON
            delay(0.2)
            smua.measure.i(smua.nvbuffer1)
            V = V - Vstep
            smua.source.output = smua.OUTPUT_OFF
    end

else
    error("Invalid sweep parameters.")
end

waitcomplete()
-------- END --------
