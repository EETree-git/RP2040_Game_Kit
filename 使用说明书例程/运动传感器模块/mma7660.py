class MMA7660:
	"""
	Interface to the MMA7660FC 3 axis accelerometer of the pyboard
	"""
	
	X_REG = 0             # x axis acceleration register (RO)
	Y_REG = 1             # y axis acceleration register (RO)
	Z_REG = 2             # z axis acceleration register (RO)
	TILT_REG = 3          # tilt register (RO)
	SAMPLE_STAT_REG = 4   # sample rate status register (RO)
	SLEEP_COUNT_REG = 5   # sleep count register (RW)
	INT_REG = 6           # interrupt setup register (RW)
	MODE_REG = 7          # mode register (RW)
	SAMPLING_REG = 8      # sampling rates register
	TAP_REG = 9           # tap detection register
	TAP_DEBOUNCE_REG = 10 # tap debounce counter
	
	# Tilt status register
	SHAKE = 0b10000000 # shake in x, y or z direction
	ALERT = 0b01000000 # register was read during update of its value
	TAP   = 0b00100000 # tap detected
	POLA  = 0b00011100 # landscape or vertical orientation
	BAFRO = 0b00000011 # front/back orientation

	# Sample rate status register
	AWSRS = 0b00000010 # active sampling in auto wake mode
	AMSRS = 0b00000001 # active sampling in active mode
	
	# Interrupt setup register
	SHINTX = 0b10000000 # interrupt when shaken along x axis
	SHINTY = 0b01000000 # interrupt when shaken along y axis
	SHINTZ = 0b00100000 # interrupt when shaken along z axis
	GINT   = 0b00010000 # interrupt when a measurement is made
	ASINT  = 0b00001000 # interrupt when exiting auto-sleep
	PDINT  = 0b00000100 # interrupt when a tap is detected
	PLINT  = 0b00000010 # interrupt when up/down/right/left position change
	FBINT  = 0b00000001 # interrupt when font/back position change
	
	# Mode register
	IAH  = 0b10000000 # interrupt output active low (0) or high (1)
	IPP  = 0b01000000 # interrupt output open-drain (0) or push-pull (1)
	SCPS = 0b00100000 # sleep counter counts in samples (0) or by 16 samples (1)
	ASE  = 0b00010000 # auto-sleep disabled (0) or enabled (1)
	AWE  = 0b00001000 # auto-wake disabled (0) or enabled (1)
	TON  = 0b00000100 # test mode enabled (1, with MODE = 0) or disabled (0)
	MODE = 0b00000001 # standby mode (0) or active mode (1)
	
	# Sampling rate register
	FILT = 0b11100000 # Tilt debounce filtering: 000 = disable, 111 = match 8 measurements
	AWSR = 0b00011000 # Auto-wake mode sampling rate: 00 = 32Hz, 11 = 1Hz
	AMSR = 0b00000111 # Active and auto-sleep mode sampling rate: 000 = 120Hz, 001 = 64Hz, 111 = 1Hz
	
	# Active and auto-sleep mode sampling rates (AMSR field)
	AMPD = 0b000 # 120 samples per second
	AM64 = 0b001 # 64 samples per second
	AM32 = 0b010 # 32 samples per second
	AM16 = 0b011 # 16 samples per second
	AM8  = 0b100 # 8 samples per second
	AM4  = 0b101 # 4 samples per second
	AM2  = 0b110 # 2 samples per second
	AM1  = 0b111 # 1 sample per second
	
	# Auto-wake sampling rates (AWSR field)
	AW32 = 0b00 # 32 samples per second
	AW16 = 0b01 # 16 samples per second
	AW8  = 0b10 # 8 samples per second
	AW1  = 0b11 # 1 sample per second
	
	# Tilt debounce filtering modes
	FILT0 = 0b000 # No filtering
	FILT2 = 0b001 # filter over 2 samples
	FILT3 = 0b010 # filter over 3 samples
	FILT4 = 0b011 # filter over 4 samples
	FILT5 = 0b100 # filter over 5 samples
	FILT6 = 0b101 # filter over 6 samples
	FILT7 = 0b110 # filter over 7 samples
	FILT8 = 0b111 # filter over 8 samples
	
	# Tap detection
	ZDA  = 0b10000000 # enable tap detection on z axis
	YDA  = 0b01000000 # enable tap detection on y axis
	XDA  = 0b00100000 # enable tap detection on x axis
	PDTH = 0b00011111 # tap detection threshold (1 to 31 counts)
	
	"""
	Initialize a new instance of the accelerometer interface.
	The accelerometer is found by comparing the devices on the I2C bus
	when the MMA chip is powered and when it is not powered.
	The device is then put in standby mode.
	"""
	def __init__(self, i2c):
            self.i2c = i2c
	    devices = self.i2c.scan()             # get devices on I2C bus

            self.address = None
	    for dev in devices:
                if dev == 0x4c:
		    self.address = dev
            
	    if self.address == None:
		raise RuntimeError("No MMA7660 accelerometer found on I2C bus 1")
            
            self.buf = bytearray(1)     # 1-byte buffer for I2C communications
            self.on(False)              # Put it in standby mode
	
	"""
	Get the address of the MMA7660 device on the I2C bus
	"""
	def getAddress(self):
		return self.address
	
	"""
	Set a bit in a register of the device.
	Params:
	* reg is the register address
	* bit is the mask of the bit to set
	"""
	def setBit(self, reg, bit):
		self.i2c.readfrom_mem_into(self.address, reg, self.buf)  # get previous register value
		self.buf[0] |= bit                              # set bit to 1
		self.i2c.writeto_mem(self.address, reg, self.buf) # write new value
        
	"""
	Clear a bit in a register of the device.
	Params:
	* reg is the register address
	* bit is the mask of the bit to clear
	"""
	def clearBit(self, reg, bit):
		self.i2c.readfrom_mem_into(self.address, reg, self.buf)  # get previous register value
		self.buf[0] &= ~bit                             # clear bit
		self.i2c.writeto_mem(self.address, reg, self.buf) # write new value

	"""
	Put the MMA7660 in active or standby mode.
	Params:
	* on: True for active mode, False for standby mode
	"""
	def on(self, on=True):
		if on:
			self.setBit(MMA7660.MODE_REG, MMA7660.MODE)
		else:
			self.clearBit(MMA7660.MODE_REG, MMA7660.MODE)
	
	"""
	Tell whether the MMA7660 is in active mode.
	"""
	def isOn(self):
		mode = self.i2c.readfrom_mem(self.address, MMA7660.MODE_REG, 1)
		return not ((mode[0] & MMA7660.MODE) == 0)
	
	"""
	Get a sample a data from the MMA7660.
	Params:
	* data: a bytearray of length 3
	data[0] will contain the 6-bit value of the acceleration along the x axis in 2's complement
	data[1] will contain the 6-bit value of the acceleration along the y axis in 2's complement
	data[2] will contain the 6-bit value of the acceleration along the z axis in 2's complement
	"""
	def getSample(self, data):
		self.i2c.readfrom_mem_into(self.address, MMA7660.X_REG, data)  # read sample
		for i in range(3):
			data[i] &= 0x3F       # clip values to 6 bits
	
	"""
	Set the sampling rate of the accelerometer in active mode.
	Params:
	* rate: one of AMPD, AM64, ..., AM2, AM1
	"""
	def setActiveSamplingRate(self, rate):
		self.i2c.mem_read(self.buf, self.address, MMA7660.SAMPLING_REG)
		r = rate & MMA7660.AMSR  # clip value to field width
		self.buf[0] = (self.buf[0] & (~MMA7660.AMSR)) | r
		was_on = self.isOn()     # save previous mode of MMA7660
		self.on(False)           # put in standby mode to change register value
		self.i2c.writeto_mem(self.address, MMA7660.SAMPLING_REG, self.buf)
		self.on(was_on)          # restore previous mode
	
	"""
	Set the mask of enabled interrupts.
	Params:
	* mask: any combination of SHINTX, SHINTY, ..., PLINT, FBINT
	"""
	def enableInterrupt(self, mask):
		was_on = self.isOn()  # save current mode
		self.on(False)        # put in standby mode to write register
		self.i2c.writeto_mem(self.address, MMA7660.INT_REG, mask)
		self.on(was_on)       # restore previous mode
	
	"""
	Set the interrupt handler for MMA7660 interrupts.
	Params:
	* handler: a function taking a pyb.ExtInt object as parameter, or None
	"""
	def setInterruptHandler(self, handler):
		mma_int_pin = pyb.Pin('MMA_INT')  # interrupt pin of the MMA7660
		# Note: we assume that the INT pin is active low and is open drain
		# Firstly, remove the previous interrupt handler
		extint = pyb.ExtInt(mma_int_pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
		# Then, if a handler is given, register it
		if handler != None:
		  extint = pyb.ExtInt(mma_int_pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, handler)
		return extint
