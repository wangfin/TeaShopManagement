from django.db import models

# Create your models here.

# 采购单信息
class Purchase_info(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    staff_name = models.CharField(max_length=50)  # 采购员姓名
    merchant_name = models.CharField(max_length=100)  # 商家名称
    merchant_phone = models.CharField(max_length=50)  # 商家电话
    today = models.CharField(max_length=50)  # 采购日期
    estimated_time = models.CharField(max_length=50)  # 预期到货日期
    purchase_status = models.CharField(max_length=10, choices=(('finished', 'finished'), ('unfinished', 'unfinished'), ('error', 'error')))  # 该订单是否已到货，默认未到货
    total_price = models.FloatField()  # 本次订单的总额

# 仓库物品
class Goods(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    #commodity_id = models.CharField(max_length=50)  # 编号id
    commodity_name = models.CharField(max_length=100)  # 采购品名称
    commodity_specification = models.CharField(max_length=100)  # 采购品规格
    commodity_num = models.IntegerField()  # 采购品总数
    commodity_price = models.FloatField()  # 采购品平均单价，这个是要算平均的
    status_level = models.IntegerField()  # 危险警戒线

# 采购物品详情
class Commodity_info(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    #commodity_id = models.CharField(max_length=50)  # 编号id
    commodity_name = models.CharField(max_length=100)  # 采购品名称
    commodity_specification = models.CharField(max_length=100)  # 采购品规格
    commodity_num = models.IntegerField()  # 采购品数量
    commodity_price = models.FloatField()  # 采购品单价
    purchase = models.ForeignKey(Purchase_info, on_delete=models.CASCADE)  # 对应的采购单的外键
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 对应的物品的外键

# 奶茶原有的信息
class Tea_info(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    tea_name = models.CharField(max_length=50)  # 奶茶名称
    tea_cost = models.FloatField()  # 奶茶成本
    tea_price = models.FloatField()  # 奶茶原本售价
    tea_composition = models.CharField(max_length=50)  # 奶茶组成成分

# 奶茶销售订单信息
class Sale_info(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    staff_name = models.CharField(max_length=50)  # 采购员姓名
    today = models.CharField(max_length=50)  # 销售日期
    ismember = models.CharField(max_length=10, choices=(('yes', 'yes'), ('no', 'no')))  # 是否是会员
    discount = models.IntegerField(default=100)  # 额外折扣
    original_price = models.FloatField()  # 原价
    discount_price = models.FloatField()  # 折后总价，最后价格

# 奶茶销售信息
class Sale_tea(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    tea = models.ForeignKey(Tea_info, on_delete=models.CASCADE)  # 对应的奶茶的外键
    tea_name = models.CharField(max_length=50)  # 奶茶名字
    tea_num = models.IntegerField()  # 数量
    tea_sugar = models.CharField(max_length=10, choices=(('free', 'free'), ('normal', 'normal'), ('full', 'full')))  # 奶茶的甜度
    tea_temperature = models.CharField(max_length=10, choices=(('cold', 'cold'), ('normal', 'normal'), ('hot', 'hot')))  # 奶茶的温度
    tea_additional = models.CharField(max_length=50)  # 奶茶额外加料
    total_price = models.FloatField()  # 奶茶实际售价
    sale = models.ForeignKey(Sale_info, on_delete=models.CASCADE)  # 对应的销售单的外键

# 额外加料表
class Tea_addition(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    name = models.CharField(max_length=50)  # 加料名称
    cost = models.FloatField()  # 加料成本
    price = models.FloatField()  # 加料售价
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 对应的物品的外键

# 财务查看，也就是将采购表和销售表拉过来
class Finance(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    time = models.CharField(max_length=50)
    staff_name = models.CharField(max_length=50)
    mode = models.CharField(max_length=10, choices=(('purchase', 'purchase'), ('sales', 'sales')))
    option_id = models.IntegerField()  # 对应的采购单，销售单编号

# 物品进出表
class Goods_inout(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    time = models.CharField(max_length=50)
    staff_name = models.CharField(max_length=50)
    num = models.IntegerField()  # 数量
    mode = models.CharField(max_length=10, choices=(('purchase', 'purchase'), ('sales', 'sales')))
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 对应的物品的外键

# 用户表
class Users(models.Model):
    id = models.AutoField(primary_key=True)  # 自增ID
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    identity = models.CharField(max_length=50)
    avatar = models.CharField(max_length=50)  # 头像的url地址