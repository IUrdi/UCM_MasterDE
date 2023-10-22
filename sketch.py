"""
Program to analize the logs files of an apache server.
An example of file acommpanies this file: access.log


"""
import re
from datetime import datetime
import doctest

def get_user_agent(line: str) -> str:
    """
    Get the user agent of the line.

    Examples
    ---------
    >>> get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
    """
    userRegExp=re.compile(r'\[.+\]\s+".+"\s+\d+\s+\d+\s+".+"\s+"(?P<userAgent>.+)".*')
    find=userRegExp.search(line)
    return find.group('userAgent')

def is_bot(line: str) -> bool:
    '''
    Check of the access in the line correspons to a bot

    Examples
    --------
    >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    False

    >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    True

    >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    True
    '''
    botRegExp=re.compile(r'[Bb]ot')
    userAgent=get_user_agent(line)
    isBot=bool(botRegExp.findall(userAgent))
    return isBot
    #raise NotImplementedError()


def get_ipaddr(line):
    '''
    Gets the IP address of the line

    >>> get_ipaddr('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    '213.180.203.109'

    >>> get_ipaddr('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    '147.96.46.52'
    '''
    ipRegExp=re.compile(r'^(\S+)\s.*')
    ipAddress=ipRegExp.findall(line)
    return ipAddress[0]
    #raise NotImplementedError()



def get_hour(line: str) -> int:
    """
    Get the user agent of the line.

    Expamples
    ---------
    >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    0

    >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    12
    """
    datetimeRegExp=re.compile(r'\[(?P<datetime>.+)\]\s+".+"\s+\d+\s+\d+\s+".+"\s+"(?P<userAgent>.+)".*')
    datetimeCET=datetimeRegExp.search(line)
    datetimeCET=datetime.strptime(datetimeCET.group('datetime'),'%d/%b/%Y:%H:%M:%S %z')
    return datetimeCET.hour

def histbyhour(filename: str) -> dict[int, int]:
    '''
    Computes the histogram of access by hour
    '''
    timeHistogram=dict()
    with open(filename,'r') as f:
        for log in f:
            hour=get_hour(log)
            if not hour in timeHistogram:
                timeHistogram[hour]=1
            else:
                timeHistogram[hour]+=1
        return timeHistogram

def ipaddreses(filename: str) -> set[str]:
    '''
    Returns the IPs of the accesses that are not bots
    '''
    with open(filename,'r') as f:
        validAddresses ={get_ipaddr(log) for log in f if not is_bot(log)}
    return validAddresses


def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_ipaddr, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)


def test_ipaddresses():
    assert ipaddreses('access_short.log') == {'34.105.93.183', '39.103.168.88'}

def test_hist():
    hist = histbyhour('access_short.log')
    assert hist == {5: 3, 7: 2, 23: 1}

def test():
    test_hist()
    test_ipaddresses()
    test_doc()
def main():
    fileName='access.log'
    ip=ipaddreses(filename=fileName)
    hist=histbyhour(filename=fileName)

if __name__=='__main__':
    main()
    test_hist()