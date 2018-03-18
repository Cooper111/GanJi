from multiprocessing import Pool
from pages_parsing import get_links
from pages_parsing import get_pageInfo
from get_list import channel_list

def get_all_links_from(channel):
    for i in range(1,100):
        get_links(channel,i)



if __name__ == '__main__':

    pool = Pool()
    # pool = Pool(processes=6)
    pool.map(get_all_links_from, channel_list.split())

    pool.close()
    pool.join()
