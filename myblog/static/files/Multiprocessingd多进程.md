# Multiprocessing

### 添加一个进程对象

##### 第一个中方法

```
通过multiprocessing.Process(target,args)实例化一个进程对象
第一个参数target是进程调用的对象函数，args是调用函数的参数
```

```
process.start()运行一个进程
```

##### 第二种方法

```
通过类来实现
form multiprocessing import Process
class myProcess(Process):
	def __init__(self,args):
		super().__init__()
		....
	def run():
		...     ##进程执行的代码  start()如果未指定target就运行run里面的代码
```

### 常用方法

```
is_alive() 返回进程是否在运行bool类型
join()等待进程终止才结束主进程
start()进程准备就绪，等待cpu调度
run（）就是Process类里的run
terminate() 不管任务是否完成立即终止
```

### 进程队列

```
from multiprocessing import Queue

进程队列可用于进程间通信

q=Queue()实例化化进程队列
q.put(name) 放入进程队列
q.get()从进程队列获取 
```

### 进程管道

```
from multiprocessing import Pipe
con1,con2=Pipe() 实例化的是一个双向管道

con1.send(data)  是发送数据 给con2
con2.recv() 接受con1发送过来的数据，如果没有就会堵塞
```

### 进程间共享数据

```
from multiprocessing import Manager
manager=Manager()  实例化Manager类
mydic=manager.dict()
myli=manager.list()

创建的进程可操作mydic和myli
```

### 进程池

##### 基本方法

```
from multiprocessing import Pool

进程池中有两种方法
apply()  同步，一般不使用
apply_async()  异步

pool=Pool(5)  含五个进程的进程池
pool.apply_async(func=func1,args=(....))
从进程池中拿一个进程运行func1
pool.close()关闭进程池，关闭进程池后不能再加进程了
pool.join() 等待进程运行完毕
```

##### 用map

```
pool=Pool()
pool.set(func1,tasks)  tasks是个列表，其中的每个元素作为参数给func1运行
pool.close()
pool.join()
```

