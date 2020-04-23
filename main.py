import pymysql
import serial
import time

if __name__ == "__main__":

    Host = '127.0.0.1'
    Port = 3307
    Database = 'gas_v2'
    User = 'root'
    Password = 'offset01'

    portNum = input('Serial Port Number (ex:COM4) : ')
    ser = serial.Serial(  # Serial port setting
        port=portNum,
        # port='COM4',
        baudrate=9600
    )
    print("Serial Open Success")
    while(1):
        try:
            if(ser.readable()):
                ser.flush()  # serial 미완료 송신 대기
                messages = ser.readline()  # serial 수신n
                # print(messages)
                message = messages.decode('utf-8')[:-3].split('.')  # Byte -> char
                for value in message:
                    # value = value[:-3]
                    value = value.split(' ')
                    idx = int(value[0])
                    sensors = [int(i) for i in value[1:]]  # char -> int
                    print(idx)
                    print(sensors)
                    conn = pymysql.connect(host=Host, port=Port, database=Database, user=User, password=Password)
                    with conn.cursor() as cursor:
                        sql = 'insert into gas_log (gas_module_idx,tgs2600,tgs2602,tgs2603,tgs2610,tgs2620,tgs826) values (%s,%s,%s,%s,%s,%s,%s);'
                        cursor.execute(sql, (idx, sensors[0], sensors[1], sensors[2], sensors[3], sensors[4], sensors[5]));
                    conn.commit()
                    conn.close()

        except Exception as ex:
            print("Serial Port Open Error", ex)