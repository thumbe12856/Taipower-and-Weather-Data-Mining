select test.date, MAX(test.northSupply) from `test` where date < '2017/6/30' group by test.date
