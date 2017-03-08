# transistor_tools_K2636
For the electrical characterisation of OFETS using a keithley 2636.
The K2636.py script in this folder loads a set of .tsp instructions into the memory of the Keithley. It then tells the keithley to execute the script before closing connection with the instrument. Run as follows:

>>python3 K2636.py example.tsp

# requires:
- PyVisa
- PyVisa-py

# Things to note
- The Keithley 2636 uses 'TSP' rather than the much-loved 'SCPI' which the Keithley 2400 understood.
- Other than the change in syntax, the way the commands are executed have changed. Now the Keithley now loads an entire script's worth of commands into it's non-volatile memory before execution. This means it's faster than before (thank god).
- The .tsp files in this repo are scripts which can be loaded into the K2636.
- .tsp are written in Lua (http://www.lua.org). Comments begin with '--'
- For more info on TSP check out the following links:
	- http://www.tek.com/sites/tek.com/files/media/document/resources/2616%20SCPI_to_TSP_AN.pdf
	- https://forum.tek.com/viewtopic.php?t=121440