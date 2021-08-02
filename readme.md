## 解决的问题

1. 跨站脚本攻击（XSS）

    使用`django.middleware.security.SecurityMiddleware`中间件

2. 跨站请求伪造（CSRF）

    使用`django.middleware.csrf.CsrfViewMiddleware`中间件

3. SQL注入

    完全使用ORM进行数据库操作，不存在SQL注入风险

4. 所有数据库操作可能存在的异常 

    使用`try except`捕获，并返回操作失败的提示

5. 删除一条记录后（如删除了某一花名册），再访问与之关联的字段（如使用到该花名册的点名册）均会出错
    
    使用外键（Foreign key）关联字段，并设置 `on_delete=models.CASCADE`
    
6. 扫码公屏再移动设备上访问

   通过userAgent判断设备类型，如果是移动设备则禁止访问
   
7. 对于一些需要持续上传信息的操作（如定位签到、快签等）如果用户中途推出程序，可能会出现奇奇怪怪的问题

   退出时直接中断
   
8. 有些小屁孩不老老实实填学号或者填别人的学号或者帮别人填学号
    
    进行第一次签到后，学号即被记录，不可修改
    
9. 强行关闭一个仍有项目在进行的点名册

   自动关闭下级的所有点名表和一切正在进行的签到，并进入统计流程

10. 小程序打包为单个Package会导致体积过大

    分包，将数据统计相关的代码单独打成SubPackage，默认不下载，只有当使用到统计相关功能的时候才下载代码
   
##未解决的问题
1. 未做负载均衡
2. API没使用token（毕竟是原型）
3. 定位防作弊

## 一些技术栈
### 服务器搭建
- CentOS+Docker
- Docker中跑nginx（http服务器，负责转发请求、端口映射、加载静态资源、负载均衡（这个还没做）） + mysql（数据库） + alpine（linux系统）
- apline中跑django（框架）+uWSGI（Web Service Gateway Interface，Web服务器网关接口，负责python和nginx的通信）
- ssl证书
### 服务器程序
- django
- ORM 使用Django的模型类来操作数据库，提升安全性可靠性（而且方便）
- middleware中间件（这个就是最上面三条，之后可以用来做API token验证）
- requests 一个python的HTTP请求库
- geopy 一个python的地理相关的库。譬如通过经纬度算距离啥的
- element-ui 饿了吗团队出品神级UI框架
- qrcode.js 二维码相关
- axios.js 一个js中的HTTP请求库
### 小程序
- ColorUI 一个CSS样式组件库
- ECharts 一个基于 JavaScript 的开源可视化图表库（在/PackageB/pages/analysis中使用，而且因为其比较大，所以做分包处理）
