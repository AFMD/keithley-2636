smua.source.func = smua.OUTPUT_DCVOLTS
smua.source.output = smua.OUTPUT_ON 
for j = 1, 5 do
  smua.source.levelv = j
  currrent = smua.measure.i( )
  print ( current )
end
smua.source.output = smua.OUTPUT_OFF
