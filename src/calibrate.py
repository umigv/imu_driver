import rospy
from sensor_msgs.msg import Imu

def write_calibration(x, y, z):
    payload = b''.join([
        (x).to_bytes(2, 'little', signed=True),
        (y).to_bytes(2, 'little', signed=True),
        (z).to_bytes(2, 'little', signed=True),
        b'\x00' * 16,
        # b'\x70\x02\xD7\x00\x2A\xFF\xFF\xFF\x00\x00\x00\x00\xE8\x03\x17\x03',
    ])
    with open("NDOF_calibration", "wb") as f:
        f.write(payload)

if __name__ == '__main__':
    rospy.init_node('imu_calibration', anonymous=True)
    samples = []
    print('Taking 100 samples')
    while len(samples) <= 100:
        samples.append(rospy.wait_for_message("/imu/data", Imu, timeout=None))
    print('Finished sampling')
    x_avg = sum([sample.linear_acceleration.x for sample in samples]) / 100
    y_avg = sum([sample.linear_acceleration.y for sample in samples]) / 100
    z_avg = sum([sample.linear_acceleration.z - 9.8 for sample in samples]) / 100
    write_calibration(round(x_avg * 100), round(y_avg * 100), round(z_avg * 100))
    print('Wrote calibration')
