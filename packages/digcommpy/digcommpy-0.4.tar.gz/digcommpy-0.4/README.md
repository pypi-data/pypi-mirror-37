# DigCommPy
Python3 package for digital communications simulations.

It includes channel coding and different channel models. Simulations can be run
to calculate bit/block error rates for different configurations.


# Installation
The package can be installed using pip with the command `pip install
digcommpy`.

Alternatively, you can clone the Gitlab repository and install the local copy
using the following commands:

    git clone https://gitlab.com/klb2/digcommpy.git
	cd digcommpy
	pip install .


# Usage
There are multiple example files in the `examples` folder.

## Basic Encoding/Decoding Example
A simple encoding example using a polar code:

    from digcommpy import messages, encoders
	n, k = 16, 4
    encoder = encoders.PolarEncoder(n, k, "BAWGN", 0.)
	mess = messages.generate_data(k, number=1000, binary=True)
	codewords = encoder.encode_messages(mess)

A full transmission chain can be simulated as follows:

    from digcommpy import messages, encoders, decoders, channels, modulators, metrics
	# Parameters
	n, k = 16, 4
	snr = 5.  # dB
	# Blocks
	encoder = encoders.PolarEncoder(n, k, "BAWGN", snr)
	modulator = modulator.BpskModulator()
	channel = channels.BawgnChannel(snr, rate=k/n)
	decoder = decoders.PolarDecoder(n, k, "BAWGN", snr)
	# Simulation
	mess = messages.generate_data(k, number=1000, binary=True)
	codewords = encoder.encode_messages(mess)
	channel_input = modulator.modulate_symbols(codewords)
	channel_output = channel.transmit_data(channel_input)
	est_mess = decoder.decode_messages(channel_output)
	ber = metrics.ber(mess, est_mess)
	print("The BER is {}".format(ber))

This can be simplified by using the `simulations` module from the
package (in progress).


# Used Software
Some parts of this library are based on different open source implementations.
The polar code encoding and decoding code is based on the Matlab implementation
from Harish Vangala et al. (http://polarcodes.com/).
