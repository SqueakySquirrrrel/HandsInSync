from bluepy import btle
import time
import binascii
import subprocess

print("connecting...")
dev = btle.Peripheral("30:C6:F7:00:1D:2A")

ArduinoNano = btle.UUID("19B10000-E8F2-537E-4F6C-D104768A1214")

ArduinoNanoService = dev.getServiceByUUID(ArduinoNano)

dataChar = btle.UUID("19B10001-E8F2-537E-4F6C-D104768A1214")
dataChannel = ArduinoNanoService.getCharacteristics(dataChar)[0]
ACKChar = btle.UUID("19B10002-E8F2-537E-4F6C-D104768A1214")
ACKChannel = ArduinoNanoService.getCharacteristics(ACKChar)[0]

val = None
while(True):
	if(dataChannel.read() == val):
		continue
	val = dataChannel.read()
	z = str(binascii.b2a_hex(val))
	z = z[8:10]+z[6:8]+z[4:6]+z[2:4]
	print("\nReceived: ", z.lstrip("0"), "\tDecimal value: ", int(z, 16))
	print("Sending ACK for", z.lstrip("0"), "\n")
	for i in range(len(z.lstrip("0"))):
		if (len(z.lstrip("0")) == 0):
			continue
		filename = z.lstrip("0")[i].upper() + ".wav"
		cmd = ['cvlc', filename]
		proc = subprocess.Popen(cmd)
		time.sleep(1)
		proc.terminate()
	#time.sleep(0.5)
	ACKChannel.write(val, withResponse=True)
