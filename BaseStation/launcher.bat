@echo OFF

start call serial.bat

timeout 5
java -jar gui.jar
timeout 5
