drop database AI;
create database AI;

use AI;


create table account(
    ID      CHAR(100)       PRIMARY KEY,
    passwd  VARCHAR(20)     NOT NULL, 
    email   VARCHAR(100)    NOT NULL UNIQUE,
    phone   CHAR(11)        NOT NULL UNIQUE
);


# 触发器，用来保证密码大于八位
create trigger account_check
before insert on account
for each ROW
begin 
    if(length(NEW.passwd)<8) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'password must be more than 8 characters';
    end if;
    if(length(NEW.phone)<11 or length(NEW.phone)>11) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'phone must be 11 characters';
    end if;

    if new.email not like '%@%' then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'email should include @';
    end if;
end;

create trigger account_check2
before update on account
for each ROW
begin 
    if(length(NEW.passwd)<8) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'password must be more than 8 characters';
    end if;
    if(length(NEW.phone)<11 or length(NEW.phone)>11) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'phone must be 11 characters';
    end if;
end;




delete 
from account;

insert into account(ID,passwd,email,phone)
values
('adopted_irelia',12345678,'adoptedirelia@gmail.com',13935239775),
('zhang3',12345678,'zhang3@qq.com',13935239776),
('li4',12345678,'li4@qq.com',13935239777);



select *
from account;


create table user(
    ID      CHAR(100)               PRIMARY KEY,
    name    VARCHAR(100)            NOT NULL,
    level   int                     NOT NULL,
    gender  ENUM('male','female')   NOT NULL,
    career  CHAR(100)               NOT NULL,
    age     int                     NOT NULL,
    FOREIGN KEY (ID) REFERENCES account(ID) on delete cascade on update cascade
);


create trigger user_check
before insert on user 
for each row
begin 
    if(NEW.age<=0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'age must be positive';
    end if;
    if(NEW.level<=0 or NEW.level>6) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'level must be between 0 and 6';
    end if;
end;

create trigger user_check2
before update on user 
for each row
begin 
    if(NEW.age<=0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'age must be positive';
    end if;
    if(NEW.level<=0 or NEW.level>6) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'level must be between 0 and 6';
    end if;
end;

create trigger user_delete
after delete on user
for each row 
begin 
    delete from account where account.id = old.id;
end;



delete 
from user;

insert into user(ID,name,level,gender,career,age)
values
('adopted_irelia','zdj',6,'male','admin',22),
('zhang3','zhangsan',5,'male','student',21),
('li4','lisi',5,'female','student',21);

select *
from user;



create table restaurant(
    ID              CHAR(100)       PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    location        CHAR(100)       NOT NULL,
    type            VARCHAR(100)    NOT NULL,
    telephone       CHAR(11)        NOT NULL UNIQUE,
    level           FLOAT             NOT NULL,
    avg_price       FLOAT           NOT NULL,
    opening_time    time            NOT NULL,
    closing_time    time            NOT NULL,
    featured_dishes VARCHAR(500)    NOT NULL
);


create trigger restaurant_check
before insert on restaurant 
for each row
begin 
    if(NEW.avg_price<0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'price must be positive';
    end if;
    if(NEW.level<0 or NEW.level>5) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'level must be between 0 and 5';
    end if;
    if(NEW.opening_time>NEW.closing_time) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'how can closing time earlier than opening time?';
    end if;
    if(length(NEW.telephone)<11) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'telephone number must be 11 characters';
    end if;
end;

create trigger restaurant_check2
before update on restaurant 
for each row
begin 
    if(NEW.avg_price<0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'price must be positive';
    end if;
    if(NEW.level<0 or NEW.level>5) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'level must be between 0 and 5';
    end if;
    if(NEW.opening_time>NEW.closing_time) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'how can closing time earlier than opening time?';
    end if;
    if(length(NEW.telephone)<11) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'telephone number must be 11 characters';
    end if;
end;

delete 
from restaurant;

insert into restaurant(ID,name,location,type,telephone,level,avg_price,opening_time,closing_time,featured_dishes)
values
('KFC01','KFC','西直门凯德茂','快餐','12345678900',0,80.0,TIME('7:00:00'),TIME('22:00:00'),'香辣鸡腿堡'),
('QJD01','全聚德','中国白石桥37号科贸中心院内','中餐','12345678901',0,100.0,TIME('7:00:00'),TIME('22:00:00'),'北京烤鸭'),
('MAC01','Macdonald','北京交通大学南门','快餐','12345678902',0,40.0,TIME('7:00:00'),TIME('22:00:00'),'圣代'),
('KFC02','KFC','大钟寺','快餐','12345678903',0,50.0,TIME('7:00:00'),TIME('22:00:00'),'香辣鸡腿堡'),
('IKUN01','IKUN','北京市??','快餐','12345678904',0,25.0,TIME('7:00:00'),TIME('22:00:00'),'鸡你太美');


select *
from restaurant;


create table comment(
    comment_ID      CHAR(100)   PRIMARY KEY,
    user_ID         CHAR(100)   NOT NULL,
    restaurant_ID   CHAR(100)   NOT NULL,
    star            int         NOT NULL,
    comment_time    date        NOT NULL,
    content         TEXT        NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES account(ID) on delete cascade on update cascade,
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(ID) on delete cascade on update cascade
);


create trigger comment_check
before insert on comment
for each row
begin
    if(NEW.star<0 or NEW.star>5) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'star must be between 0 and 5';
    end if;
end;

create trigger comment_check2
before update on comment
for each row
begin
    if(NEW.star<0 or NEW.star>5) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'star must be between 0 and 5';
    end if;
end;

CREATE TRIGGER update_avg_rating
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
    -- 计算饭店的平均评分
    UPDATE restaurant
    SET level = (
        SELECT AVG(star) FROM comment WHERE restaurant_ID = NEW.restaurant_ID
    )
    WHERE ID = NEW.restaurant_ID;
END;

CREATE TRIGGER update_avg_rating2
AFTER delete ON comment
FOR EACH ROW
BEGIN
    -- 计算饭店的平均评分
    UPDATE restaurant
    SET level = (
        SELECT AVG(star) FROM comment WHERE restaurant_ID = old.restaurant_ID
    )
    WHERE ID = old.restaurant_ID;
END;


delete
from comment;

insert into comment(comment_ID,user_ID,restaurant_ID,star,comment_time,content)
values
('c001','adopted_irelia','KFC01',1,'2023-3-30','太贵啦!!'),
('c002','adopted_irelia','QJD01',5,'2023-3-30','好!'),
('c003','zhang3','KFC01',4,'2023-3-30','好吃'),
('c004','li4','MAC01',4,'2023-3-31','又近又好吃');



select *
from comment;


create table meal(
    ID              CHAR(100)   PRIMARY KEY,
    name            CHAR(100)   NOT NULL,
    price           float       NOT NULL,
    discount        float       NOT NULL,
    time_consuming  int         NOT NULL,
    style           CHAR(100)   NOT NULL
);


create trigger meal_check
before insert on meal
for each row
begin 
    if(NEW.price<0) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'price must be positive';
    end if;
    if(NEW.time_consuming<=0) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'time must be positive';
    end if;
    if(NEW.discount<0 or NEW.discount>1) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'discount must be between 0 and 1';
    end if;
end;

create trigger meal_check2
before update on meal
for each row
begin 
    if(NEW.price<0) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'price must be positive';
    end if;
    if(NEW.time_consuming<=0) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'time must be positive';
    end if;
    if(NEW.discount<0 or NEW.discount>1) then 
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'discount must be between 0 and 1';
    end if;
end;

delete 
from meal;

insert into meal(ID,name,price,discount,time_consuming,style)
values
('m001','蛋挞',5,0.8,5,'甜'),
('m002','香辣鸡腿堡',20,0.9,10,'辣'),
('m003','北京烤鸭',80,1,60,'甜'), 
('m004','薯条',10,0.9,1,'咸'),
('m005','圣代',7,0.9,2,'甜'),
('m006','可乐',5,1,4,'甜'),
('m007','辣么大鸡排',25,1,5,'辣'),
('m008','欢乐儿童餐',100,1,20,'甜'),
('m009','米饭',2,1,1,'无'), 
('m010','宫保鸡丁',20,1,1,'甜'),
('m011','鱼香肉丝',25,1,1,'甜'),
('m012','松仁玉米',23,1,1,'甜'),
('m013','木须肉',18,1,1,'咸'),
('m014','油饼',3,1,1,'甜'),
('m015','香精煎鱼',25,1,1,'辣'),
('m016','香翅捞饭',25,1,1,'甜'),
('m017','香贝旺堡',18,1,1,'咸'),
('m018','卤出鸡脚',20,1,1,'咸'),
('m019','荔枝',5,1,1,'甜'),
('m020','蒸虾头',9,1,1,'咸'),
('m021','驴食寒',18,1,1,'咸'),
('m022','蒸乌鱼',80,1,1,'咸'),
('m023','坤坤蛋炒饭',10,1,1,'咸'),
('m024','梅油酥汁',18,1,1,'甜'),
('m025','香精橘子',23,1,1,'甜'),
('m026','纯路仁',60,1,1,'咸'),
('m027','香精金茶菊',120,1,1,'咸'),
('m028','鲵干麻',140,1,1,'苦'),
('m029','鸡你太美',2.5,1,1,'酸甜苦辣咸')
;

select *
from meal;




create table rm(
    restaurant_ID   CHAR(100)   NOT NULL,
    meal_ID         CHAR(100)   NOT NULL,
    PRIMARY KEY (restaurant_ID,meal_ID),
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(ID) on delete cascade on update cascade,
    FOREIGN KEY (meal_ID) REFERENCES meal(ID) on delete cascade on update cascade
);

delete 
from rm;


insert into rm VALUES
('KFC01','m006'),
('KFC02','m006'),
('KFC01','m008'),
('KFC02','m008'),
('Mac01','m006'),
('Mac01','m007'),
('QJD01','m009'),
('QJD01','m010'),
('QJD01','m011'),
('QJD01','m012'),
('QJD01','m013'),
('IKUN01','m014'),
('IKUN01','m015'),
('IKUN01','m016'),
('IKUN01','m017'),
('IKUN01','m018'),
('IKUN01','m019'),
('IKUN01','m020'),
('IKUN01','m021'),
('IKUN01','m022'),
('IKUN01','m023'),
('IKUN01','m024'),
('IKUN01','m025'),
('IKUN01','m026'),
('IKUN01','m027'),
('IKUN01','m028'),
('IKUN01','m029')
;


select *
from rm;




create table material(
    ID      CHAR(100)   PRIMARY KEY,
    name    CHAR(100)   NOT NULL,
    price   int         NOT NULL
);


create trigger material_check
before insert on material
for each row
begin 
    if(NEW.price<0) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'price must be positive';
    end if;
end;

create trigger material_check2
before update on material
for each row
begin 
    if(NEW.price<0) then 
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'price must be positive';
    end if;
end;

delete 
from material;

insert into material(ID,name,price)
values
('mtl001','生菜',5),
('mtl002','面包',5),
('mtl003','鸭',50),
('mtl004','奶油',10),
('mtl005','肉饼',10),
('mtl006','芝士酱',5),
('mtl007','鸡蛋',5);

select *
from material;


create table mm(
    meal_ID     CHAR(100)   NOT NULL,
    material_ID CHAR(100)   NOT NULL,
    amount      float       NOT NULL,    
    PRIMARY KEY(meal_ID,material_ID),
    FOREIGN KEY (meal_ID) REFERENCES meal(ID) on delete cascade on update cascade,
    FOREIGN KEY (material_ID) REFERENCES material(ID) on delete cascade on update cascade
);


create trigger mm_check
before insert on mm
for each row
begin
    if(NEW.amount<0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'amount must be positive';
    end if;
end;

create trigger mm_check2
before update on mm
for each row
begin
    if(NEW.amount<0) then
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'amount must be positive';
    end if;
end;

delete 
from mm;

insert into mm(meal_ID,material_ID,amount)
values
('m002','mtl001',1),
('m002','mtl002',1),
('m002','mtl005',1),
('m002','mtl006',1),
('m001','mtl007',2),
('m003','mtl003',1);

select *
from mm;



create table chef(
    ID              CHAR(100)   PRIMARY KEY,
    restaurant_ID   CHAR(100)   NOT NULL,
    name            CHAR(100)   NOT NULL,
    proficiency     int         NOT NULL,
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(ID) on delete cascade on update cascade 
);


create trigger chef_check
before insert on chef
for each row
begin 
    if(NEW.proficiency<=0 or NEW.proficiency>5) then  
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'proficiency must between 1 and 5';
    end if;
end;

create trigger chef_check2
before update on chef
for each row
begin 
    if(NEW.proficiency<=0 or NEW.proficiency>5) then  
        signal SQLSTATE '45000'
        set MESSAGE_TEXT = 'proficiency must between 1 and 5';
    end if;
end;

delete 
from chef;

insert into chef(ID,restaurant_ID,name,proficiency)
values
('chef01','KFC01','faker',5),
('chef02','MAC01','bang',5),
('chef03','QJD01','wolf',5),
('chef04','KFC02','guma',5);

select *
from chef;


create table cm(
    chef_ID     CHAR(100)   NOT NULL,
    meal_ID     CHAR(100)   NOT NULL,
    PRIMARY KEY (chef_ID,meal_ID),
    FOREIGN KEY (chef_ID) REFERENCES chef(ID) on delete cascade on update cascade,
    FOREIGN KEY (meal_ID) REFERENCES meal(ID) on delete CASCADE on update CASCADE
);

delete
from cm;

create trigger cm_insert
after insert on cm 
for each row 
begin 
    DECLARE rid char(100);
    DECLARE done INT DEFAULT FALSE;
    DECLARE cnt int;
    DECLARE mcursor CURSOR FOR select restaurant_ID from chef where chef.ID = new.chef_ID;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    open mcursor;

    mloop: LOOP
        fetch mcursor into rid;
        if done then
            leave mloop;
        end if;

        SELECT COUNT(*) INTO cnt FROM rm WHERE restaurant_ID = rid and meal_ID = new.meal_ID;
        IF cnt = 0 THEN 
            #SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate entry not allowed.';
            insert into rm(restaurant_ID,meal_ID) values(rid,new.meal_ID);
        END IF;


    end loop;

    close mcursor;

end;

create trigger cm_update
after update on cm
for each row 
begin 
    #delete
    delete from cm where chef_ID = old.chef_ID and meal_ID = old.meal_ID;
    #insert
    insert into cm values(new.chef_ID,new.meal_ID);

end;

create trigger cm_delete
after delete on cm 
for each row  
begin 
    declare cnt int DEFAULT 0;
    declare rid char(100);
    select restaurant_ID into rid from chef where ID = old.chef_ID;

    select count(*) into cnt from cm inner join chef on cm.chef_ID = chef.ID where chef.restaurant_ID = rid and cm.meal_ID = old.meal_ID;

    if cnt = 0 then 
        delete from rm where restaurant_ID = rid and meal_ID = old.meal_ID;
    end if;

end;

insert into cm(chef_ID,meal_ID)
values
('chef01','m001'),
('chef01','m002'),
('chef01','m004'),
('chef01','m005'),
('chef02','m001'),
('chef02','m002'),
('chef02','m004'),
('chef02','m005'),
('chef03','m003'),
('chef04','m001'),
('chef04','m002'),
('chef04','m004'),
('chef04','m005')

;


select *
from cm;


create table myorder( 
    ID CHAR(100)    PRIMARY KEY NOT NULL, 
    order_date date NOT NULL, 
    order_time time NOT NULL,
    acc int NOT NULL
);

create table om( 
    order_ID CHAR(100) NOT NULL, 
    meal_ID CHAR(100) NOT NULL, 
    num int NOT NULL,
    PRIMARY KEY (order_ID,meal_ID),
    FOREIGN KEY (order_ID) REFERENCES myorder(ID) on delete CASCADE on update CASCADE,
    FOREIGN KEY (meal_ID) REFERENCES meal(ID) on delete CASCADE on update CASCADE
);

create table ore( 
    order_ID CHAR(100) NOT NULL, 
    restaurant_ID CHAR(100) NOT NULL, 
    PRIMARY KEY (order_ID,restaurant_ID),
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(ID) on delete cascade on update cascade,
    FOREIGN KEY (order_ID) REFERENCES myorder(ID) on delete CASCADE on update CASCADE
);

create table ou( 
    order_ID CHAR(100) NOT NULL, 
    user_ID CHAR(100) NOT NULL,
    cost float NOT NULL,
    PRIMARY KEY (order_ID,user_ID),
    FOREIGN KEY (user_ID) REFERENCES account(ID) on delete cascade on update cascade,
    FOREIGN KEY (order_ID) REFERENCES myorder(ID) on delete CASCADE on update CASCADE

);



create view acc_info
as 
select ID,passwd
from account
with check option;


create view price(name,origin,current,discount)
as
select name,price,price*discount,discount
from meal
with check option;

create view cmtable(chef,meal)
as 
select chef.name,meal.name
from meal,chef,cm
where chef.ID=cm.chef_ID and meal.ID=cm.meal_ID
ORDER BY chef.name
with check option;

create view commentacc(restaurant_name, star, comments)
as
select restaurant.name,avg(star),count(*)
from comment,restaurant
where comment.`restaurant_ID` = restaurant.ID
group by `restaurant_ID`;


DELIMITER //
CREATE PROCEDURE SelectDataFromTable(
  IN tableName VARCHAR(255)
)
BEGIN
  SET @query = CONCAT('SELECT * FROM ', tableName);
  PREPARE stmt FROM @query;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

#CALL SelectDataFromTable('account');

DELIMITER //
CREATE PROCEDURE InsertDataIntoTable(
  IN tableName VARCHAR(255),
  IN columnValues VARCHAR(255)
)
BEGIN
  SET @query = CONCAT('INSERT INTO ', tableName, ' VALUES (', columnValues, ')');
  PREPARE stmt FROM @query;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

#CALL InsertDataIntoTable('account',  '"wang5", "12345678", "wang5@qq.com", "13935239887"');


DELIMITER //
CREATE PROCEDURE DeleteDataFromTable(
  IN tableName VARCHAR(255),
  IN mcondition VARCHAR(255)
)
BEGIN
  SET @query = CONCAT('DELETE FROM ', tableName, ' WHERE ', mcondition);
  PREPARE stmt FROM @query;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


#CALL DeleteDataFromTable('account', 'ID = "wang5" AND email = "wang5@qq.com"');

DELIMITER //
CREATE PROCEDURE UpdateDataInTable(
  IN tableName VARCHAR(255),
  IN setClause VARCHAR(255),
  IN mcondition VARCHAR(255)
)
BEGIN
  SET @query = CONCAT('UPDATE ', tableName, ' SET ', setClause, ' WHERE ', mcondition);
  PREPARE stmt FROM @query;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

# CALL UpdateDataInTable('account', 'passwd = "123456788"', 'ID = "adopted_irelia"');


create view test3 as select restaurant_ID,count(*) from rm group by 'meal_ID';

select name,count(*) from restaurant group by name;

update chef set proficiency = 0.8 * proficiency where `restaurant_ID` in (select ID from restaurant where `name`='KFC');