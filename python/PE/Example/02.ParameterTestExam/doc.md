# ParameterTestExam

Notification before use
-------------------------------------------------------
Depending on the type of product you are using, the definitions of 'Parameter', 'IO Logic', 'AxisStatus', etc. may be different.
This example is based on 'Ezi-SERVO2', so please apply the appropriate value depending on the product you are using.

```
Example)

FM_EZISERVO2_PARAM			// Parameter enum when using 'Ezi-SERVO2'
FM_EZIMOTIONLINK2_PARAM		// Parameter enum when using 'Ezi-MOTIONLINK2'
```
[EN]    
This example code is implemented to run on Python 3.x and later.
If you use version 3.0 or less, you need to change the print and input functions.

[KR]  
이 예제코드는 파이썬 3.x이상에서 동작하도록 구현되어있습니다.
3.0이하 버전에서 사용하실경우 print, input함수의 변형이 필요합니다.

## 0. Program scenario
[EN]  
1. Connect a device.
2. Get parameter information.
3. Configure parameters.
4. Close connection.

[KR]  
1. 장치 연결.
2. 파라미터 확인.
3. 파라미터 변경.
4. 연결 해제.

## 1. Setting the Path
```python
import sys
import os
import platform
try:
    include_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
except NameError:
    include_path = os.path.abspath(
        os.path.join(os.getcwd(), "..")
    )

arch = platform.architecture()[0]
if arch == '64bit':
    library_path = os.path.join(include_path, "Include_Python_x64")
else:
    library_path = os.path.join(include_path, "Include_Python")

sys.path.append(library_path)
```
[EN]    
This code adds the appropriate Library folder path according to the Python architecture to import FAS_EziMOTIONPlusE, MOTION_DEFINE, and ReturnCodes_Define modules.
If the Library folder is in a different path, enter that path in Library_path.

[KR]  
FAS_EziMOTIONPlusE, MOTION_DEFINE, ReturnCodes_Define 모듈들을 Import 하기 위하여 파이썬 아키텍쳐에 따라 알맞은 Library 폴더 경로를 추가하는 코드입니다.
Library 폴더가 다른 경로에 있는 경우, library_path에 해당 경로를 입력해 주시기 바랍니다.

## 2. Get parameter
```python
# Check The Axis Start Speed Parameter Status
status_result, lParamVal = FAS_GetParameter(nBdID, SERVO2_AXISSTARTSPEED)
if status_result != FMM_OK:
    print("Function(FAS_GetParameter) was failed.")
    return False
else:
    print("Load Parameter[Before] : Start Speed = %d[pps]" % lParamVal)
```
[EN]  
You can check the parameter value using the 'FAS_GetParameter' function.

[KR]  
'FAS_GetParameter' 함수를 사용하여 현재 설정된 파라미터의 값을 확인할 수 있습니다.

### 2.1 Parameter No.
[EN]  
'SERVO2_AXISSTARTSPEED' is the parameter number. It is defined in the 'MOTION_SERVO2_DEFINE.py' file.

You can check the the parameter number in the define file of the corresponding model (for example, 'MOTION_SERVO2_DEFINE.py' for the Ezi-SERVOII Plus-E model).
Or, refer to the Parameter List of the Ezi-MOTION Plus-E program.

[KR]  
'SERVO2_AXISSTARTSPEED'는 파라미터 번호입니다. 이것은 'MOTION_SERVO2_DEFINE.py' 파일에 정의되어 있습니다.

설정하고자 하는 파라미터의 번호는 해당하는 모델의 define 파일(예를 들어 Ezi-SERVOII Plus-E 모델의 경우 'MOTION_SERVO2_DEFINE.py')에서 확인하실 수 있습니다.
혹은, Ezi-MOTION Plus-E 프로그램의 Parameter List 화면에 표시되는 번호를 참고하시기 바랍니다.

## 3. Set parameter
```python
nChangeValue = 100

# Change the (Axis Start Speed Parameter) value to (nChangeValue) value.
status_result = FAS_SetParameter(nBdID, SERVO2_AXISSTARTSPEED, nChangeValue)
if status_result != FMM_OK:
    print("Function(FAS_SetParameter) was failed.")
    return False
else:
    print("Set Parameter: Start Speed = %d[pps]" % nChangeValue)
```
[EN]  
You can change the parameter value using the 'FAS_SetParameter' function.
The parameter value takes effect immediately after it is set.

[KR]  
'FAS_SetParameter' 함수를 사용하여 파라미터의 값을 변경할 수 있습니다.
파라미터의 값은 설정하는 즉시 적용됩니다.

### 3.1 Return value
[EN]  
The return value of the 'FAS_SetParameter' function, nRtn indicates the success or failure of the function (and the cause of the failure).

If the function is executed normally without any problems, 'FMM_OK' is returned.

If a value other than 'FMM_OK' is received, it indicates that the function was not executed normally.
For examples, 'FMC_TIMEOUT_ERROR' indicates that no response was received from the controller. Please check the power and the Ethernet cable connection of the product.
'FMP_DATAERROR' indicates that the value you are trying to set is out of the range of the corresponding parameter. Please check the range of the corresponding parameter again.

Please refer to the 'ReturnCodes_Define.py' file and the product manual for more detailed information of the return values.

[KR]  
'FAS_SetParameter' 함수의 리턴 값인 nRtn에는 함수의 성공 혹은 실패(그리고 실패의 원인)를 알려줍니다.

함수가 아무런 문제 없이 정상적으로 수행되었다면 'FMM_OK'를 리턴합니다. 

'FMM_OK' 이외의 값을 받았다면, 함수가 정상적으로 실행되지 못하였음을 가리킵니다.
'FMC_TIMEOUT_ERROR'는 제어기로 부터 아무런 응답을 받지 못하였음을 표시합니다. 제품의 전원이 꺼져 있지 않은지, Ethernet 케이블의 연결에 문제는 없는지 확인하시기 바랍니다.
'FMP_DATAERROR'는 설정하려는 값이 해당 파라미터의 범위를 벗어났음을 표시합니다. 해당 파라미터의 범위를 다시 확인하시기 바랍니다.

이외에도 여러 리턴값이 존재합니다. 'ReturnCodes_Define.py' 파일과 제품의 매뉴얼을 참조하시기 바랍니다.
