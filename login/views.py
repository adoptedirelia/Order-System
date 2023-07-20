from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql
from datetime import date,datetime
import os 
global global_table
global_table = ''


def savesql():
    command = f'mysqldump -u root -p 12345678 --all-databases > "/Users/savannasilver/Desktop/program/vscode/mysql/ai.sql"'
    os.system(command)


def show_res(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(f"Username: {username}\nPassword: {password}\n")
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    #table_name = request.form['table_name']

    sql = f"select passwd from account where id = '{username}'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()

    sql = f"select career from user where id = '{username}'"
    cursor.execute(sql)
    #print(cursor.fetchall())
    pro = cursor.fetchall()
    car = pro[0][0]

    if data and data[0][0] == password:
        print("#################################")
        cursor.execute(f"describe user")
        model_code = cursor.fetchall()
        #print(model_code)
        cursor.execute(f"SELECT * FROM restaurant order by level desc")
        data = cursor.fetchall()
        print(data)
        #len2 = len(data)
        #index = [i for i in range(1,len2+1)]
        #print(index)
        cursor.close()
        savesql()
        if car != 'admin':
            return render(request,'show_res.html',{'data':data,'username':username,'career':car})
        else:
            return render(request,'index.html',{'username':username,'career':car})
    
    else:
        return HttpResponse("404 error")
# 信息管理页面
def index(request):
    #return HttpResponse('hello world')
    return render(request,'index.html')

# 打开注册页面
def register(request):
    #return HttpResponse('hello world')
    return render(request,'register.html')

# 打开登录页面
def login(request):
    #return HttpResponse('hello world')
    return render(request,'login.html')

# 打开修改密码页面
def changepwd(request):
    #return HttpResponse('hello world')
    return render(request,'change_passwd.html')


# 登录，然后转到管理页面
# 首先读取账号密码
# 如果正确则转入对应界面
# 否则无法进入
def login_data(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(f"Username: {username}\nPassword: {password}\n")
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    #table_name = request.form['table_name']

    sql = f"select passwd from account where id = '{username}'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()

    sql = f"select career from user where id = '{username}'"
    cursor.execute(sql)
    #print(cursor.fetchall())
    pro = cursor.fetchall()
    car = pro[0][0]

    if data and data[0][0] == password:
        print("#################################")
        if car == 'admin':
            cursor.execute(f"describe user")
            model_code = cursor.fetchall()
            #print(model_code)
            cursor.execute(f"SELECT * FROM user")
            data = cursor.fetchall()
            #len2 = len(data)
            #index = [i for i in range(1,len2+1)]
            #print(index)
            cursor.close()
            global global_table
            global_table = 'user'
            add = 0
            modify = 0
            savesql()

            return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username})
        
        else: 
            return HttpResponse("权限不足")
    
    else:
        return HttpResponse("404 error")


# 管理页面 展示数据
def showtable(request):
    username = request.POST.get('username')
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    table_name = request.POST.get('table_name')
    #print(table_name)
    cursor.execute(f"describe {table_name}")
    model_code = cursor.fetchall()
    #print(model_code)
    cursor.execute(f"CALL SelectDataFromTable('{table_name}')")
    data = cursor.fetchall()
    cursor.close()
    global global_table
    global_table = table_name
    add =0
    modify = 0
    savesql()

    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username})

# 管理页面 进行修改的操作
def modify(request):
    username = request.GET.get('username')
    id = request.GET.get('id')
    print(id)
    id2 = request.GET.get('id2')
    print(id2)

    label1 = request.GET.get('label1')
    print(label1)
    label2 = request.GET.get('label2')
    print(label2)

    #print("I am test")
    global global_table
    print(global_table)
    #print(global_table)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    ###
    cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    value = ''
    # 找data
    index = 1
    for row in data:
        #print(row[0],id)
        
        if row[0] == id[1:-1] and row[1] == id2[1:-1]:
            
            print('yes')
            value = row
            break
        index +=1

    #index = [i for i in range(len(model_code))]
    

    sql = f"delete from {global_table} where {label1[1:-1]}={id} and {label2[1:-1]}={id2}"
    #print(sql)
    #cursor.execute(sql)
    #cnx.commit()

    cursor.execute(f"describe {global_table}")
    model_code = cursor.fetchall()
    #print(model_code)
    cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    add = 0
    modify = 1
    pack = zip(value,model_code)
    savesql()
    
    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'pack':pack,'index':index,'username':username[1:-1]})

def modify_data(request):
    print("######################")
    username = request.POST.get('username')
    global global_table
    print(global_table)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    cursor.execute(f"describe {global_table}")
    model_code = cursor.fetchall()
    #print(model_code)
    #
    # print(request.POST['index'])

    idx1 = model_code[0][0]
    idx2 = model_code[1][0]
    print(idx1,idx2)

    ii = int(request.POST['index'])
    cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    print(data[ii-1])
    idx1_data = data[ii-1][0]
    idx2_data = data[ii-1][1]
    print(idx1_data,idx2_data)
    
    
    index = -2
    for i in request.POST:
        index +=1
        if index == 0 or index == -1:
            continue
        if i == 'index':
            break
        data = request.POST.get(i)
        print(data)
        #print(model_code[index-1][0],data)
        #sql = f"update {global_table} set {model_code[index-1][0]}='{data}' where {idx1}='{idx1_data}' and {idx2}='{idx2_data}'"
        #data = f"'{data}'"

        #sql = f'CALL UpdateDataInTable("{global_table}", "{model_code[index-1][0]}={data}", "{idx1}={idx1_data} and {idx2}={idx2_data}");'

        #print(sql)
        #cursor.execute(sql)
        #print((f"{global_table}", f"{model_code[index-1][0]}='{data}'", f"{idx1}='{idx1_data}' and {idx2}='{idx2_data}'"))
        cursor.callproc('UpdateDataInTable',(f"{global_table}", f"{model_code[index-1][0]}='{data}'", f"{idx1}='{idx1_data}' and {idx2}='{idx2_data}'"))
        cnx.commit()

        if index == 1:
            idx1_data = data
        
        if index == 2:
            idx2_data = data

    #print(model_code)
    cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    add = 0
    modify = 0
    savesql()

    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username[1:-1]})

# 管理页面 进行插入的操作，打开插入的功能
def insert(request):
    username = request.GET.get('username')

    #print("I am test")
    global global_table
    print(global_table)
    #print(global_table)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    cursor.execute(f"describe {global_table}")
    model_code = cursor.fetchall()
    #print(model_code)
    cursor.execute(f"SELECT * FROM {global_table}")

    data = cursor.fetchall()
    add = 1
    modify = 0
    savesql()

    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username[1:-1]})



# 管理页面 插入数据
def insert_data(request):
    username = request.POST.get('username')

    #print("I am test")
    global global_table
    print(global_table)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    index = -1
    data = ""
    for i in request.POST:
        index +=1
        if index == 0 or index == 1:
            continue

        data = data + f'"{request.POST.get(i)}"' + ","
        
    #try:
    #    cursor.execute(sql)
    #    cnx.commit()
    #except pymysql.err.Error as e:
    #    return HttpResponse(e)
    
    cursor.execute(f"describe {global_table}")
    model_code = cursor.fetchall()
    #print(model_code)
    print(data)

    cursor.callproc("InsertDataIntoTable",(f"{global_table}",data[:-1]))
    cnx.commit()

    aff = cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    add = 0
    modify = 0
    savesql()

    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username[1:-1]})


# 管理页面 删除数据
def delete(request):
    username = request.GET.get('username')

    id = request.GET.get('id')
    print(id)
    id2 = request.GET.get('id2')
    print(id2)

    label1 = request.GET.get('label1')
    print(label1)
    label2 = request.GET.get('label2')
    print(label2)
    global global_table
    print(global_table)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    #sql = f"delete from {global_table} where {label1[1:-1]}={id} and {label2[1:-1]}={id2}"

    cursor.callproc('DeleteDataFromTable',(f"{global_table}", f"{label1[1:-1]}={id} and {label2[1:-1]}={id2}"))
    cnx.commit()
    
    cursor.execute(f"describe {global_table}")
    model_code = cursor.fetchall()
    #print(model_code)
    cursor.execute(f"SELECT * FROM {global_table}")
    data = cursor.fetchall()
    cursor.close()
    add = 0
    modify = 0
    savesql()

    return render(request,'index.html',{'data':data,'model_code':model_code,'add':add,'modify':modify,'username':username[1:-1]})


# 注册页面
# 输入内容，并且插入数据库
def register_data(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    name = request.POST.get('fullname')
    gender = request.POST.getlist('gender')
    age = request.POST.get('age')
    career = request.POST.get('career')
    print(f"Username: {username}\nPassword: {password}\nEmail: {email}\nPhone: {phone}\nname: {name}\ngender: {gender[0]}\nage: {age}\ncareer: {career}")
    
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    sql = f"insert into account values('{username}',{password},'{email}',{phone})"
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    sql = f"insert into user values('{username}','{name}','1','{gender[0]}','{career}','{age}')"
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    cursor.close()
    return render(request,'login.html')

# 改变数据库的内容
def change_data(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    newpassword = request.POST.get('newpassword')
    print(f"Username: {username}\nPassword: {password}\nNew Password: {newpassword}")

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    #table_name = request.form['table_name']
    #判断密码
    sql = f"select passwd from account where id = '{username}'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()

    if data and data[0][0] == password:
        sql = f"update account set passwd = {newpassword} where id = '{username}'"
        cursor.execute(sql)
        cnx.commit()
        savesql()

        return render(request,'login.html')
    
    else: 
        return HttpResponse("404 error")

def show_comment(request):
    id = request.GET.get('id')
    username = request.GET.get('username')
    career = request.GET.get('career')

    print(id)

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    
    sql = f'select * from comment where restaurant_id = {id} order by star desc'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    savesql()
    return render(request,'show_comment.html',{'data':data,'username':username[1:-1],'career':career[1:-1]})

def comment(request):
    username = request.POST.get('username')
    career = request.POST.get('career')

    restaurant = request.POST.get('res')
    score = request.POST.get('score')
    comment = request.POST.get('comment')

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    
    sql = f"select * from comment"
    cursor.execute(sql)
    indexn = len(cursor.fetchall())
    print(indexn)

    sql = f'insert into comment values("c{indexn}","{username}","{restaurant}",{score},"{date.today()}","{comment}")'
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    sql = f'select * from comment where restaurant_id = "{restaurant}" order by star desc'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(restaurant,score,comment,username)
    savesql()
    return render(request,'show_comment.html',{'data':data,'username':username,'career':career})

def delete_comment(request):
    id = request.GET.get('id')
    username = request.GET.get('username')
    career = request.GET.get('career')

    restaurant = request.GET.get('res')
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    


    sql = f'delete from comment where comment_id = {id}'
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    sql = f'select * from comment where restaurant_id = "{restaurant}"'
    
    cursor.execute(sql)
    data = cursor.fetchall()
    savesql()
    return render(request,'show_comment.html',{'data':data,'username':username[1:-1],'career':career[1:-1]})


def check_all(request):
    id = request.GET.get('id')
    username = request.GET.get('username')
    career = request.GET.get('career')

    print(id)

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    
    sql = f'select * from comment order by star desc'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    savesql()
    return render(request,'show_comment.html',{'data':data,'username':username[1:-1],'career':career[1:-1]})

def buy(request):
    id = request.GET.get('id')[1:-1]
    username = request.GET.get('username')
    career = request.GET.get('career')

    res = request.GET.get('res')
    data = 1
    print(id,username,res)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()

    sql = f"select * from rm where restaurant_id = '{id}'"
    print(sql)
    cursor.execute(sql)
    tmp = cursor.fetchall()
    print(tmp)
    data = []
    for i in tmp:
        meal = i[1]
        sql = f"select * from meal where id = '{meal}'"
        cursor.execute(sql)
        tmp2 = cursor.fetchall()[0]
        #print(tmp2)
        data.append(tmp2)
    savesql()

    return render(request,'order.html',{'data':data,'username':username[1:-1],'career':career[1:-1],'res':res,'id':id})

def show_comment_page(request):
    return render(request,'show_comment.html')

def tomindex(request):
    username = request.GET.get('username')
    career = request.GET.get('career')

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM restaurant order by level desc")
    data = cursor.fetchall()
    savesql()
    return render(request,'show_res.html',{'data':data,'username':username[1:-1],'career':career[1:-1]})

def myorder(request):
    return render(request,'pinfo.html')


def show_order(request):
    a = request.POST.getlist('quantity')
    username = request.POST.get('username')
    career = request.POST.get('career')

    id = request.POST.get('id')
    now_date = date.today()
    tmp_time = datetime.now()
    now_time = f'{int(tmp_time.hour)+8}:{tmp_time.minute}:{tmp_time.second}'

    print(a,username,id)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    sql = f"select * from rm where restaurant_id = '{id}'"
    print(sql)
    cursor.execute(sql)
    tmp = cursor.fetchall()
    total_price = 0
    meal_num = {}
    for index,i in enumerate(tmp):
        meal_id = i[1]
        sql = f"select * from meal where id = '{meal_id}'"
        cursor.execute(sql)
        info = cursor.fetchall()[0]
        price = float(info[2])
        
        if int(a[index]) == 0:
            continue
        
        meal_num[meal_id] = int(a[index])

        total_price += price*int(a[index])
        print(info,price)

    sql = f"select * from myorder"
    cursor.execute(sql)
    num = len(cursor.fetchall())
    print(num)
    
    sql = f"insert into myorder values('o{num}','{now_date}',TIME('{now_time}'),0)"
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    sql = f"insert into ore values('o{num}','{id}')"
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    sql = f"insert into ou values('o{num}','{username}',{total_price})"
    print(sql)
    cursor.execute(sql)
    cnx.commit()

    for i in meal_num:
        sql = f"insert into om values('o{num}','{i}','{meal_num[i]}')"
        print(sql)
        cursor.execute(sql)
        cnx.commit()

    print(f"总共花费{total_price}元")

    # 找到对应的user的订单号然后全部输出即可

    data = []

    sql = f"select * from ou where user_id = '{username}'"

    cursor.execute(sql)
    
    all = cursor.fetchall()

    for item in all:
        order_id = item[0]
        sdata = [order_id]

        sql = f"select * from ore where order_ID = '{order_id}'"

        cursor.execute(sql)
        res_id = cursor.fetchall()[0][1]
        sql = f"select * from restaurant where ID = '{res_id}'"
        cursor.execute(sql)
        res = cursor.fetchall()[0][1]
        sdata.append(res)

        #sdata.append("hello")

        sql = f"select * from om where order_ID = '{order_id}'"
        cursor.execute(sql)
        contain = cursor.fetchall()
        
        #sdata.append(contain)
        sent = []
        for i in contain:
            sql = f"select * from meal where ID = '{i[1]}'"
            cursor.execute(sql)
            ans = cursor.fetchall()[0]

            sent.append(f"菜名:{ans[1]}\t单价:{ans[2]}\t数量:{i[2]}")
            
        sdata.append(sent)

        sql = f"select * from ou where order_ID = '{order_id}' "
        cursor.execute(sql)
        price = cursor.fetchall()[0][2]
        sdata.append(price)

        sql = f"select * from myorder where ID = '{order_id}' "
        cursor.execute(sql)
        acc = cursor.fetchall()[0][3]
        sdata.append(acc)

        data.append(sdata)
    data = sorted(data, key=lambda x: x[-1])
    savesql()
    return render(request,'all_order.html',{'data':data,'username':username,'career':career})


def show_order2(request):
    username = request.GET.get('username')[1:-1]
    career = request.GET.get('career')[1:-1]

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()
    data = []

    sql = f"select * from ou where user_id = '{username}'"

    cursor.execute(sql)
    
    all = cursor.fetchall()

    for item in all:
        order_id = item[0]
        sdata = [order_id]

        sql = f"select * from ore where order_ID = '{order_id}'"

        cursor.execute(sql)
        res_id = cursor.fetchall()[0][1]
        sql = f"select * from restaurant where ID = '{res_id}'"
        cursor.execute(sql)
        res = cursor.fetchall()[0][1]
        sdata.append(res)

        #sdata.append("hello")

        sql = f"select * from om where order_ID = '{order_id}'"
        cursor.execute(sql)
        contain = cursor.fetchall()
        
        #sdata.append(contain)
        sent = []
        for i in contain:
            sql = f"select * from meal where ID = '{i[1]}'"
            cursor.execute(sql)
            ans = cursor.fetchall()[0]

            sent.append(f"菜名:{ans[1]}\t单价:{ans[2]}\t数量:{i[2]}")
            
        sdata.append(sent)

        sql = f"select * from ou where order_ID = '{order_id}' "
        cursor.execute(sql)
        price = cursor.fetchall()[0][2]
        sdata.append(price)

        sql = f"select * from myorder where ID = '{order_id}' "
        cursor.execute(sql)
        acc = cursor.fetchall()[0][3]
        sdata.append(acc)

        data.append(sdata)

    data = sorted(data, key=lambda x: x[-1])
    print(username)
    savesql()
    return render(request,'all_order.html',{'data':data,'username':username,'career':career})


def delete_order(request):
    username = request.GET.get('username')[1:-1]
    career = request.GET.get('career')[1:-1]

    id = request.GET.get('id')
    print(username,id)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()   

    sql = f"delete from myorder where id = {id}"
    cursor.execute(sql)
    cnx.commit()


    data = []

    sql = f"select * from ou where user_id = '{username}'"

    cursor.execute(sql)
    
    all = cursor.fetchall()

    for item in all:
        order_id = item[0]
        sdata = [order_id]

        sql = f"select * from ore where order_ID = '{order_id}'"

        cursor.execute(sql)
        res_id = cursor.fetchall()[0][1]
        sql = f"select * from restaurant where ID = '{res_id}'"
        cursor.execute(sql)
        res = cursor.fetchall()[0][1]
        sdata.append(res)

        #sdata.append("hello")

        sql = f"select * from om where order_ID = '{order_id}'"
        cursor.execute(sql)
        contain = cursor.fetchall()
        
        #sdata.append(contain)
        sent = []
        for i in contain:
            sql = f"select * from meal where ID = '{i[1]}'"
            cursor.execute(sql)
            ans = cursor.fetchall()[0]

            sent.append(f"菜名:{ans[1]}\t单价:{ans[2]}\t数量:{i[2]}")
            
        sdata.append(sent)

        sql = f"select * from ou where order_ID = '{order_id}' "
        cursor.execute(sql)
        price = cursor.fetchall()[0][2]
        sdata.append(price)

        sql = f"select * from myorder where ID = '{order_id}' "
        cursor.execute(sql)
        acc = cursor.fetchall()[0][3]
        sdata.append(acc)
        print(sdata)

        data.append(sdata)
    
    print(username)
    data = sorted(data, key=lambda x: x[-1])
    savesql()
    return render(request,'all_order.html',{'data':data,'username':username,'career':career})

def update_order(request):
    username = request.GET.get('username')[1:-1]
    career = request.GET.get('career')[1:-1]

    id = request.GET.get('id')
    print(username,id)
    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()   

    sql = f"update myorder set acc = 1 where id = {id}"
    cursor.execute(sql)
    cnx.commit()


    data = []

    sql = f"select * from ou where user_id = '{username}'"

    cursor.execute(sql)
    
    all = cursor.fetchall()

    for item in all:
        order_id = item[0]
        sdata = [order_id]

        sql = f"select * from ore where order_ID = '{order_id}'"

        cursor.execute(sql)
        res_id = cursor.fetchall()[0][1]
        sql = f"select * from restaurant where ID = '{res_id}'"
        cursor.execute(sql)
        res = cursor.fetchall()[0][1]
        sdata.append(res)

        #sdata.append("hello")

        sql = f"select * from om where order_ID = '{order_id}'"
        cursor.execute(sql)
        contain = cursor.fetchall()
        
        #sdata.append(contain)
        sent = []
        for i in contain:
            sql = f"select * from meal where ID = '{i[1]}'"
            cursor.execute(sql)
            ans = cursor.fetchall()[0]

            sent.append(f"菜名:{ans[1]}\t单价:{ans[2]}\t数量:{i[2]}")
            
        sdata.append(sent)

        sql = f"select * from ou where order_ID = '{order_id}' "
        cursor.execute(sql)
        price = cursor.fetchall()[0][2]
        sdata.append(price)

        sql = f"select * from myorder where ID = '{order_id}' "
        cursor.execute(sql)
        acc = cursor.fetchall()[0][3]
        sdata.append(acc)

        data.append(sdata)

    print(username)
    data = sorted(data, key=lambda x: x[-1])
    savesql()
    return render(request,'all_order.html',{'data':data,'username':username,'career':career})

def pinfo(request):
    username = request.GET.get('username')
    career = request.GET.get('career')

    cnx = pymysql.connect(user='root', password='12345678', host='localhost', database='AI')
    cursor = cnx.cursor()   
    data = []
    sql = f"select * from account where id = {username}"

    cursor.execute(sql)
    tmp = cursor.fetchall()[0]
    data.append(tmp[2]) #邮箱
    data.append(tmp[3]) #电话

    print(tmp)

    sql = f"select * from user where id = {username}"

    cursor.execute(sql)
    tmp = cursor.fetchall()[0]
    print(tmp)
    data.append(tmp[1]) #name
    data.append(tmp[2]) #等级
    if tmp[3] == 'male':
        data.append('男') 
    else: data.append("女")
    data.append(tmp[4]) #职业
    data.append(tmp[5]) #年龄
    savesql()
    return render(request,'pinfo.html',{'data':data,'username':username[1:-1],'career':career[1:-1]})

def manage(request):
    username = request.GET.get('username')
    career = request.GET.get('career')
    return render(request,'index.html',{'username':username[1:-1],'career':career[1:-1]})


