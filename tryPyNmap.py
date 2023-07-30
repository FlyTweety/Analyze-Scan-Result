import nmap


def test():
    ip = '192.168.137.1'
    nm = nmap.PortScanner()
    nm.scan(ip, '80, 445', '-v -n -sS -T4 -Pn')
    print(nm.command_line())
    #print(nm.scaninfo())
    #print(nm.all_hosts())
    print(nm[ip])


if __name__ == '__main__':
    test()