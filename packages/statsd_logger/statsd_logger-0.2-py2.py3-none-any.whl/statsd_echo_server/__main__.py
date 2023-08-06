'''
Simple StatsD Echo Server
'''
import socket
from termcolor import colored


class StatsDServer:
    def __init__(self, host='127.0.0.1', port=8125):
        self.port = port
        self.host = host

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def run(self):
        '''Main function.
        Listen on port 8125 by default, parse StatsD messages
        received on port and print on stdout'''
        print("Server listening on {}:{}".format(self.host, self.port))
        try:
            while True:
                data, _ = self.sock.recvfrom(1024)

                data = data.decode('utf-8').split('\n')
                for line in data:
                    metric_val, metric_type, tag = line.split('|')
                    metric, value = metric_val.split(':')
                    metric = colored(metric, 'blue')
                    value_str = colored("|".join([value, metric_type, tag]), 'green')
                    print("StatsD Metric: {} {}".format(metric, value_str))
        except KeyboardInterrupt:
            print("Stopping StatsD Echo Server")
            self.sock.close()


def main():
    '''Create statsd server and run it'''
    server = StatsDServer()
    server.run()


if __name__ == '__main__':
    main()
