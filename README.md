[![DOI](https://zenodo.org/badge/475187257.svg)](https://zenodo.org/badge/latestdoi/475187257)
# nanonisTCP
Python module for communicating to nanonis via TCP. I am actively developing this so if you have any requests or find any bugs, feel free to raise an issue.

### Installing

Install with pip:
```pip install nanonisTCP```

Installing from source:
Clone the repository, navigate to the root directory and run ```pip install .```

### Using

The following code demonstrates how to change tip bias.

```python
from nanonisTCP import nanonisTCP
from nanonisTCP.Bias import Bias

TCP_IP  = '127.0.0.1'                               # Local host
TCP_PORT= 6501                                      # Check available ports in NANONIS > File > Settings Options > TCP Programming Interface

NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=13520)  # This is how you establish a TCP connection. NTCP is the connection handle.
                                                    # Check your nanonis version in Nanonis > help > info and enter the RT Engine number

bias = Bias(NTCP)                                   # Nanonis Bias Module - Pass in the connection handle

bias.Set(1.1)                                       # Set bias to 1.1 V
v = bias.Get()                                      # Get the current bias
print("Bias: " + str(v) + " V")                     # Confirm bias has been set

NTCP.close_connection()                             # Close the connection.
```

See any of the xxxTest.py scripts to see how each module can be implemented in more detail.

### Testing
After installing, you can test any of the modules using the sctipts in the test folder.
To test all of the modules, run test.py
<strong>Note that Nanonis must be open for the tests to pass.</strong>

### Citing
If you use nanonisTCP, please consider citing it: [10.5281/zenodo.7402664](https://doi.org/10.5281/zenodo.7402664)
