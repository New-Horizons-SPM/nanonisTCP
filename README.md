# nanonisTCP
python module for communicating via nanonis TCP protocal. I am actively developing this so if you have any requests or find any bugs, feel free to raise an issue.

### Installing

Clone this repository, navigate to said directory, and run:
```
pip install .
```

### Using

The following code demonstrates how to change tip bias.

```python
from nanonisTCP import nanonisTCP
from nanonisTCP.Bias import Bias

TCP_IP  = '127.0.0.1'               # Local host
TCP_PORT= 6501                      # Check available ports in NANONIS > File > Settings Options > TCP Programming Interface

NTCP = nanonisTCP(TCP_IP, TCP_PORT) # This is how you establish a TCP connection. NTCP is the connection handle.

bias = Bias(NTCP)                   # Nanonis Bias Module - Pass in the connection handle

bias.Set(1.1)                       # Set bias to 1.1 V
v = bias.Get()                      # Get the current bias
print("Bias: " + str(v) + " V")     # Confirm bias has been set

NTCP.close_connection()             # Close the connection.
```

See any of the xxxTest.py scripts to see how each module can be implemented in more detail
