from .D4_constants import *
from .chip_mode import AD7175_MODE, AD7175_SPEED

class D4_module(object):
    def __init__(self, spi_rack, module):
        # Set module and chip number for Chip Select
        self.module = module
        # Give the spi_rack object to use
        self.spi_rack = spi_rack
        self.mode = 0
        self.filter_val = 16
        self.buf_en = 1
        # Setup the ADC with standard values
        self.setup_ADC()

    def setup_ADC(self):
        # For both ADC chips (ADC=0 and ADC=1)
        for ADC in range(0,2):
            # Disable internal reference and single conversion
            # Extra: single cycle
            self.write_data(ADC, MODE_REG, 0<<REF_EN | self.mode<<MODE | 1<<SING_CYC)
            #
            self.write_data(ADC, IFMODE, 1<<DOUT_RESET)
            # Set config reg 0 to binary coded offset
        	# Set input buffers enabled, reference buffers disabled, external reference
            self.write_data(ADC, CONFIG_REG, (1<<BI_UNIPOLAR) | (0b00<<REF_SEL) | (self.buf_en<<AINBUF0P) | (self.buf_en<<AINBUF0M) )
            # Set CH1, Enable, setup0, meas diff between AIN2 and AIN3
            self.write_data(ADC, CH1_REG, (1<<CH_EN) | (0b000<<SETUP_SEL) | (AIN0<<AINPOS) | (AIN4<<AINNEG))
            # Set CH2/3/4, Disable, setup0, AINx - AIN4
            self.write_data(ADC, CH2_REG, (0<<CH_EN) | (0b000<<SETUP_SEL) | (AIN1<<AINPOS) | (AIN4<<AINNEG))
            self.write_data(ADC, CH3_REG, (0<<CH_EN) | (0b000<<SETUP_SEL) | (AIN2<<AINPOS) | (AIN4<<AINNEG))
            self.write_data(ADC, CH4_REG, (0<<CH_EN) | (0b000<<SETUP_SEL) | (AIN3<<AINPOS) | (AIN4<<AINNEG))
            # Filter: sinc3 at 50Hz output rate, 12.8 Hz -3dB point: 60 ms settling
            self.write_data(ADC, FILTER_REG, (0b11<<ORDER0) | (self.filter_val<<ODR))

    def write_data(self, ADC, reg, data):
        """
        Write given data to register of the given ADC
        """
        s_data = bytearray([reg, data>>8, data & 0xFF])
        self.spi_rack.write_data(self.module, ADC, AD7175_MODE, AD7175_SPEED, s_data)

    def read_data(self, ADC, reg, no_bytes):
        """
        Read a given number of bytes (no_bytes) from given ADC register
        """

        s_data = bytearray([ reg | (1<<6)] + no_bytes*[0])
        r_i_data = self.spi_rack.read_data(self.module, ADC, AD7175_MODE, AD7175_SPEED, s_data)

        return r_i_data

    def singleConversion(self, ADC):
        """
        Start one conversion and keep waiting until conversion is done
        Give back calculated voltage
        """
        if self.mode == 1:
            self.write_data(ADC, MODE_REG, 0<<REF_EN | 1<<MODE | 1<<SING_CYC)
        else:
            self.write_data(ADC, FILTER_REG, (0b11<<ORDER0) | (self.filter_val<<ODR))
        while(True):
            #time.sleep(0.05)
            status = self.read_data(ADC, STATUS_REG, 1)
            #print("Status: " + str(status[0]))

            # if new data available:
            if (status[0]&(1<<7)) == 0:
                # Get raw data, shift to correct place and convert to voltage
                raw_data = self.read_data(ADC, DATA_REG, 3)
                raw_data = raw_data[1:]
                raw_data_val = raw_data[0] << 16 | raw_data[1] << 8 | raw_data[2]
                #print("Raw data: " + str(bin(raw_data_val)))
                # For differential, use 10 Volt instead of 5 Volt
                return (5.0/(2**24)*raw_data_val) - 2.5
                #return (10.0/(2**24)*raw_data_val) - 5;

class AD7175_registers:
    # ADC register locations
    STATUS_REG = 0x00
    ADCMODE_REG = 0x01
    IFMODE_REG = 0x02
    REGCHECK_REG = 0x03
    DATA_REG = 0x04
    GPIOCON_REG = 0x06
    ID_REG = 0x07
    CH0_REG = 0x10
    CH1_REG = 0x11
    CH2_REG = 0x12
    CH3_REG = 0x13
    SETUPCON0_REG = 0x20
    SETUPCON1_REG = 0x21
    SETUPCON2_REG = 0x22
    SETUPCON3_REG = 0x23
    FILTCON0_REG = 0x28
    FILTCON1_REG = 0x28
    FILTCON2_REG = 0x28
    FILTCON3_REG = 0x28
    OFFSET0_REG = 0x30
    OFFSET1_REG = 0x30
    OFFSET2_REG = 0x30
    OFFSET3_REG = 0x30
    GAIN0_REG = 0x38
    GAIN1_REG = 0x38
    GAIN2_REG = 0x38
    GAIN3_REG = 0x38

    # Status Register bits
    nRDY = 7
    ADC_ERROR = 6
    CRC_ERROR = 5
    REG_ERROR = 4
    CHANNEL = 0

    # ADC Mode Register bits
    REF_EN = 15
    HIDE_DELAY = 14
    SING_CYC = 13
    DELAY = 8
    MODE = 4
    CLOCKSEL = 2

    # IFMODE Register bits
    ALT_SYNC = 12
    IOSTRENGTH = 11
    DOUT_RESET = 8
    CONTREAD = 7
    DATA_STAT = 6
    REG_CHECK = 5
    CRC_EN = 2
    WL16 = 0

    # GPIOCON Register bits
    MUX_IO = 12
    SYNC_EN = 11
    ERR_EN = 9
    ERR_DAT = 8
    IP_EN1 = 5
    IP_EN0 = 4
    OP_EN1 = 3
    OP_EN0 = 2
    GP_DATA1 = 1
    GP_DATA0 = 0

    # Channel Registers bits
    CH_EN = 15
    SETUP_SEL = 12
    AINPOS = 5
    AINNEG = 0

    # Setup Configuration Register bits
    BI_UNIPOLAR = 12
    REFBUF0P = 11
    REFBUF0M = 10
    AINBUF0P = 9
    AINBUF0M = 8
    REF_SEL = 4

    # Filter Configuration Register bits
    SINC3_MAP0 = 15
    ENHFILTEN = 11
    ENHFILT = 8
    ORDER0 = 5
    ODR = 0

    # ADC register values
    AIN0 = 0
    AIN1 = 1
    AIN2 = 2
    AIN3 = 3
    AIN4 = 4
    REFP = 21
    REFN = 22
