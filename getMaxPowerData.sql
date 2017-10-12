select test.date, MAX(test.northSupply) from `test` where date >= '2016/10/1' and date < '2017/6/31' group by test.date;
select test.date, MAX(test.northUsage) from `test` where  date >= '2016/10/1' and date < '2017/6/31' group by test.date;
select test.date, MAX(test.centerSupply) from `test` where date >= '2016/10/1' and date < '2017/6/31' group by test.date;
select test.date, MAX(test.centerUsage) from `test` where date >= '2016/10/1' and date < '2017/6/31' group by test.date;
select test.date, MAX(test.southSupply) from `test` where date >= '2016/10/1' and  date < '2017/6/31' group by test.date;
select test.date, MAX(test.southUsage) from `test` where date >= '2016/10/1' and  date < '2017/6/31' group by test.date;
select test.date, MAX(test.eastSupply) from `test` where date >= '2016/10/1' and  date < '2017/6/31' group by test.date;
select test.date, MAX(test.eastUsage) from `test` where date >= '2016/10/1' and  date < '2017/6/31' group by test.date;
