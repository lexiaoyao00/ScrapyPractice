from spider_controller import SpiderController


if __name__ == '__main__':
    controller = SpiderController('config.json')

    # controller.run_spider('spider2107','douban')
    # controller.run_spider('spider2107','nyaa',q='MIDE_565')
    # controller.run_selected_spiders({
    #     'spider2107': ['nyaa', 'another_spider'],
    #     'another_project': ['some_spider']

    scraped_data  = controller.run_spider('mySpider','hanime',output='test.csv')

    print(scraped_data)

