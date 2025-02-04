from spider_controller import SpiderController


if __name__ == '__main__':
    controller = SpiderController('config.json')

    controller.run_spider('spider2107','nyaa',q='NHDT-743')
    # controller.run_selected_spiders({
    #     'spider2107': ['nyaa', 'another_spider'],
    #     'another_project': ['some_spider']