import os
from os.path import exists
from time import time


MAX_LOG_SIZE_IN_BYTES = 1_000_000

def rotate_logs():
    pi_pathname = os.path.curdir
    log_pathname = pi_pathname + '/logs'
    log_filename = log_pathname + '/log.txt'

    if not exists(pi_pathname):
        os.mkdir(pi_pathname)

    if not exists(log_pathname):
        os.mkdir(log_pathname)

    if not exists(log_filename):
        new_log_file = open(log_filename, 'w')
        new_log_file.close()

    filesize = os.path.getsize(log_filename)

    if filesize > MAX_LOG_SIZE_IN_BYTES:
        rotate_file = '{}/log-{}.txt'.format(pi_pathname, time.ctime())
        os.rename(log_filename, rotate_file)
        new_log_file = open(log_filename, 'w')
        new_log_file.close()

def log_temperature(temperature, message):
    log_filename = f'{os.path.curdir}/logs/log.txt'

    with open(log_filename, 'a') as f:
        logtext = '{} {} {}\n'.format(time.ctime(), temperature, message)
        f.write(logtext)