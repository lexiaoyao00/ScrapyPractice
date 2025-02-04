import os
import sys
import json
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class SpiderController:
    def __init__(self, config_file='config.json', result_dir='outputs'):
        self.config = self.load_config(config_file)
        self.processes = {}
        self.result_dir = os.path.abspath(result_dir)
        # self.ensure_result_dir()
        self.original_cwd = os.getcwd()  # 保存原始工作目录

    def load_config(self, config_file):
        with open(config_file,'r',encoding="UTF-8") as f:
            return json.load(f)

    def ensure_result_dir(self):
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def setup_project(self, project_name):
        if project_name not in self.processes:
            project_config = self.config[project_name]
            project_path = project_config['project_path']

            sys.path.append(project_path)
            os.chdir(project_path)  # 改变到项目目录
            settings = get_project_settings()
            self.processes[project_name] = CrawlerProcess(settings)

    def set_output(self, process, output, project_name, spider_name):
        if output:
            self.ensure_result_dir()
            base_name, ext = os.path.splitext(output)
            file_name = f"{base_name}_{project_name}_{spider_name}{ext}"
            spider_output = os.path.join(self.result_dir, file_name)
            process.settings.set('FEEDS', {
                spider_output: {
                    'format': 'csv',
                    'encoding': 'utf8',
                },
            })

    def run_spider(self, project_name, spider_name, output=None, **kwargs):
        self.setup_project(project_name)
        process = self.processes[project_name]

        self.set_output(process, output, project_name, spider_name)

        spider_config = self.config[project_name]['spiders'].get(spider_name, {}).copy()

        spider_config.update(kwargs)

        # 将参数添加到 Scrapy 的 settings 中
        for key, value in spider_config.items():
            if isinstance(value, list):
                # 如果值是列表，直接设置
                process.settings.set(key, value)
            else:
                # 如果不是列表，将其转换为单元素列表
                process.settings.set(key, [value])

        print(f"Starting spider: {spider_name} in project: {project_name} with config: {spider_config}")
        print(f"Additional settings: {kwargs}")
        process.crawl(spider_name, **spider_config)
        process.start()
        os.chdir(self.original_cwd)  # 恢复原始工作目录

    def run_project_spiders(self, project_name, output=None):
        self.setup_project(project_name)
        process = self.processes[project_name]

        for spider_name, spider_config in self.config[project_name]['spiders'].items():
            self.set_output(process, output, project_name, spider_name)
            print(f"Starting spider: {spider_name} in project: {project_name} with config: {spider_config}")
            process.crawl(spider_name, **spider_config)
        process.start()
        os.chdir(self.original_cwd)  # 恢复原始工作目录

    def run_selected_spiders(self, selections, output=None):
        for project_name, spider_names in selections.items():
            self.setup_project(project_name)
            process = self.processes[project_name]

            for spider_name in spider_names:
                if spider_name in self.config[project_name]['spiders']:
                    self.set_output(process, output, project_name, spider_name)
                    spider_config = self.config[project_name]['spiders'][spider_name]
                    print(f"Starting spider: {spider_name} in project: {project_name} with config: {spider_config}")
                    process.crawl(spider_name, **spider_config)
                else:
                    print(f"Warning: Spider '{spider_name}' not found in project '{project_name}'")

        # 启动所有已配置的爬虫进程
        for process in self.processes.values():
            process.start()
        os.chdir(self.original_cwd)  # 恢复原始工作目录
