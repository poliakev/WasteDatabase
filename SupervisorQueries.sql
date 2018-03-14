--Query 2

--Query 3
select account_mgr, count(distinct account_no), count(service_no), sum(price), sum(internal_cost), (sum(price) - sum(internal_cost)) as num
from accounts a, service_agreements sa
where sa.master_account = a.account_no
group by account_mgr
order by (num);
