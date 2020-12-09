def get_data(url):
    """
    从数据源（携程）爬取数据，对元数据进行筛选，返回我们想要的数据
    """
    return ""


def process_data(data):
    """
    将数据进行加工，整合到ArcGIS Online，输出地图URL
    """
    return ""


def show_map(map):
    """ 
    展示地图
    """
    pass


def main():
    url = "Ctrip.com"
    data = get_data(url)
    map = process_data(data)
    show_map(map)


main()
