--Query 1
select location, local_contact, waste_type, cid_drop_off, cid_pick_up, date_time
from service_agreements sa, service_fulfillments sf
where sf.service_no = sa.service_no and sf.driver_id = '43743';
