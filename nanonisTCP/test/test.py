# %%
# Import all test scripts
from AutoApproachTest import run_test as autoApproachTest
from BiasSpectrTest import run_test as biasSpectrTest
from BiasTest import run_test as biasTest
from CurrentTest import run_test as currentTest
from FolMeTest import run_test as folMeTest
from LockInTest import run_test as lockinTest
from MarksTest import run_test as marksTest
from MotorTest import run_test as motorTest
from Osci2TTest import run_test as osci2TTest
from PiezoTest import run_test as piezoTest
from SafeTipTest import run_test as safeTipTest
from ScanTest import run_test as scanTest
from SignalsTest import run_test as signalsTest
from TipShaperTest import run_test as tipShaperTest
from UserOutTest import run_test as userOutTest
from ZControllerTest import run_test as zControllerTest
from Util import run_test as UtilTest
import time

# %%
# Run test scripts
debug   = False
version = 13520

print("********************************")
print("Testing AutoApproach module...")
result = autoApproachTest(debug=debug, version=version)
if(not result == "success"):
    print("AutoApproach test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing BiasSpectr module...")
result = biasSpectrTest(debug=debug, version=version)
if(not result == "success"):
    print("BiasSpectr test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Bias module...")
result = biasTest(debug=debug, version=version)
if(not result == "success"):
    print("Bias test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Current module...")
result = currentTest(debug=debug, version=version)
if(not result == "success"):
    print("Current test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing FolMe module...")
result = folMeTest(debug=debug, version=version)
if(not result == "success"):
    print("FolMe test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Lockin module...")
result = lockinTest(debug=debug, version=version)
if(not result == "success"):
    print("Lockin test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Marks module...")
result = marksTest(debug=debug, version=version)
if(not result == "success"):
    print("Marks test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Motor module...")
result = motorTest(debug=debug, version=version)
if(not result == "success"):
    print("Motor test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Osci2T module...")
result = osci2TTest(debug=debug, version=version)
if(not result == "success"):
    print("Osci2T test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Piezo module...")
result = piezoTest(debug=debug, version=version)
if(not result == "success"):
    print("Piezo test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing SafeTip module...")
result = safeTipTest(debug=debug, version=version)
if(not result == "success"):
    print("SafeTip test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Scan module...")
result = scanTest(debug=debug, version=version)
if(not result == "success"):
    print("Scan test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Signals module...")
result = signalsTest(debug=debug, version=version)
if(not result == "success"):
    print("Signals test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing TipShaper module...")
result = tipShaperTest(debug=debug, version=version)
if(not result == "success"):
    print("TipShaper test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing UserOut module...")
result = userOutTest(debug=debug, version=version)
if(not result == "success"):
    print("UserOut test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing ZController module...")
result = zControllerTest(debug=debug, version=version)
if(not result == "success"):
    print("ZController test failed")
print(result)
time.sleep(0.5)

print("********************************")
print("Testing Utility module...")
result = UtilTest(debug=debug, version=version)
if(not result == "success"):
    print("Utility test failed")
print(result)
time.sleep(0.5)