--Query 1
select location, local_contact, waste_type, cid_drop_off, cid_pick_up
from service_agreements sa, service_fulfillments sf
where sa.master_account = sf.master_account and sf.date_time > "start date input" and sf.date_time < "end date input"