# PiNaps Supporting Library

This library provides comprehensive, high level control of the PiNaps Raspberry Pi hat.

## Installation

### Step 1: Install PiNaps Python Library

To install the PiNaps library onto your raspberry pi. There are two methods.

* Use "pip install pinaps" (See [URL])
* Alternatively, clone the repository "git clone https://harri-renney@bitbucket.org/synapsdev/pinaps.git" into your python libs path or a local directory. (See https://harri-renney@bitbucket.org/synapsdev/pinaps)

If you are looking to run the examples straight away, it is best to clone the repository and work from that folder. The pip installs only the library modules, not the examples.

#### Installing I2C separately

If you need to install the I2C driver separately:
* Use "pip install SC16IS750" (See [URL]).
* Alternatively, clone the repository "git clone https://github.com/Harri-Renney/SC16IS750-Python-Driver.git" into your python libs path or pinaps directory. (See https://github.com/Harri-Renney/SC16IS750-Python-Driver)

### Step 2: Prepare raspberry pi

#### Serial Port

* Run raspi-config from command line.

![Serial Step 0](/images/SerialStep0.png)

* Select interfacing options from menu.

![Serial Step 1](/images/SerialStep1.png)

* Select serial from menu.

![Serial Step 2](/images/SerialStep2.png)

* Say no to shell use over serial.

![Serial Step 3](/images/SerialStep3.png)

* Say yes to enabling serial port hardware.

![Serial Step 4](/images/SerialStep4.png)

#### BLE

[Coming soon - When BLE example added]

## Usage

There are two main classes the library provides. The PiNapsController is for controlling the PiNaps hardware. The BlinoParser is used for parsing/processing the data retrieved from the TGAT sensor on the PiNaps.

### PiNapsController

Use the PiNapsController to setup how the PiNaps operates. This includes functions for powering the TGAT and on-board LED, retrieving data from the TGAT over UART or I2C and setting the TGAT operating mode.

### BlinoParser

Use the BlinoParser class to process bytes retrieved from the TGAT sensor into meaningful information. There are two methods for working with the parsed information.

#### Returning Packets
The parseByte function returns the latest packet. It is advisable to check with a conditional that the packet has been updated before using it. This is advised as not every iteration a byte is parsed is new information updated in the packet. Check the object's "updated" member variable.

#### Callbacks
There are a set of callback functions which when defined are executed when the associated information is parsed. Define these to use the information as desired.

#### Getters
Additionally at any time the latest information can be retrieved from the BlinoParser object using getters.

## Examples

### Blinky
This example uses the I2C chip to control the on-board LED. The PiNaps LED is only controled using I2C, therefore not useable with UART.

### Logging
This example demonstrates the data logging functionality to a local log file and prints the debug information to the console.

### Returning Packets
This example demonstrates the use of the returned packets from the parsing function. The function currently returns the latest formed packet every byte passed. First a check is made to discover if the packet has been updated since the last byte was passed.

### Callbacks - Ideal usage
This example demonstrates the definition of the parsers callbacks. In doing this, the user can choose how each piece of information is processed as it is parsed.

### Command Bytes
This example demonstrates how the TGAT mode can be configured using the PiNaps controller functions. In this example the command bytes are controlled by the user using the console to input the desired mode to transition to.

### BlinoPlotter
This example demonstrates a simple graph plot of the EEG data retrieved in real time using the matplotlib pyplot (https://matplotlib.org)
You are required to install matplotlib - Use "pip install matplotlib"

## Additional Notes

### Pip Installing

If you're having trouble using pip install. Try using "python -m pip install --index-url https://pypi.org/simple/ example_pkg"
Where the url is the project url and the example_pkg is the package you wish to install.

### Python Library Path

You might be having a lot of trouble finding where to install the libraries manually. On raspbian it should look something like this:
"usr/local/lib/python2.7/dist-packages"

### Contacting Blino

If you'd like to get in contact with us about the PiNaps Library, especially any bugs you come across - Contact Harri at harri.renney@blino.co.uk