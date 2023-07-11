select
	dealership_name
	, count(distinct
			case
				when scraped_month = date_trunc('month', CURRENT_DATE) then vin
			end
		   ) as current_month_count
	, count(distinct
			case
				when scraped_month = date_trunc('month', CURRENT_DATE) + interval '-1 month' then vin
			end
		   ) as past_month_count
from scraped_inventory_data.inventories
group by 1;
