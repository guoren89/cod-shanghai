# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import xlwt
import pymysql


class CodPipeline:
    def open_spider(self,spider):
        self.workbook=xlwt.Workbook()
        self.sheet=self.workbook.add_sheet('sheet1')
        self.sheet.write(r=0,c=0,label='编号')
        self.sheet.write(r=0,c=1,label='日期')
        self.sheet.write(r=0,c=2,label='确诊')
        self.sheet.write(r=0,c=3,label='无症状')
        print('excel创建成功')
        self.row=0

    def process_item(self,item,spider):
        self.row+=1
        self.sheet.write(r=self.row,c=0,label=int(self.row))
        self.sheet.write(r=self.row,c=1,label=item['title'])
        print(f'{self.row}记录')



        fname=os.getcwd()+'/cod19.xls'
        self.workbook.save(fname)

        print('写入成功')
        return item
##########
class CsvPipeline:

    def open_spider(self,spider):
        fname=os.getcwd()+'/cod19.csv'
        self.fname=open(fname,'w',encoding='utf-8')
        line='编号，内容'
        self.fname.write(line+'\n')
        self.row=0
        print('csv文件创建')

    def process_item(self,item,spider):
        self.row+=1
        line=f'{self.row},{item["title"]}\n'
        self.fname.write(line+'\n')
        print(f'csv共{self.row}行')
        return item

    def close(self,spider):
        self.fname.close()
        print('csv已创建')

