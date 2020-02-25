select name 
from Country;

select name 
from Mountain 
where height > 4000;

select capital,population 
from Province 
where country = 'B' and population <= 1000000;

select distinct name as language 
from Language;

select name,Independence 
from Country join Independence 
on Country.code = Independence.country;

select name,percentage,continent
from Encompasses join Country 
on Encompasses.country = Country.code 
where percentage < 100;

select mountain,height 
from GeoMountain join Mountain 
on GeoMountain.mountain = Mountain.name 
where country = 'CH' and height between 4400 and 4500;

with MyBorders as (
	select country1, country2 
	from Borders 
	where country1 < country2
), MyBorders1 as (
	select name as c1, country2 
	from MyBorders join Country 
	on MyBorders.country1 == Country.code
) 
select c1, name as c2 
from MyBorders1 
join Country 
on MyBorders1.country2 == Country.code;

select name 
from Country 
where code not in (
	select country 
	from GeoMountain
);

select name 
from Province 
where name in (
	select name 
	from Country
);

with CountryCodes as (
	select country1 
	from Borders 
	where country2 = 'USA' 
	or country2 in (
		select country1 
		from Borders 
		where country2 = 'USA'
	) 
	and not country1 = 'USA'
) 
select name 
from CountryCodes join Country 
on CountryCodes.country1 == Country.code;

with Ethnic as (
	select distinct name 
	from EthnicGroup
) 
select count(name) 
from Ethnic;

with AllCountryMountains as (
	select name, count(mountain) as cnt 
	from Country left join GeoMountain 
	on Country.code == GeoMountain.country group by code
) 
select * 
from AllCountryMountains 
where cnt <= 3;

with T as (
	select country, name, percentage 
	from Language
), T1 as (
	select T.country || T.name 
	from T join T as TT 
	on T.country == TT.country 
	where T.percentage < TT.percentage
) 
select country, name 
from Language 
where country || name not in T1;

select Borders.country1,Borders.country2 
from Borders left join Borders as Borders2 
on Borders.country1 = Borders2.country2 and Borders.country2 = Borders2.country1 
where Borders2.country1 is null;
with CountryLanguages as (
	select country, count(name) as cnt 
	from Language group by country
), InterestingCountryLanguages as (
	select * 
	from CountryLanguages 
	where cnt >= 3
) 
select name, cnt 
from InterestingCountryLanguages join Country 
on InterestingCountryLanguages.country == Country.code;
