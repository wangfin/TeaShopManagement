import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Purchase_info,Commodity_info,Goods,Tea_info,Sale_info,Sale_tea,Tea_addition,Finance,Goods_inout,Users
from collections import Counter
from django.db.models import Q
from django.forms.models import model_to_dict

# Create your views here.

# 显示首页
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'teamanagement/index.html')

# 显示采购单创建页面
def purchase_create(request):
    return render(request, 'teamanagement/purchase_create.html')

# 提交采购单信息
@csrf_exempt
def purchase_input(request):
    if request.method == 'POST':
        # 订单信息
        purchase_data = request.POST.get("purchase_data")
        # 表格内信息
        table_data = request.POST.get("table_data")

        # 将两个进行json序列化
        purchase_data = json.loads(purchase_data)
        table_data = json.loads(table_data)

        # 存入数据库

        # 第一种存入方式
        # 存入purchase_info数据表
        pur = Purchase_info(staff_name=purchase_data['staff_name'],
                            merchant_name=purchase_data['merchant_name'],
                            merchant_phone=purchase_data['merchant_phone'],
                            today=purchase_data['today'],
                            estimated_time=purchase_data['estimated_time'],
                            purchase_status='unfinished',
                            total_price=0.0)
        pur.save(force_insert=True)


        fin = Finance(time=purchase_data['today'],
                      staff_name=purchase_data['staff_name'],
                      mode='purchase',
                      option_id=pur.id)
        fin.save(force_insert=True)

        # 第二种存入方式
        # uq = {'userquestion': user_question, 'question_time': Time}
        #
        # Purchase_info.objects.create(**uq)

        # 这两者等价
        # 存入commodity数据表

        # 总价
        total_price = 0.0

        for data in table_data['data']:

            # 存入commodity的采购详情表中
            commod = Commodity_info(commodity_name=data[0].strip(),
                                    commodity_specification=data[1].strip(),
                                    commodity_num=data[2].strip(),
                                    commodity_price=data[3].strip(),
                                    purchase=Purchase_info.objects.get(id=pur.id),  # 返回新建记录的id
                                    goods=Goods.objects.get(commodity_name=data[0].strip()))  # 外键，这个外键需要传入一个对象，而不是一个id
            commod.save(force_insert=True)
            total_price = total_price + float(data[3].strip()) * int(data[2].strip())


        # print(total_price)

        # 在这之后存入总额
        Purchase_info.objects.filter(id=pur.id).update(total_price=total_price)
            # uq = {'commodity_id': table_data['data'][i][0].strip(),
            #       'commodity_name': table_data['data'][i][1].strip(),
            #       'commodity_specification': table_data['data'][i][2].strip(),
            #       'commodity_num': table_data['data'][i][3].strip(),
            #       'purchase': pur.id}
            #
            # Commodity_info.objects.create(**uq)

        result = {'result': '存入数据库成功！'}

        result_json = json.dumps(result)
        return HttpResponse(result_json)

# 显示采购单信息页面
def purchase_show(request):
    # 在显示页面时，请求数据库
    purchase_info = Purchase_info.objects.all()  # 返回所有的对象
    # 因为本次没有使用json传值，而是使用django自己的内置标签，这个东西和jsp与PHP类似，比较方便
    return render(request, 'teamanagement/purchase_show.html', {'purchase_info': purchase_info})

# 显示订单详情
def purchase_detail(request, purchase_id):
    # 根据purchase_id请求数据库
    purchase_detail = Commodity_info.objects.filter(purchase=purchase_id)  # 返回该id采购单下面的详细内容
    return render(request, 'teamanagement/purchase_detail.html',{'purchase_detail': purchase_detail})

# 删除订单
@csrf_exempt
def purchase_del(request):
    if request.method == 'POST':
        # 订单信息
        purchase_id = request.POST.get("purchase_id")

        # print(purchase_id)
        # 根据purchase_id删除这一条订单
        # 这里可以留一下，只有未确认的订单可以被删除
        Purchase_info.objects.get(id=purchase_id).delete()  # 删除订单
        # Finance 表中的数据也需要删除
        # Q对象复杂查询
        fin = Finance.objects.filter(Q(id=purchase_id) & Q(mode='purchase')).delete()
        print(fin)

        result = {'result': '删除采购单成功！'}
        result_json = json.dumps(result)

        return HttpResponse(result_json)

# 显示仓库确认收货页面
def warehouse_confirm(request):
    # 在显示页面时，请求数据库
    purchase_info = Purchase_info.objects.all()  # 返回所有的对象
    # 因为本次没有使用json传值，而是使用django自己的内置标签，这个东西和jsp与PHP类似，比较方便
    return render(request, 'teamanagement/warehouse_confirm.html', {'purchase_info': purchase_info})

@csrf_exempt
# 确认收货
def purchase_confirm(request):
    if request.method == 'POST':
        # 订单信息
        comfirm_id = request.POST.get("comfirm_id")

        # print(comfirm_id)

        time = Purchase_info.objects.filter(id=comfirm_id).values('today')[0]['today']
        staff_name = Purchase_info.objects.filter(id=comfirm_id).values('staff_name')[0]['staff_name']

        # 确认进货后在inout表单记录
        purchase = Commodity_info.objects.filter(purchase=comfirm_id)
        for pur in purchase:
            pur_dict = model_to_dict(pur)
            # 在仓库确认到货之后才能在仓库增加数额
            # 在仓库表中添加数额
            num = Goods.objects.filter(id=pur_dict['goods']).values('commodity_num')[0]['commodity_num']
            # print(num)
            Goods.objects.filter(id=pur_dict['goods']).update(commodity_num=num + pur.commodity_num)

            # 货物进出表
            inout = Goods_inout(time=time,
                                staff_name=staff_name,
                                num=pur.commodity_num,
                                mode='purchase',
                                goods=Goods.objects.get(id=pur_dict['goods']))
            inout.save(force_insert=True)

        # 确认订单
        Purchase_info.objects.filter(id=comfirm_id).update(purchase_status='finished')

        result = {'result': '仓库确认收货成功！'}
        result_json = json.dumps(result)

        return HttpResponse(result_json)

@csrf_exempt
# 订单有误
def purchase_wrong(request):
    if request.method == 'POST':
        # 订单信息
        wrong_id = request.POST.get("wrong_id")

        Purchase_info.objects.filter(id=wrong_id).update(purchase_status='error')

        result = {'result': '确认订单有误！'}
        result_json = json.dumps(result)

        return HttpResponse(result_json)

# 仓库进货查看
def warehouse_goodscheck(request):
    goods_info = Goods.objects.all()  # 返回所有的对象
    return render(request, 'teamanagement/warehouse_goodscheck.html', {'goods_info': goods_info})

# 采购品进出记录查询
def warehouse_goodsdetail(request, goods_id):
    # 根据goods_id 查询 采购单和销售单
    inout_info = Goods_inout.objects.filter(goods=goods_id)
    return render(request, 'teamanagement/warehouse_goodsdetail.html', {'inout_info': inout_info})

# 显示销售单创建页面
def sales_create(request):
    tea_info = Tea_info.objects.all()
    addition_info = Tea_addition.objects.all()
    return render(request, 'teamanagement/sales_create.html', {'tea_info': tea_info, 'addition_info': addition_info})

# 买一杯奶茶时的检查程序
@csrf_exempt
def tea_buy(request):
    if request.method == 'POST':
        '''
            这边不仅仅需要处理刚刚添加的这个奶茶
            而是要考虑到和之前的奶茶加在一起的用料会不会超过仓库
        '''
        # 奶茶信息
        tea = request.POST.get("tea_info")
        tea = json.loads(tea)

        # 原先已有的奶茶
        table_data = request.POST.get("table_data")
        table_data = json.loads(table_data)

        '''
            
            这边需要处理几个逻辑
            1.获取了奶茶的名字，数量，添加的料。
            2.就是要计算仓库内的物品是否够用。（奶茶的名字可以获取到用料 + 加料） * 数量 = 用的材料总数
            看看仓库够不够，如果不够报出提示，仓库缺货，无法添加奶茶
            3.就是计算总价了，根据奶茶的名字+加料 * 杯数，算出这一次的单价
            4.表单尾的总价也要更新
            {'tea_name': '椰果奶茶', 'tea_addition': ['椰果', '红豆'], 'tea_num': '1'}
            
        '''

        # 获取该奶茶的用料
        compos = Tea_info.objects.filter(tea_name=tea['tea_name']).values('tea_composition')[0]['tea_composition']
        # 在数据库中，这段是使用.来分割的
        composition = compos.split('.')

        # 获取辅料
        addition = []
        for add in tea['tea_addition']:
            addition.append(Tea_addition.objects.filter(name=add).values('goods')[0]['goods'])

        # 计算之前的表格中的数据
        old_composition = []
        old_addition = []
        old_sum = []
        for data in table_data['data']:
            # 获取组成原料
            old_com = Tea_info.objects.filter(tea_name=data[0].strip()).values('tea_composition')[0]['tea_composition']
            old_coms = old_com.split('.')
            old_composition = old_composition + old_coms

            # 加料
            if data[2] != '':
                old_adds = data[2].strip().split(',')
                for old_add in old_adds:
                    old_addition.append(Tea_addition.objects.filter(name=old_add).values('goods')[0]['goods'])

            old_composition = list(map(int, old_composition))
            # 乘上奶茶的数量
            old_sum = (old_composition + old_addition) * int(data[1])

        #print('原有的'+str(old_sum))


        # 计算总价
        sum_price = 0
        tea_price = Tea_info.objects.filter(tea_name=tea['tea_name']).values('tea_price')[0]['tea_price']
        for add in tea['tea_addition']:
            adddition_price = Tea_addition.objects.filter(name=add).values('price')[0]['price']
            sum_price = sum_price + adddition_price

        sum_price = (sum_price + tea_price) * int(tea['tea_num'])

        # com 中的字符串转换成数字
        composition = list(map(int, composition))

        # 将两个数组合并，方便统计
        # 算上数量
        new_sum = (composition + addition) * int(tea['tea_num'])
        #print('新的'+str(new_sum))

        sum = new_sum + old_sum
        #print('全部的'+str(sum))
        # 统计list中元素出现的次数，结果为dict{1: 3, 2: 2, 3: 1}
        goods_sum = Counter(sum)
        # for i in goods_sum.keys():
        # # 还要乘以数量
        #     goods_sum[i] = goods_sum[i] * int(tea['tea_num'])
        #print(goods_sum)

        # 使用统计好的用料去仓库中进行对比
        # 使用key去对比

        # 判断状态的 flag，只有全部的循环结束了，才能进行操作
        flag = False
        for key in goods_sum.keys():
            # 原来的数量
            origin_num = Goods.objects.filter(id=key).values('commodity_num')[0]['commodity_num']
            # 本次需要的数量
            need_num = goods_sum[key]
            # 剩余的数量
            remain_num = origin_num - need_num
            # print(remain_num)
            if remain_num >= 0:
                flag = True
            else:
                flag = False
                break

        # print(flag)

        if flag:
            result = {'flag': 'true', 'sum_price': sum_price, 'result': '确认订单正确！'}
            result_json = json.dumps(result)
        else:
            result = {'flag': 'false', 'sum_price': sum_price, 'result': '材料不足，已提醒进行采购！'}
            result_json = json.dumps(result)

        return HttpResponse(result_json)

# 提交销售单信息
@csrf_exempt
def sales_input(request):
    if request.method == 'POST':
        # 订单信息
        sales_data = request.POST.get("sales_data")
        # 表格内信息
        table_data = request.POST.get("table_data")

        # 将两个进行json序列化
        sales_data = json.loads(sales_data)
        table_data = json.loads(table_data)

        # 数据库操作
        sale = Sale_info(today=sales_data['today'],
                         staff_name=sales_data['staff_name'],
                         ismember=sales_data['ismember'],
                         discount=sales_data['discount'],
                         original_price=float(sales_data['origin_price']),
                         discount_price=float(sales_data['discount_price'])
                        )
        sale.save(force_insert=True)

        fin = Finance(time=sales_data['today'],
                      staff_name=sales_data['staff_name'],
                      mode='sales',
                      option_id=sale.id)
        fin.save(force_insert=True)

        composition = []
        addition = []

        for data in table_data['data']:
            '''
                先获取全部的数据，将数据存入数据表中
                在去仓库表中去减去相应的数字
            '''
            # 存入数据库
            tea = Sale_tea(tea=Tea_info.objects.get(tea_name=data[0].strip()),
                           tea_name=data[0].strip(),
                           tea_num=data[1].strip(),
                           tea_temperature=data[2].strip(),
                           tea_sugar=data[3].strip(),
                           tea_additional=data[4].strip(),
                           total_price=float(data[5].strip()),
                           sale=Sale_info.objects.get(id=sale.id)
                        )
            tea.save(force_insert=True)

            # 去仓库中减去对应的数量

            # 获取组成原料
            com = Tea_info.objects.filter(tea_name=data[0].strip()).values('tea_composition')[0]['tea_composition']
            coms = com.split('.')
            composition = composition + coms

            # 加料
            if data[4] != '':
                adds = data[4].strip().split(',')
                for add in adds:
                    addition.append(Tea_addition.objects.filter(name=add).values('goods')[0]['goods'])

            composition = list(map(int, composition))
            # 乘上奶茶的数量
            sum = (composition + addition) * int(data[1])
            goods_sum = Counter(sum)

            for key in goods_sum.keys():
                # 原来的数量
                origin_num = Goods.objects.filter(id=key).values('commodity_num')[0]['commodity_num']
                # 本次需要的数量
                need_num = goods_sum[key]
                # 剩余的数量
                remain_num = origin_num - need_num
                # print(remain_num)
                # 可以进行实际操作
                Goods.objects.filter(id=key).update(commodity_num=remain_num)

                # 对物品进出表进行插入
                inout = Goods_inout(time=sales_data['today'],
                                    staff_name=sales_data['staff_name'],
                                    mode='sales',
                                    num=need_num,
                                    goods=Goods.objects.get(id=key)
                                    )
                inout.save(force_insert=True)

        result = {'result': '提交订单正确！'}
        result_json = json.dumps(result)

        return HttpResponse(result_json)

# 显示销售单页面
def sales_show(request):
    sales_info = Sale_info.objects.all()
    return render(request, 'teamanagement/sales_show.html', {'sales_info': sales_info})

# 采购单详细信息
def sales_detail(request, sales_id):
    # 根据goods_id 查询 采购单和销售单
    sales_info = Sale_tea.objects.filter(sale=sales_id)

    return render(request, 'teamanagement/sales_detail.html', {'sales_info': sales_info})

# 销售部的显示
def finance_show(request):

    finance_info = Finance.objects.all()
    return render(request, 'teamanagement/finance_show.html', {'finance_info': finance_info})

# 登录页面显示
def login_show(request):

    return render(request, 'teamanagement/login.html')

# 登陆
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 用户名
        username = request.POST.get("username")
        # 密码
        password = request.POST.get("password")

        user = Users.objects.get(username=username)

        if user.password == password:
            result = {'result': '登陆成功！'}
            request.session['username'] = user.username
            request.session['identity'] = user.identity

        else:
            result = {'result': '账户或密码错误！'}

        result_json = json.dumps(result)

        return HttpResponse(result_json)

# 登出
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        del request.session['username']
        del request.session['identity']

        result = {'result': '登出成功！'}

        result_json = json.dumps(result)

        return HttpResponse(result_json)

# 销售部详细信息
# def finance_detail(request, sales_id):
#     # 根据goods_id 查询 采购单和销售单
#     sales_info = Sale_tea.objects.filter(sale=sales_id)
#
#     return render(request, 'teamanagement/sales_detail.html', {'sales_info': sales_info})








