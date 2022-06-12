#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
#plt绘图库 rcParams配置参数，调色板,FontProperties 字体属性
from matplotlib import  pyplot as plt,rcParams, cycler
#字体管理器
from matplotlib import font_manager
import matplotlib as mpl 
import re
from scipy import stats


# In[2]:


# plt.style.use('seaborn')
plt.style.use('ggplot')
#常规配置
#字体 宋体，可以用自己安装的其他字体
plt.rcParams['font.sans-serif']=['Microsoft YaHei','SimHei'] #可以配置多个的
# 设置中文和负号正常显示
plt.rcParams['axes.unicode_minus']=False #处理些特殊字符


# In[3]:


df_book=pd.read_excel(io='./spiders/数据格式化.xls',sheet_name='数据格式化')
print(df_book)


# In[4]:


df_book.reset_index(inplace=True,drop=True)
df_book.drop(columns=['编号','转化确诊'],inplace=True)
print(df_book)


# In[5]:


df_book.dropna(subset=['确诊','无症状'],inplace=True)
df_book.reset_index(inplace=True,drop=True)
df_book.info()
df_book['无症状']=df_book['无症状'].astype('int64')
# df_book['日期']=df_book['日期'].astype('datetime64')
df_book.info()


# In[6]:


def processdate(x):
    exp=r'\d+'
    result=re.findall(exp,x)
    result='2022-'+result[0]+'-'+result[1]
    return result
df_book['日期']=df_book['日期'].apply(processdate)
df_book.info()
# for i in range(0,len(df_book['日期'])):
#     a=df_book.iloc[i,0].replace('月','-')
#     df_book['日期']=a.replace('日','')
# df_book['日期']


# In[7]:


#计算无症状增长
#增加列
df_book['较昨日新增']=df_book['无症状']-df_book['无症状'].shift(-1)
df_book.fillna(0)


# In[8]:


df_book['确诊']=df_book['确诊'].fillna(0)
print(df_book)


# In[9]:


df_book['日期'] = pd.to_datetime(df_book.日期)
df_book.sort_values(by='日期',inplace=True)
print(df_book)


# In[10]:


df_book['增长率']=df_book['较昨日新增']/df_book['无症状']
print(df_book)


# In[11]:


df_book['确诊']=df_book['确诊'].replace(' ',0,regex=True)
df_book


# In[12]:


sub_data=df_book.loc[df_book.日期>= '2022-02-20' ,:]
plt.figure(figsize=(20,10))
plt.plot(sub_data['日期'],
         sub_data['无症状'],
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = '*', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='blue', # 点的边框色
         markerfacecolor='brown',# 点的填充色
         label='无症状人数'
        ) 

plt.plot(sub_data['日期'],
         sub_data['确诊'],
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = '*', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='red', # 点的边框色
         markerfacecolor='brown',# 点的填充色
         label='确诊人数'
        ) 

plt.title('确诊，无症状趋势图')
plt.xlabel('日期')
plt.ylabel('人数')
# 获取图的图对象
ax = plt.gca()
# # 设置日期的显示格式  
xlocator = mpl .ticker.MultipleLocator(7)
ax.xaxis.set_major_locator(xlocator)
# # 为了避免x轴日期刻度标签的重叠，设置并且45度倾斜
plt.xticks(rotation=45)
# 显示图形
plt.legend()
plt.show()


# In[13]:


np.mean(df_book['增长率'])


# In[14]:


df_book['天数'] = range(1,len(df_book)+1)


# In[15]:


df_book


# In[16]:


df_book[['天数','增长率']]


# In[17]:


sub_data=df_book.loc[df_book.日期>= '2022-02-20' ,:]
plt.figure(figsize=(20,10))
plt.plot(sub_data['天数'],
         sub_data['增长率'],
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = '*', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='blue', # 点的边框色
         markerfacecolor='brown',# 点的填充色
         label='天数-增长率'
        ) 


# In[18]:


np.min(df_book['增长率'])


# In[19]:


df_book[df_book['增长率'].isin([np.min(df_book['增长率'])])]
# df[df['列名'].isin([相应的值])]


# In[20]:


#回归
x = df_book[['天数']] #作为自变量
y = df_book[['无症状']]#作为因变量


# In[21]:


#回归
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import PolynomialFeatures
x = df_book[['天数']]
ds = []
scores = []
for d in range(2,80):  #从第2阶开始尝试到第20阶
    ds.append(d)
    p1 = PolynomialFeatures(degree = d)
    x_d = p1.fit_transform(x)  #转化
    lrModel = LinearRegression()
    lrModel.fit(x_d,y)
    scores.append(lrModel.score(x_d,y))
    
dScores = pd.DataFrame({
    
    '阶次':ds,
    '模型得分':scores
})


# In[22]:


dScores


# In[23]:


np.max(dScores['模型得分'])
dScores[dScores['模型得分'].isin([np.max(dScores['模型得分'])])]
# df_book[df_book['增长率'].isin([np.min(df_book['增长率'])])]


# In[24]:


plt.xlabel('阶次')
plt.ylabel('模型得分')
plt.title('多项式阶次与模型得分')
plt.scatter(ds,scores,color = 'red')


# In[25]:


p2 = PolynomialFeatures(degree = 10)
x_3 = p2.fit_transform(x)
lrModel = LinearRegression()
lrModel.fit(x_3,y)
lrModel.score(x_3,y)


# In[26]:


px3 = pd.DataFrame({
    
    "天数":[150] #天数可以自己选择
})
px_3 = p2.fit_transform(px3)
lrModel.predict(px_3)


# In[27]:


df_book2=df_book.head(50)
df_book2


# In[28]:


mean_m=[]
for i in range(0,len(df_book['增长率'])):

    if i>=2:
        a=np.mean(df_book['增长率'].head(i))
        mean_m.append(a)
    else:
        mean_m.append(0)
df_book


# In[29]:


df_book['平均增长率']=mean_m


# In[30]:


df_book


# In[31]:


sub_data=df_book.loc[df_book.日期>= '2022-02-20' ,:]
plt.figure(figsize=(30,10))
plt.plot(sub_data['天数'],
         sub_data['平均增长率'],
         linestyle = '-', # 折线类型
         linewidth = 4, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = '*', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='blue', # 点的边框色
         markerfacecolor='brown',# 点的填充色
         label='天数-增长率'
        ) 


# In[32]:


#散点图
plt.scatter(x=df_book["增长率"],y=df_book["无症状"],marker='*',s=50)
plt.title("散点图测试")
plt.show()


# In[33]:


#检验数据是否正太分布
u = df_book['无症状'].mean()  # 计算均值
std = df_book['无症状'].std()  # 计算标准差
stats.kstest(df_book['无症状'], 'norm', (u, std))


# In[34]:


#p值大于0.05符合正太分布


# In[35]:


#皮尔逊相关
from scipy.stats import stats
X=df_book['天数']
Y=df_book['无症状']
r,p=stats.pearsonr(X,Y)
print(r,p)


# In[ ]:




