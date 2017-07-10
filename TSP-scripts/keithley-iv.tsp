--[[

  coordinated sweep on smua and smub of a dual channel 2600B

  generates the Id-Vg curve for a FET

  the smu connected to the drain will not change the voltage value, but will measure
  drain current for each point in the sweep

  the smu connected to the gate will change voltage value for each.  Current measurements
  not needed from this smu.  If we were to enable measurements, they would be very small
  values (gate leakage) and would require appropriate settling time for the low level
  of current.

]]


function configSweep(smu, startv, stopv, points)

-- Configure source and measure settings.
    smu.source.output = smu.OUTPUT_OFF
    smu.source.func = smu.OUTPUT_DCVOLTS
    smu.source.levelv = 0
    smu.source.rangev = math.max(math.abs(startv), math.abs(stopv))

    smu.measure.autozero = smu.AUTOZERO_ONCE
    smu.measure.lowrangei = 100e-9  -- limited auto

    -- Setup a buffer to store the result(s) in and start testing.
    smu.nvbuffer1.clear()
    smu.nvbuffer1.appendmode = 1
    smu.nvbuffer1.collecttimestamps = 1
    smu.nvbuffer1.collectsourcevalues = 1

    -- Reset trigger model
    smu.trigger.arm.stimulus = 0
    smu.trigger.source.stimulus = 0
    smu.trigger.measure.stimulus = 0
    smu.trigger.endpulse.stimulus = 0
    smu.trigger.arm.count = 1
    -- Configure the source action
    smu.trigger.source.linearv(startv, stopv, points)
    smu.trigger.source.action = smu.ENABLE
    smu.trigger.endpulse.action = smu.SOURCE_HOLD
    -- Configure the measure action
    smu.trigger.measure.i(smu.nvbuffer1)
    smu.trigger.measure.action = smu.ENABLE
    -- Configure the sweep count
    smu.trigger.count = points

end  -- function configSweep() definition

--Prints the results from the reading buffers.
function printData_IdVg(drainsmu, gatesmu)
   if drainsmu.nvbuffer1.n == 0 then
      print("No readings in buffer")
   else
      print("Vg\tId")
      for i = 1, drainsmu.nvbuffer1.n do
         print(string.format("%g\t%g", gatesmu.nvbuffer1.sourcevalues[i],
                                           drainsmu.nvbuffer1.readings[i]))
      end
   end
end  -- function printData definition

function start_test(drainsmu, gatesmu)

    -- overwrite some value setup in the configSweep() function
    -- no current measurements on gate, but measure voltage for use in printData()
    gatesmu.trigger.measure.v(gatesmu.nvbuffer1)

    -- gate sources after drain sources the Vds bias
    gatesmu.trigger.source.stimulus = drainsmu.trigger.SOURCE_COMPLETE_EVENT_ID

    -- measure drain current after each gate voltage is sourced
    drainsmu.trigger.measure.stimulus = gatesmu.trigger.SOURCE_COMPLETE_EVENT_ID


    -- output on, run the sweep and then turn the output off.
    drainsmu.source.output = drainsmu.OUTPUT_ON
    gatesmu.source.output = gatesmu.OUTPUT_ON

    -- start the gate first, so that is armed and can detect drain source complete event
    gatesmu.trigger.initiate()
    drainsmu.trigger.initiate()

    waitcomplete()

    drainsmu.source.output = drainsmu.OUTPUT_OFF
    gatesmu.source.output = gatesmu.OUTPUT_OFF

end -- function


-- ******************************************
--
-- main program that calls our functions
--
-- ******************************************

reset()
errorqueue.clear()

drain = smub
gate = smua

sweep_pts = 61
vds_bias = 0.1

--configSweep(smu, startv, stopv, points)
configSweep(drain, vds_bias, vds_bias, sweep_pts)
configSweep(gate, 0, 3, sweep_pts)

start_test(drain, gate)

printData_IdVg(drain, gate)
