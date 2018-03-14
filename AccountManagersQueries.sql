--Query 4

select count(*), sum(price), sum(internal_cost), count(distinct waste_type)
from service_agreements
where master_account = "customer's master_account";
