--[[

   Generate a pulsed Vg-Id curve on FET using nonA version of 2600
  
   Method:  sweep the gate voltage and measure the drain current with voltage bias on drain
  
   Tested with 2602, firmware 1.4.2

]]


reset()
errorqueue.clear()

--display.screen = display.USER

gate = smub
drain = smua

local ton = 25e-3  -- pulse ON time
local toff = 25e-3   -- pulse OFF time
local draincurrentLimit = 10e-6   -- affects the current measure range that will be used
local gatecurrentLimit = 10e-6  -- affects the current measure range that will be used
local startV = 0
local stopV = 10
local npts = 101
local drain_voltage = 10
local gate_voltage = {}

vstep_size = (stopV - startV) / (npts - 1)
--print("step size of voltage sweep: "..vstep_size)

-- build an array of gate voltage values
for i = 1, npts-1 do
  gate_voltage[i] = vstep_size * i
  --print(gate_voltage[i])
end


function config_smu_for_pulse_mode(whichsmu)
    whichsmu.source.autorangev = whichsmu.AUTORANGE_OFF
    whichsmu.source.autorangei = whichsmu.AUTORANGE_OFF
    whichsmu.measure.autorangei = whichsmu.AUTORANGE_OFF
    whichsmu.measure.autorangev = whichsmu.AUTORANGE_OFF
    whichsmu.measure.autozero = whichsmu.AUTOZERO_ONCE
    -- measure time must be less than pulse ON time
    --whichsmu.measure.nplc = (ton - 50e-6) / (1/60)   -- coded for 60Hz power
end


<<<<<<< Updated upstream
-- Beep in excitement
beeper.beep(1, 800)


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


-- Measurement Setup
-- To adjust the delay factor.
smua.measure.delayfactor = 1.0
-- Set Vd
smua.source.levelv = 0.0
--Channel 2 (sweep Vg)
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.levelv = 0.0
-- Channel 1 (source Vd, meas Id)
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
-- Set complaince to 1uA
smua.source.limiti = 1e-5
smua.measure.rangei = 1e-5
smub.source.limiti = 1e-5
smua.measure.nplc = 1.00

-- Measurement
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

smub.source.output = smua.OUTPUT_ON
smua.source.output = smub.OUTPUT_ON

smua.source.levelv = -20
delay(5)

for Vg = -10, 10 do
    smub.source.levelv = Vg * 5
    delay(5)
    smua.measure.i(smua.nvbuffer1)
    smub.measure.i(smub.nvbuffer1)
end
=======
    config_smu_for_pulse_mode(drain)
    config_smu_for_pulse_mode(gate)

    -- set source range for each SMU channel
    gate.source.rangev = math.max(startV, stopV)    
    drain.source.rangev = drain_voltage
    
   
    --[[
    
      if we pass an array of two buffers to the 
      ConfigPulse function, then the SMU will measure both
      current and voltage.
    
    ]]
    -- create buffers to hold both current and voltage
    drain_i = drain.makebuffer(npts)
    drain_v = drain.makebuffer(npts)
    drain_i.appendmode = 1
    drain_v.appendmode = 1
    drain_buffers = { i = drain_i, v = drain_v }  -- an array of buffers
    
    gate_v = gate.makebuffer(npts)
    gate_i = gate.makebuffer(npts)
    gate_v.appendmode = 1
    gate_i.appendmode = 1
    gate_buffers = { i = gate_i, v = gate_v }
    

-- turn the outputs on    
drain.source.output = drain.OUTPUT_ON    
gate.source.output = gate.OUTPUT_ON

print("Gate_V, Gate_I, Drain_I, Drain_V") 
for i = 1, npts-1 do
   f, msg = ConfigPulseVMeasureI(drain,0,drain_voltage,draincurrentLimit,ton,toff,1,drain_buffers,1)
   --print(f, msg)
   f, msg = ConfigPulseVMeasureI(gate,0,gate_voltage[i],gatecurrentLimit,ton,toff,1,gate_buffers,2)
   --print(f, msg)
   --InitiatePulseTest(1)
   f,msg =InitiatePulseTestDual(1,2)
   --print(f, msg)
   waitcomplete()
   print(gate_v[i]..","..gate_i[i]..","..drain_i[i]..","..drain_v[i])
end

drain.source.output = drain.OUTPUT_OFF
gate.source.output = gate.OUTPUT_OFF
>>>>>>> Stashed changes

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
