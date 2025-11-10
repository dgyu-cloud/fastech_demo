import sys
sys.path.append("/python/PE/Library")

import FAS_EziServo  # 또는 FAS_EziServo
import time

# ---------------------------------------------------------
# Ezi-SERVO Ethernet 연결 정보
# ---------------------------------------------------------
ip = "192.168.0.2"  # 드라이버 IP
port = 502           # 기본 포트
slave_id = 1         # 슬레이브 ID (EziManager에서 확인)

# 객체 생성
driver = FAS_Ethernet(ip, port)

# 연결 시도
if not driver.connect():
    print("❌ Connection failed")
    exit()
print("✅ Connected to Fastech Ezi-SERVO Ethernet")

# 서보 ON
driver.set_servo_on(slave_id, True)
time.sleep(0.5)

# 현재 위치 확인
pos = driver.get_command_position(slave_id)
print(f"Current position: {pos}")

# 절대 위치 이동
target = 50000
velocity = 2000
print(f"Moving to {target}")
driver.move_abs(slave_id, target, velocity)

# 이동 완료 대기
while True:
    status = driver.read_motion_status(slave_id)
    if not status['RUN']:
        break
    time.sleep(0.1)

print("✅ Motion complete")

# 서보 OFF
driver.set_servo_on(slave_id, False)

# 연결 해제
driver.disconnect()
print("Disconnected")
