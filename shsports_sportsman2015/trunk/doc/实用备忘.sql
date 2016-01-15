--初始化测试编号
update sportsman_student set number=(select count(*) from sportsman_student b where sportsman_student.id >= b.id and sportsman_student.dateOfTesting=b.dateOfTesting)

--原理
select id, dateOfTesting, number, (select count(*) from sportsman_student b where a.id >= b.id and a.dateOfTesting=b.dateOfTesting) as cnt from sportsman_student a order by 
dateOfTesting,number

--初始化序列号字典
DELETE FROM sportsman_sequencenumber WHERE code like 'NUMBER_DATE_OF_TESTING_%'

INSERT INTO sportsman_sequencenumber(code,value)
SELECT 'NUMBER_DATE_OF_TESTING_'||dateOfTesting,max(number) from sportsman_student group by dateOfTesting