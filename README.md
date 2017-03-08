# transistor_tools_K2636
For the electrical characterisation of OFETS using a keithley 2636

# Things to note
- The Keithley 2636 uses 'TSP' rather than the much-loved 'SCPI' which the Keithley 2400 understood. To read more about this change please see the following links:
-- http://www.tek.com/sites/tek.com/files/media/document/resources/2616%20SCPI_to_TSP_AN.pdf
-- https://forum.tek.com/viewtopic.php?t=121440
- Other than the change in syntax, the way the commands are executed have changed. Now the Keithley now loads an entire script's worth of commands into it's non-volatile memory before execution. This means it's faster than before (thank god).
- The .tsp files in this repo are scripts which can be loaded into the K2636.