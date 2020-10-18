import subprocess


# start kafka server
kafka_dir = "C:/Users/krock/kafka_2.13-2.6.0/"


def start_server():
    process = subprocess.Popen(['C:/Users/krock/kafka_2.13-2.6.0/bin/windows/kafka-server-start.bat', 'C:/Users/krock/kafka_2.13-2.6.0/config/server.properties'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               shell=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break
    start_server()


if __name__ == '__main__':
    start_server()
