import re
# Use regular Experssion answer from https://stackoverflow.com/a/319293
def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None
def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None

def v4_prefix(addr):
    if addr[-3] == '/':
        pfx = int(addr[-2:])
        adr = is_valid_ipv4(addr[:-2])
    elif addr[-2] == '/':
        pfx = int(addr[-1])
        adr = is_valid_ipv4(addr[:-1])
    else:
        if is_valid_ipv4(addr): 
            return 32
        else:
            return False
    if (pfx < 8 or pfx > 32) or adr:
        return False
    else:
        return pfx

def v6_prefix(addr):
    slash = addr.find('/')
    if slash == -1:
        if is_valid_ipv6(addr):
            return 128
        else:
            return False
    elif slash - len(addr) < -4:
        return is_valid_ipv6(addr)
    else:
        adr = addr[:(slash-len(addr))]
        pfx = int(addr[(slash-len(addr)+1):])
        if is_valid_ipv6(adr):
            if pfx >=8 and pfx <= 128:
                return pfx
            else:
                return False
        else:
            return False

if __name__ == '__main__':
    valist_v4 = [ '1.1.1.1' , '2.2.2.2' , '999.99.9.9' , '1.1.1.1/24' , '2.2.2.2/33' ]
    valist_v6 = [ '2001:db8::1' , '::1' , 'game::0ver' , '2001:a::c/32' , '2001:b::c/129' ] 
    for addrs in valist_v4:
        print(f' {addrs} v4 : {is_valid_ipv4(addrs)} prefix {v4_prefix(addrs)}')
    for addrs in valist_v6:
        print(f' {addrs} v6 : {is_valid_ipv6(addrs)} prefix {v6_prefix(addrs)}')
