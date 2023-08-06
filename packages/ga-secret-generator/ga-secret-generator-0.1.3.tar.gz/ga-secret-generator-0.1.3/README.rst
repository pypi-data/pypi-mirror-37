###################
ga-secret-generator
###################

ga-secret-generator is a small tool for generating totp secrets for use with
google authenticator.


************
Installation
************

.. code-block:: text

   pip install ga-secret-generator

ga-secret-generator relies on python 3, so on some system you'll need to
replace pip with pip3


*****
Usage
*****

.. code-block:: text

    usage: ga-secret-generator [-h] [-n] [-o OUTPUT_FILE] [-s SECRET] keyname

    generates google authenticator totp secret as text and optionally as QR code

    positional arguments:
      keyname               keyname, as displayed in google authenticator

    optional arguments:
      -h, --help            show this help message and exit
      -n, --no-qr           omit generating a QR code image
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            where to store the QR code image (default: qr-
                            code.png)
      -s SECRET, --secret SECRET
                            use existing secret instead of generating one
