--Query 2
select name, count(*), sum(price), sum(internal_cost), count(distinct waste_type)
from service_agreements sa, accounts a, personnel p
where sa.master_account = "customer's master_account" and sa.master_account = a.account_no and a.account_mgr = p.pid
