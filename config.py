import datetime

path_to_parsing='/root/bot/raspbot/'
path_to_rasp='/root/bot/rasptxt/'
patt_to_groop="/root/bot/groop.txt"
path_to_admin_id="/root/bot/IdAdmin.txt"
path_to_log="/root/bot/log.txt"
token = ''


def date(n=0):
    delta = datetime.timedelta(days=n)
    det = datetime.date.today()
    det += delta
    det = str(det)
    det = det.split('-')
    det.reverse()
    det = '.'.join(det)
    return det


if __name__ == '__main__':
    pass
