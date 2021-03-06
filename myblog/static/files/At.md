# At

### at的运作方式

at指令将其要执行的工作已文本的形式写入到 **/var/spool/at**目录内

然后等待atd这个服务取用和执行

##### 权限管理

/etc/at.allow和/etc/at.deny两个文件会限制at的使用，如果有at.allow，则只有这个文件里面的使用者才能使用at,其他都不行，如果没有at.allow，只有at.deny,则只有这个文件里面的使用者不能使用at,其他都可以。如果两个文件都没有，则只有root可以用at。at.allow管理较为严格，而at.deny的管理较为松散。

##### 基本指令

```
at [-mldv] TIME
at -c 工作号码
-m		表示当工作完成后，即使没有输出讯息，也发email给使用者
-l		atq -l 相当于atq,列出系统上所有该用户的例程
-d		atq -d 相当于atrm,可以取消一个在at例程中的工作
-v		可以使用较明显的时间格式栏出at例程中的任务栏表
-c		列出工作的实际指令内容

TIME是时间格式： 有
HH:MM		04:20
HH:MM YYYY-MM-DD  		04:20 2020-02-05
HH:MM[am|pm] [Month] [Date] 		  04pm July 21
HH:MM[am|pm] + number [minutes|hours|days|weeks]	04pm + 3 days

```

