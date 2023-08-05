===============
OsensaPlantiga
===============

Python module for interfacing with the OSENSA-Plantiga pods.

*History*
---------

*Release 0.1.5:*

- Update erase function to support fast erase
- Update default SYNC pin state
- Minor tweaks to connect() logic

*Release 0.1.4:*

- Add convert_unixtime() method

*Release 0.1.3:*

- Add method to test clock drift/accuracy

*Release 0.1.2:*

- Add methods to set device into bootloader and to upload new firmware
- Add custom exception to allow return of partially complete flash record read
- Add 1.5Mbaud as a selectable baudrate option
- Other misc bug fixes

*Release 0.1.1:*

- Update API to work with new pod and dock hardware
- Update documentation detailing new pod operation modes and instructions on setting dock serial number
- Fix issue with serial port initialization causing communication issues between pods and docks
- Add methods to get SYNC and RESET pin states
- Revise connect() logic to improve pod detection speed
- Fix bug with minimal modbus library causing errors when compiled
- Add poll() method for continuous monitoring of a single parameter 
- Add speed_test() method for evaluating device read speed
- Add placeholder battery_level() method that returns a hardcoded percentage value (0.98 = 98%)

*Release 0.1.0:*

- Rename release version to fix install error

*Release 0.0.10:*

- Time base in CSV file now based on unix time stamps + interpolation

*Release 0.0.9:*

- Fix bug in minimalmodbus that prevented reconnecting after disconnecting

*Release 0.0.8:*

- Revise Record logic to support new record format that includes record size and data rate
- Revise Record print() and tocsv() logic to include unix timestamp
- Revise save_records() logic to allow option to save headers

*Release 0.0.7:*

- Add modbus CRC check in the read flash command
- Add option to adjust number of flash pages to read at a time
- Update baudrate options to support faster baudrates
- Fix find_docks() support for MacOS
- Increase speed of Pod connection failure detection

*Release 0.0.6:*

- Add logic to handle none type exceptions when finding docks
- Add pyserial and python-dateutil as package dependencies

*Release 0.0.5:*

- Add methods to improve accessibility for connecting to a dock
- Add methods for pod time synchronization

*Release 0.0.4:*

- Add method to read pod firmware version

*Release 0.0.3:*

- Add methods to read and write from device flash
- Add Record class to store 1 page of data from flash
- Add methods to conveniently read disk page and usage
- Add helper methods to convert flash data to a plot, a csv file and to a serial blob

*Release 0.0.2:*

- Add missing modbus library

*Release 0.0.1:*

- Test release