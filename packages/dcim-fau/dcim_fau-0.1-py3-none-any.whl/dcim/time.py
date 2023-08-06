from time import time, sleep


# wait for specified (conf.yaml) interval value
def wait(start, interval):
    print('waiting {0} seconds'.format(interval-(time()-start)))
    while time() - start < interval:
        sleep(.1)
