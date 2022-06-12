
import xlrd
import re
import xlwt
# # 读取数据
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('数据格式化', cell_overwrite_ok=True)
sheet.write(r=0, c=0, label='编号')
sheet.write(r=0, c=1, label='日期')
sheet.write(r=0, c=2, label='确诊')
sheet.write(r=0, c=3, label='无症状')
sheet.write(r=0, c=4, label='转化确诊')
row = 1
##########################
# 数据分割
data = xlrd.open_workbook('cod19.xls')
table = data.sheets()[0]
nrows = table.nrows
for i in range(nrows):
    table_lists = table.row_values(rowx=i, start_colx=0, end_colx=None)
    # print(table_lists[1])
    # 分割日期
    time = re.findall(r'\d{1,2}月\d{1,2}日', table_lists[1])
    numbers = re.findall('(?<=新增本土新冠肺炎确诊病例).[0-9]*', table_lists[1])
    numbers2 = re.findall('(?<=本土无症状感染者).[0-9]*', table_lists[1])
    numbers3 = re.findall('(?<=无症状感染者转为确诊病例).[0-9]*', table_lists[1])
    # 写入序号
    sheet.write(r=row, c=0, label=row)
    row = i + 1
    # 写入日期
    sheet.write(r=row, c=1, label=time)
    # 写入感染者
    sheet.write(r=row, c=2, label=numbers)
    # 写入无症状
    sheet.write(r=row, c=3, label=numbers2)
    # 转化确诊
    sheet.write(r=row, c=4, label=numbers3)
    workbook.save('数据格式化.xls')


