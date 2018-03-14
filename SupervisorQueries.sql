--Query 2
select name, count(*), sum(price), sum(internal_cost), count(distinct waste_type)
from service_agreements sa, accounts a, personnel p
where sa.master_account = "customer's master_account" and sa.master_account = a.account_no and a.account_mgr = p.pid;

--Query 3
select account_mgr, count(account_no), count(service_agreements), sum(price), sum(internal_cost)
from accounts a, service_agreements sa
where sa.master_account = a.account_no
order by (sum(price) - sum(internal_cost));