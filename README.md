# TeaShopManagemant
奶茶店的管理系统

### 项目简介

奶茶店管理系统，课设任务。管理系统大都大同小异，都是由一些用于管理的功能形成的。本不想做这个管理系统的，但是这个算是做了这么长时间的管理系统的一个总结之作，本项目综合运用了多种技术。

### 技术框架

这次的管理系统还是做的web系统，用的Python。

后台框架：Django

前端：国外大佬做的前端管理模版adminTO，非常的简洁美观而且功能齐全。主要用的全是基于jquery和boostrap，然后在这两个上面进阶开发的各种组件。（这是在国外是收费的，前端的HTML在模板文件夹中，相应的静态文件在teamaangement/static/teamanagement下面）

这一次使用Django基本上是把Django中一些常见的功能全都进行了使用，算是对这么长时间使用django的一次总结使用

Django的urls、views、models、template、static file基本上都是按照了官网的标准用法，也进行了一些以前没有使用过的的用法的使用。

本次项目遇到的最大的困难，也是最大的收获都在前端。前端的Jquery的使用一是复习了一遍，二是对以前不太清楚的也进行了实际的练习，以前不知道的这次也知道了。

### 版本

好像原先没说版本的问题，这里提一下

django，当时好像是用的2.x的版本，最好是2.1

PyMysql，0.93版本

### 功能介绍

用户一开始提出了几个部门要求，而具体的功能就是基于这几个部门的。
部门如下：
1. 采购部
2. 销售部
3. 仓库
4. 财务部
5. 人事部

每个部门的具体功能是我自己想的，但也就是一些基础功能，毕竟用户没有提出具体的要求，我也没有什么开店的经验，所以每个部门都是常见的功能。

### 具体的功能和界面

#### 首页

首页本来想的是做一个图表页面的，上面展示了各种数据页面，都是以图表的形式展现的。预期设想了包括会员数量、财务进账、支出、增长比等一系列数据的图表展示。但是因为时间有限没有做这个。

整个首页都是以图片墙的形式展现的奶茶的图片，如下：

![首页](https://github.com/wangfin/TeaShopManagement/raw/master/pic/首页.png)

首页以后可以再进行改进，增加功能！！！

#### 采购部

采购部的功能就很简单，采购物品，查看采购单

采购物品中上部分是必要的信息填写，下半部分是添加采购的物品，下方的表格是可以在表格内修改的（在这里是有个小bug的，就是在第一个格子**输入采购物品名称的时候千万不能输错**，不然在仓库无法对相应的采购品进行数量的增加）

页面如下：

![采购单创建](https://github.com/wangfin/TeaShopManagement/raw/master/pic/采购单创建.png)

![表格](https://github.com/wangfin/TeaShopManagement/raw/master/pic/可修改表格.png)

采购单查看页面就是普通的数据表格Datatable，最后一排的左边的按钮可以查看采购单的详细内容，第二个按钮可以进行订单的删除（在仓库确认收货之后不可以删除订单）

页面如下：

![采购单查看页面](https://github.com/wangfin/TeaShopManagement/raw/master/pic/采购单查看.png)

![采购单详细信息页面](https://github.com/wangfin/TeaShopManagement/raw/master/pic/采购详细信息.png)

#### 仓库

仓库的功能就是确认订单已经到货、查看仓库物品

确认订单到货是为了确认订单采购的物品已经到仓库了。如果到了就点击确认到货，确认后仓库物品的数量才能进行相应的增加。如果订单有误就点击订单有误按钮，有误订单只能进行删除后重新创建。

页面如下：

![仓库确认到货](https://github.com/wangfin/TeaShopManagement/raw/master/pic/仓库确认订单.png)

仓库查看物品的数量等信息，也可以查看某个物品的具体进货出货信息

页面如下：

![仓库物品查看](https://github.com/wangfin/TeaShopManagement/raw/master/pic/仓库物品查看.png)

![物品详细进出](https://github.com/wangfin/TeaShopManagement/raw/master/pic/仓库物品详细进出查看.png)

#### 销售部

销售部功能为：销售奶茶、查看销售记录

销售页面上部分为必要信息填写，如销售员信息、是否为会员（出示会员卡打8折）、是否有额外的折扣。下半部分为奶茶的表格，在选择完具体的奶茶后，下方表格会计算出具体的价格，显示原价，总价（折后价）。在添加奶茶时，如果仓库物品不足，会进行提示并禁止添加该奶茶。

页面如下：


![订单创建](https://github.com/wangfin/TeaShopManagement/raw/master/pic/订单创建.png)

![选择奶茶](https://github.com/wangfin/TeaShopManagement/raw/master/pic/添加奶茶.png)

查看销售记录就是查看销售的信息，同采购部相同，也可以查看具体的某一个销售信息。

页面如下

![订单查看](https://github.com/wangfin/TeaShopManagement/raw/master/pic/销售单查看.png)

#### 财务部

财务部的功能就是查看每一笔的支出项和收入项。之前还想过要加一个支出/收入创建的功能，用来记录非采购/销售之外的收入/支出（额外收入/支出，如广告支出等），但因为时间不足未实现。也可以查看某一个详细的信息。

页面如下：

![财务部页面](https://github.com/wangfin/TeaShopManagement/raw/master/pic/财务部的进出项查看.png)


#### 人事部

人事部因时间关系没有做，预期设想的功能为，创建会员、查看会员；创建员工、查看员工、员工职务信息更改等


#### 登陆

![登陆](https://github.com/wangfin/TeaShopManagement/raw/master/pic/登陆.png)


#### sweet alert

本项目所有的alert，都是用的这种alert，很好看。

![sweet alert](https://github.com/wangfin/TeaShopManagement/raw/master/pic/sweetalert.png)


### 未上线功能

本来想做各种可视化图表、还想做数据的预测之类的，但都没有实现。

### 总结

隔了一年看了下这个项目，确实是真的简陋，很多的小细节没有处理好，然后有一些功能也不完善，业务逻辑也不怎么合理。

然后有些代码我自己看了都不知道是要用来做什么的。
因为当时在就是一边写一边出现bug，然后就是为了解决bug而添加了一些临时性的补救代码，所以现在看来感觉也不知道当时怎么想的。
但是这个项目可以操作的地方还是挺多的，可以继续改善。


