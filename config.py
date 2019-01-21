import datetime

path_to_parsing='/home/render/bot/raspbot/'
path_to_rasp='/home/render/bot/rasptxt/'
patt_to_groop="/home/render/bot/groop.txt"
path_to_admin_id="/home/render/bot/IdAdmin.txt"
path_to_log="/home/render/bot/log.txt"
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
