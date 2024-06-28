### 1. Number of Yelp tip compliments by each business
```
select business_id, count(compliment_count) as compliment_count from yelp_academic_dataset_tip
group by business_id
order by compliment_count desc
limit 30
;
```
#### Output
![Screen Shot 2024-06-27 at 4 37 23 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/17b8945d-ce2c-4a82-8234-562ad3489d21)

-> Top 30 businesses with highest number of tip compliments. Tips are written by users to provide advice and what to look out for when visiting a busines establishment. Compliments are given by other Yelp users who read the tips, indicating their agreeableness (either positive or negative) on the business itself.

### 2. Sum of Yelp 5-star review ratings for each business
```
select business_id, sum(stars) as sum_of_stars from yelp_academic_dataset_review
where stars = 5
group by business_id
order by sum_of_stars desc
limit 30
;
```
#### Output
![Screen Shot 2024-06-27 at 4 42 11 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/81140a0a-45bb-448d-a711-37977c8cb9f5)

-> Highest total number of 5 star review rating a business has.

### 3. What's their total 5-star review ratings in #1 and what's their tip compliment count in #2? Is the list in #1 and #2 the same? 
### their total 5-star review ratings in #1
```
with cte as (select business_id, count(compliment_count) as compliment_count from yelp_academic_dataset_tip
group by business_id
order by compliment_count desc
limit 30)
select distinct cte.business_id, sum(ya.stars) as sum_of_stars from cte
join yelp_academic_dataset_review ya on ya.business_id = cte.business_id
where ya.stars = 5
group by cte.business_id
order by sum_of_stars desc
;
```
#### Output
![Screen Shot 2024-06-27 at 4 46 45 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/bc57ac40-eeee-417d-a2e0-67b48440a831)


### out of 21 businesses identified above, how many are in the top 30 list of businesses with high 5-star review rating? 
```
with cte as (select business_id, count(compliment_count) as compliment_count from yelp_academic_dataset_tip
group by business_id
order by compliment_count desc
limit 30), 
cte2 as (select business_id, sum(stars) as sum_of_stars from yelp_academic_dataset_review
where stars = 5
group by business_id
order by sum_of_stars desc
limit 30)
select distinct cte.business_id, cte2.business_id, cte2.sum_of_stars from cte
join cte2 on cte2.business_id = cte.business_id
;
```
#### Output
![Screen Shot 2024-06-27 at 4 48 43 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/a8eff62f-1888-4bfd-b94c-23a7172a7aad)


### their tip compliment count in #2
```
with cte as (select business_id, sum(stars) as sum_of_stars from yelp_academic_dataset_review
where stars = 5
group by business_id
order by sum_of_stars desc
limit 30)
select cte.business_id, count(ya.compliment_count) as compliment_count from cte
join yelp_academic_dataset_tip ya on cte.business_id = ya.business_id
group by cte.business_id
order by compliment_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 4 49 45 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/bddab732-e4c3-4f24-a406-c95036bc84b4)


### out of 30 businesses, how many are in the top 30 list of businesses with high tip compliments? 
```
with cte as (select business_id, sum(stars) as sum_of_stars from yelp_academic_dataset_review
where stars = 5
group by business_id
order by sum_of_stars desc
limit 30),
cte2 as (select business_id, count(compliment_count) as compliment_count from yelp_academic_dataset_tip
group by business_id
order by compliment_count desc
limit 30)
select distinct cte.business_id, cte2.business_id, cte2.compliment_count from cte
join cte2 on cte2.business_id = cte.business_id
;
```
#### Output
![Screen Shot 2024-06-27 at 4 53 07 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/e516a769-3025-4020-a4ce-b99761b34473)


## List is not the same. Just because they have received high number of compliments does not mean that same business will receive high number of 5-star review ratings, as we see that there are only 21 businesses with highest tip compliments that have 5-star review rating as well. And there are only 8 businesses out of 21 that are in the top 30 list of businesses with high 5-star review rating and 8 businesses out of 30 of highest 5-star review rating in the top 30 list of businesses with high tip compliments as well.

### 4. Number of star review ratings in each star
```
SELECT distinct stars, count(stars) as star_count FROM yelp_academic_dataset_review
group by stars
order by star_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 4 54 53 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/a3e022e0-614c-44bd-87e0-9ee5f8a2873d)

-> 5-star review rating has the most count

### 5. Top 30 businesses with number of checkins 
```
SELECT business_id, sum(LENGTH(date) - LENGTH(REPLACE(date, ',', '')) + 1) as checkins_count 
FROM yelp_academic_dataset_checkin
group by business_id
order by checkins_count desc
limit 30
;
```
#### Output
![Screen Shot 2024-06-27 at 4 56 10 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/a4c776cb-ce7c-45fe-98d1-3eb28ec8eef7)

-> Highest number of checkins a business has.

### 6. Are there relationship between number of checkins and 5-star review rating? 
### let's create a view from the above query (Remove limit 30) and query in #2 first
### correlation
```
select @ax := avg(nc.checkins_count), 
       @ay := avg(ns.sum_of_stars), 
       @div := (stddev_samp(checkins_count) * stddev_samp(sum_of_stars))
from number_of_checkins nc
join number_of_stars ns on nc.business_id = ns.business_id;

select sum((nc.checkins_count - @ax) * (ns.sum_of_stars - @ay) )/((count(nc.checkins_count) -1) * @div) 
as correlation
from number_of_checkins nc
join number_of_stars ns on nc.business_id = ns.business_id;
```
#### Output
![Screen Shot 2024-06-27 at 5 00 06 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/6dc1fb09-bc06-457a-8158-3af379d72343)

-> They have a moderate positive relationship

### 7. Does number of fan a user have when gives 5-star review rating correlate to number of checkins? 
### correlation
```
select @ax := avg(nc.checkins_count), 
       @ay := avg(yu.fans), 
       @div := (stddev_samp(nc.checkins_count) * stddev_samp(yu.fans))
from number_of_checkins nc
join yelp_academic_dataset_review yr on nc.business_id = yr.business_id
join yelp_academic_dataset_user yu on yr.user_id = yu.user_id
where yr.stars = 5;

select sum((nc.checkins_count - @ax) * (yu.fans - @ay) )/((count(nc.checkins_count) -1) * @div) 
as correlation
from number_of_checkins nc
join yelp_academic_dataset_review yr on nc.business_id = yr.business_id
join yelp_academic_dataset_user yu on yr.user_id = yu.user_id
where yr.stars = 5;
```
#### Output
![Screen Shot 2024-06-27 at 5 06 56 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/8ec8498f-5690-4c59-8e2f-232751ad80e7)

-> No relationship

### 8. Number of photos by label (there are many labels, but we'll only look at the main ones)
```
SELECT label, count(distinct photo_id) as photos_count FROM photos
where label in ('inside', 'outside', 'drink', 'food', 'menu')
group by label
order by photos_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 07 42 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/6afc0ff3-5063-46b7-8e3c-9f3b3d86e02e)

-> Food and interior of a business has the most photos posted by users.

### 9. If a business accepts credit cards or by appointment only, what star rating do they receive? 
### By appointment only 
```
SELECT distinct stars, ByAppointmentOnly, count(stars) as stars_count FROM yelp_academic_dataset_business
where ByAppointmentOnly in ('True', 'False')
group by stars, ByAppointmentOnly
order by stars_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 09 52 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/090e585a-8d8b-4eca-9f33-e0e650e234e5)


### Accepts credit cards
```
SELECT distinct stars, BusinessAcceptsCreditCards, count(stars) as stars_count FROM yelp_academic_dataset_business
where BusinessAcceptsCreditCards in ('True', 'False')
group by stars, BusinessAcceptsCreditCards
order by stars_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 10 22 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/f035b67e-2b82-46be-b510-1c3d9edf8a56)

-> Look like if they accept credit cards or no appointment, they would get more star ratings at all levels. So let's look at their review count to confirm
```
SELECT DISTINCT
    CASE
        WHEN review_count < 1000 THEN 'Less than 1000'
        WHEN review_count BETWEEN 1000 and 2000 then '1000-2000'
        WHEN review_count BETWEEN 2001 AND 3000 THEN '2001-3000'
        WHEN review_count BETWEEN 3001 AND 4000 THEN '3001-4000'
        WHEN review_count BETWEEN 4001 AND 5000 THEN '4001-5000'
        WHEN review_count >= 5001 THEN '5001 and above'
    END review_count_group, BusinessAcceptsCreditCards, stars, count(stars) as stars_count 
from yelp_academic_dataset_business
where BusinessAcceptsCreditCards in ('True', 'False')
group by review_count_group, BusinessAcceptsCreditCards, stars
order by stars_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 11 29 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/e5aed250-dd6c-41a1-a97f-cc73357fa186)

```
SELECT DISTINCT
    CASE
        WHEN review_count < 1000 THEN 'Less than 1000'
        WHEN review_count BETWEEN 1000 and 2000 then '1000-2000'
        WHEN review_count BETWEEN 2001 AND 3000 THEN '2001-3000'
        WHEN review_count BETWEEN 3001 AND 4000 THEN '3001-4000'
        WHEN review_count BETWEEN 4001 AND 5000 THEN '4001-5000'
        WHEN review_count >= 5001 THEN '5001 and above'
    END review_count_group, ByAppointmentOnly, stars, count(stars) as stars_count 
from yelp_academic_dataset_business
where ByAppointmentOnly in ('True', 'False')
group by review_count_group, ByAppointmentOnly, stars
order by stars_count desc
;
```
#### output
![Screen Shot 2024-06-27 at 5 12 19 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/dac1a4ab-11bb-4215-b7f1-348047a88933)

-> In conclusion, number of review has nothing to do with star rating and BusinessAcceptsCreditCards or ByAppointmentOnly attributes. Whether the review count is high or low does not affect the star rating. In other words, they can have less reviews but more star rating at all levels, and vice versa. Let's check the correlation between review count and star rating to confirm.
### correlation
```
select @ax := avg(review_count), 
       @ay := avg(stars), 
       @div := (stddev_samp(review_count) * stddev_samp(stars))
from yelp_academic_dataset_business;

select sum((review_count - @ax) * (stars - @ay) )/((count(review_count) -1) * @div) 
as correlation
from yelp_academic_dataset_business;
```
#### Output
![Screen Shot 2024-06-27 at 5 13 35 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/66176303-d170-4edc-8d68-23cfbb0c7a6e)

-> It's confirmed, there's no relationship. 

### 10. What is the star rating of businesses with WiFi attribute? 
```
SELECT distinct WiFi, stars, count(stars) as stars_count FROM yelp_academic_dataset_business
where WiFi in ('no', 'free', 'paid')
group by WiFi, stars
order by stars_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 14 35 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/1fa25eb5-8738-4dee-91f7-7036f27badb8)

-> It looks like the number of star rating received by business has nothing to do with whether WiFi free or not, or paid. They can still get low star even if their WiFi is free. Let's check the correlation to confirm. 

### correlation between WiFi and star rating
### create view named wifi_correlation from the below query
```
SELECT distinct WiFi,
CASE
        WHEN WiFi in ('free') THEN '0'
        WHEN WiFi in ('paid') THEN '1'
        WHEN WiFi in ('no') THEN '2'
        ELSE null
    END WiFi_multiclass,
stars, count(stars) as stars_count FROM yelp_academic_dataset_business
where WiFi in ('no', 'free', 'paid')
group by WiFi, stars
order by stars_count desc
;
```
### then check for correlation
### first way
```
SELECT 
    (SUM(WiFi_multiclass * stars * stars_count) - SUM(WiFi_multiclass * stars_count) * SUM(stars * stars_count) / SUM(stars_count)) /
    (SQRT(SUM(WiFi_multiclass * WiFi_multiclass * stars_count) - SUM(WiFi_multiclass * stars_count) * SUM(WiFi_multiclass * stars_count) / SUM(stars_count)) * 
     SQRT(SUM(stars * stars * stars_count) - SUM(stars * stars_count) * SUM(stars * stars_count) / SUM(stars_count))) AS correlation
FROM 
    wifi_correlation;
```
#### Output
![Screen Shot 2024-06-27 at 5 18 06 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/f46c203d-e393-434e-9d20-0c50daa3d527)

    
### second way
```
select @ax := avg(WiFi_multiclass), 
       @ay := avg(stars), 
       @div := (stddev_samp(WiFi_multiclass) * stddev_samp(stars))
from wifi_correlation;

select sum((WiFi_multiclass - @ax) * (stars - @ay) )/((count(WiFi_multiclass) -1) * @div) 
as correlation
from wifi_correlation;
```
#### Output 
![Screen Shot 2024-06-27 at 5 18 23 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/a50a7ec3-41c6-4804-9737-5617e3eff9e1)

-> It's confirmed, there's no relationship.  

### 11. The most popular business categories? 
```
with cte as (select yelp_academic_dataset_business.business_id, 
SUBSTRING_INDEX(SUBSTRING_INDEX(yelp_academic_dataset_business.categories, ', ', numbers.n), ', ', -1) categories
from
(select 1 n union all
   select 2 union all select 3 union all
   select 4 union all select 5) numbers INNER JOIN yelp_academic_dataset_business
  on CHAR_LENGTH(yelp_academic_dataset_business.categories)
     -CHAR_LENGTH(REPLACE(yelp_academic_dataset_business.categories, ', ', ''))>=numbers.n-1
order by
  business_id, n)
select distinct categories, count(distinct business_id) as categories_count from cte
group by categories
order by categories_count desc
limit 30
;
```
#### Output
![Screen Shot 2024-06-27 at 5 19 33 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/5d23cac6-f5f2-4a55-b0fb-be78a686f44c)

-> Restaurants top the list of the most popular Yelp business category.

### per state
```
with cte2 as (with cte as (select yelp_academic_dataset_business.business_id, state,
SUBSTRING_INDEX(SUBSTRING_INDEX(yelp_academic_dataset_business.categories, ', ', numbers.n), ', ', -1) categories
from
(select 1 n union all
   select 2 union all select 3 union all
   select 4 union all select 5) numbers INNER JOIN yelp_academic_dataset_business
  on CHAR_LENGTH(yelp_academic_dataset_business.categories)
     -CHAR_LENGTH(REPLACE(yelp_academic_dataset_business.categories, ', ', ''))>=numbers.n-1
order by
  business_id, n)
select distinct state, categories, count(distinct business_id) as categories_count from cte
group by state, categories
order by categories_count desc)
SELECT distinct cc.*
FROM cte2 cc                   
LEFT JOIN cte2 ccc ON cc.state = ccc.state 
AND (cc.categories_count < ccc.categories_count or (cc.categories_count = ccc.categories_count and cc.categories < ccc.categories))
WHERE ccc.categories_count is NULL 
order by categories_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 22 01 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/2d006469-a25f-4137-8995-4c7e84fe9480)

-> Restaurants category is the most popular category in most states, while other categories spread out across the rest of states. It also looks like some states use Yelp more than other states, it's possible that there are many businesses out there that haven't used Yelp yet, hence the low count.

### 12. Top 10 cities with most popular categories
```
with cte2 as (with cte as (select yelp_academic_dataset_business.business_id, state, city,
SUBSTRING_INDEX(SUBSTRING_INDEX(yelp_academic_dataset_business.categories, ', ', numbers.n), ', ', -1) categories
from
(select 1 n union all
   select 2 union all select 3 union all
   select 4 union all select 5) numbers INNER JOIN yelp_academic_dataset_business
  on CHAR_LENGTH(yelp_academic_dataset_business.categories)
     -CHAR_LENGTH(REPLACE(yelp_academic_dataset_business.categories, ', ', ''))>=numbers.n-1
order by
  business_id, n)
select distinct state, city, categories, count(distinct business_id) as categories_count from cte
group by state, city, categories
order by categories_count desc)
SELECT distinct cc.*
FROM cte2 cc                   
LEFT JOIN cte2 ccc ON cc.city = ccc.city and cc.state = ccc.state
AND (cc.categories_count < ccc.categories_count or (cc.categories_count = ccc.categories_count and cc.categories < ccc.categories))
WHERE ccc.categories_count is NULL 
order by categories_count desc
limit 10
;
```
#### Output
![Screen Shot 2024-06-27 at 5 27 12 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/5daa197f-938e-457e-a078-8fe57ca5997a)

-> Restaurants category wins the race this time as well.

### 13. What's the business name, stars, and categories of top 30 businesses with highest number of checkins? 
```
with cte as (SELECT business_id, sum(LENGTH(date) - LENGTH(REPLACE(date, ',', '')) + 1) as checkins_count 
FROM yelp_academic_dataset_checkin
group by business_id
order by checkins_count desc
limit 30)
select distinct yb.name, yb.stars, cte.checkins_count, yb.categories
from cte
join yelp_academic_dataset_business yb on cte.business_id = yb.business_id
order by cte.checkins_count desc
;
```
#### Output
![Screen Shot 2024-06-27 at 5 28 28 PM](https://github.com/quocduyenanhnguyen/Yelp-analysis/assets/92205707/6bf5fe3a-e34b-4fe6-8e0b-c64b0a5a118a)

-> Most of them have 4 star rating and above, while the minority has less than 4 star. The categories are also diverse, most of them are restaurants. 




