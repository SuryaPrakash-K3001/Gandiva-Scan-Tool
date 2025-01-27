@echo off
echo Please enter the IP address:
set /p ip_address=

echo Please enter the start port:
set /p start_port=

echo Please enter the end port:
set /p end_port=

echo Please enter the output file name:
set /p output_file=

start port_scanner.exe %ip_address% %start_port% %end_port% --report %output_file%

pause

