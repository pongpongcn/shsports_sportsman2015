--��ʼ�����Ա��

update sportsman_student set number=(select count(*) from sportsman_student b where sportsman_student.id >= b.id and sportsman_student.dateOfTesting=b.dateOfTesting)

--ԭ��
select id, dateOfTesting, number, (select count(*) from sportsman_student b where a.id >= b.id and a.dateOfTesting=b.dateOfTesting) as cnt from sportsman_student a order by dateOfTesting,number

--��ʼ�����к��ֵ�
INSERT INTO sportsman_sequencenumber(code,value)
SELECT 'NumberByDateOfTesting_'||dateOfTesting,max(number) from sportsman_student group by dateOfTesting
