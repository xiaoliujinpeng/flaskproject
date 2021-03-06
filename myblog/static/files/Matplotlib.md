# Matplotlib

### 容器

##### figure

```
import matplotlib.pyplot as plt
fig=plt.figure()   创建一个空的figure  即没有子区域
fig,ax=plt.subplots()  创建一个figure和一个子区域
fig,axs=plt.subplots(2,2)  创建一个figure和4个子区域

fig.close()关闭figure
```

为figure增加axes

```
fig.add_axes([left,bottom,width,height]) 或者  坐标是0-1的小数
plt.axes([left,bottom,width,height])
```

为figure增加subplot

```
ax1=fig.add_subplot(211)
ax2=fig.add_subplot(212)
```

增加的axes和subplot都会加进fig.axes这个列表中(毕竟subplot是axes的子类)

删除axes

```
fig.delaxes(axname)
```



获取figure patch的属性

```
matplotlib.artist.getp(fig.patch)
同plt.getp(fig.patch)  一样
```



figure的一些属性

| Figure attribute | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| axes             | A list of Axes instances (includes Subplot)                  |
| patch            | The Rectangle background                                     |
| images           | A list of FigureImage patches - useful for raw pixel display |
| legends          | A list of Figure Legend instances (different from Axes.legends) |
| lines            | A list of Figure Line2D instances (rarely used, see Axes.lines) |
| patches          | A list of Figure patches (rarely used, see Axes.patches)     |
| texts            | A list Figure Text instances                                 |



##### <u>Axes</u>（非常重要）

图形展示的区域，包括在figure之中

```
设置标题  ax.set_title()
设置x和y轴标签  ax.set_xlabel()  ax.set_ylabel()
设置x和y的范围  ax.set_xlim()  ax.set_ylim()
也可以这样ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
或 ax.axis([xmin,xmax,ymin,ymax])
```

```
当调用plot时，会自动创建一个Line2D实例，并将它添加到axes.lines列表中
当掉用bar时，会创建一系列矩形，并将其添加到axes.patches中，
不要自己创建实例然后添加到，axes.lines和axes.patches中，因为中间省略了一系列复杂的过程


```

一些创建primitive artists 的方法

| Helper method                  | Artist               | Container               |
| ------------------------------ | -------------------- | ----------------------- |
| ax.annotate - text annotations | Annotate             | ax.texts                |
| ax.bar - bar charts            | Rectangle            | ax.patches              |
| ax.errorbar - error bar plots  | Line2D and Rectangle | ax.lines and ax.patches |
| ax.fill - shared area          | Polygon              | ax.patches              |
| ax.hist - histograms           | Rectangle            | ax.patches              |
| ax.imshow - image data         | AxesImage            | ax.images               |
| ax.legend - axes legends       | Legend               | ax.legends              |
| ax.plot - xy plots             | Line2D               | ax.lines                |
| ax.scatter - scatter charts    | PolygonCollection    | ax.collections          |
| ax.text - text                 | Text                 | ax.texts                |

axes的一些属性

| Axes attribute | Description                            |
| -------------- | -------------------------------------- |
| artists        | A list of Artist instances             |
| patch          | Rectangle instance for Axes background |
| collections    | A list of Collection instances         |
| images         | A list of AxesImage                    |
| legends        | A list of Legend instances             |
| lines          | A list of Line2D instances             |
| patches        | A list of Patch instances              |
| texts          | A list of Text instances               |
| xaxis          | matplotlib.axis.XAxis instance         |
| yaxis          | matplotlib.axis.YAxis instance         |

##### subplot

Axes的子类



##### Axis

处理`刻度线`,`网格线`,`刻度线标签`,`坐标轴标签`

axis 包含一个label属性和一系列刻度线

一些

```
axis.Axis.get_major_ticks()获取主要的刻度  返回一个列表其中包括XTick或YTick
axis.Axis.get_minor_ticks()获取次要的刻度
axis.Axis.get_ticklines() 获得刻度线，是默认是刻度线标签的两倍，因为底边和顶边都有刻度线，只有底部有刻度线标签
axis.Axis.get_ticklocs()  获取刻度线标签列表
axis.Axis.get_ticklabels()  获取刻度线标签及其位置，返回一个列表

若要获得次要刻度线，只需把minor设置为True,如
axis.Axis.get_ticklines(minor=True)
```

一些有用的方法

| get_scale           | The scale of the axis, e.g., 'log' or 'linear'               |
| ------------------- | ------------------------------------------------------------ |
| get_view_interval   | The interval instance of the axis view limits                |
| get_data_interval   | The interval instance of the axis data limits                |
| get_gridlines       | A list of grid lines for the Axis                            |
| get_label           | The axis label - a Text instance                             |
| get_ticklabels      | A list of Text instances - keyword minor=True\|False         |
| get_ticklines       | A list of Line2D instances - keyword minor=True\|False       |
| get_ticklocs        | A list of Tick locations - keyword minor=True\|False         |
| get_major_locator   | The [`ticker.Locator`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Locator) instance for major ticks |
| get_major_formatter | The [`ticker.Formatter`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Formatter) instance for major ticks |
| get_minor_locator   | The [`ticker.Locator`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Locator) instance for minor ticks |
| get_minor_formatter | The [`ticker.Formatter`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Formatter) instance for minor ticks |
| get_major_ticks     | A list of Tick instances for major ticks                     |
| get_minor_ticks     | A list of Tick instances for minor ticks                     |
| grid                | Turn the grid on or off for the major or minor ticks         |

| 方法                 | 描述              |
| -------------------- | ----------------- |
| Axes.set_xticks      | 设指x刻度线的位置 |
| Axis.set_tickslabels | 设置刻度线标签    |
| Axes.set_xticklabels | 设置刻度线标签    |



##### Tick

Tick 包含了tick和grid line 实例，还有label instance 和上下刻度线

一些属性

| Tick attribute | Description     |
| -------------- | --------------- |
| tick1line      | Line2D instance |
| tick2line      | Line2D instance |
| gridline       | Line2D instance |
| label1         | Text instance   |
| label2         | Text instance   |



##### 使用matplotlib的两种重要方式

面向对象的方式

```
import matplotlib.pyplot as plt
fig,ax=plt.subplots()  创建一个figure 和 axes
然后利用axer绘图
ax.plot(..)
..


```

pyplot-style

```
import matplotlib.pyplot as plt
直接使用pyplot绘图
plt.plot(..)
....
```



### pyplot

这里面包含了很多绘图函数且它们类似于matlab

##### plot()

`matplotlib.pyplot.plot`(**args*, *scalex=True*, *scaley=True*, *data=None*, ***kwargs*)[[source\]](https://matplotlib.org/stable/_modules/matplotlib/pyplot.html#plot)

```
import matplotlib.pyplot as plt
plt.plot()   生成一个Line2D实例，并将它加进Axes.lines列表，然后返回


如果只给plot函数一个序列参数,例如
plt.plot([1,2,3,4])   默认对应的是y轴，而x轴会根据y的长度从零开始自动生成
如果给两个序列参数
plt.plot([1,2,3,4],[1,2,3,4])  则第一个参数对应x轴，第二个参数对应y轴

plot的第三个参数是颜色和线条类型默认是"b-"代表蓝色实线
plt.plot([1,2,3,4],[1,2,3,4],"ro")  是红圆圈  

还有linewidth参数设置线宽
plt.plot([1,2,3,4],[1,2,3,4],"ro",linewidth=2.0) 


还可以同时设置多组
plt.plot([1,2,3,4],[1,2,3,4],"ro"，[1,2,3,4],[1,2,3,4],"r+")


a,=plt.plot([1,2,3,4],[1,2,3,4])
a.set_antialiased(False)   //是否设置抗锯齿，设为False则有锯齿
```

##### setp()

"setproperty"的缩写

`matplotlib.pyplot.setp`(*obj*, ***args, *****kwargs*)[
  ](https://matplotlib.org/stable/_modules/matplotlib/pyplot.html#setp)

给artist对象设置属性

```
line,=plt.plot([1,2,3])
plt.setp(line,color='r',linewidth=2.0)
或者使用matlab风格的
plt.setp(line,"color","r","linewidth",2.0)

只写第一个参数而不写后面的参数会列出可以修改的属性，例如
plt.setp(line)
输出:
  alpha: float
  animated: [True | False]
  antialiased or aa: [True | False]
  ...snip
  
  
  
```

##### 当前的figure和axes

使用的绘图函数会应用到当前的figure和axes

`gcf()`用于获取当前的figure,返回一个[`matplotlib.figure.Figure`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure) 

`gca()`用于获取当前的axes，返回一个 [`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/axes_api.html#matplotlib.axes.Axes) 

我们一般不用担心，matplotlib会自动处理

```
fig=plt.figure()  其实默认调用的是figure(1)
plt.subplot()  其实默认调用的是subplot(111)
subplot的参数
subplot(numrows,numcols,plot_number)  plot_number<=numrows*numcols
例如plt.subplot(2,1,1)  也可以不用逗号subplot(211)
```

`clf()`清除当前的figure

`cla()`清除当前的axes



##### 绘图函数

annotating text

`matplotlib.pyplot.annotate(text,xy,xytest,xycoords="data",textcoords,arrowprops,..)`

```
例如
plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
```

bar

`Axes.bar`(*self*, *x*, *height*, *width=0.8*, *bottom=None*, ***, *align='center'*, *data=None*, ***kwargs*)[
  ](https://matplotlib.org/stable/_modules/matplotlib/axes/_axes.html#Axes.bar)

```
x  要求一个浮点数或一个类数组
height bars的高度  要求一个浮点数或一个类数组
widht   bars的宽度 要求一个浮点数或一个类数组默认是0.8
align   {"center","edge"}  默认是"center"
color   颜色
xerr,yerr  要求浮点数或类数组 错误箭头的长度
bottom 距离0刻度的距离  浮点数或类数组
```



##### 控制样式

查看所有样式

```
print(plt.sytle.available)
```

使用某个样式

```
plt.style.use("fivethirtyeight")
```



##### 保存图像

查看可以保存的类型

```
print(fig.canvas.get_supported_filetypes())
```

保存figure

```
fig.savefig()
参数：
transparent=True  将背景设置为透明
dpi=80  控制输出分辨率，每平方英寸的像素
bbox_inches="tight"  使图形适应边界
```

