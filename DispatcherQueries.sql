--Query to find all drivers who own a truck, and the owned trucks id
select pid, owned_truck_id
from drivers
where owned_truck_id <> NULL

