#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import string
import json
import pprint
import random
import sqlite3

# 1. "Create a python script which downloads as much drinks as possible from following page: https://www.thecocktaildb.com/api.php"


fp = open('sales.txt', 'x')

generateAlphabet = list(string.ascii_lowercase)   
print(f'_____________________________________________________________________\r\n\n Generated API call parameters (to fetch all available cocktails from https://www.thecocktaildb.com/):\r\n {generateAlphabet}\r\n_____________________________________________________________________\r\n')


jsonCocktails = []

for p in generateAlphabet:
    try:

        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={p}')
        response.raise_for_status()

        data = response.json().get("drinks")
        # check if response contains relevant data
        if data is not None and len(data)>0 :

            print(f"\r\n{len(data)} elements downloaded for letter \'{p}\'. \n\nSample: \n{data[0]}")
            jsonCocktails.extend(data)

        else:
            print(f'\r\n\nThere aren\'t any cocktails found in "TheCocktailDB"  w/ letter: \'{p}\'...  :(\r\n')

    except HTTPError as httpError:
        print(f'HTTP error: {httpError}')

    except Exception as e:
        print(f'Error occurred: {e}')



# 3. "Extend your script (from point 1) to insert the data in your database. Please insert just data which has German instructions."

parsedDataset = []
parsedCocktails = {}
uselessKeys = ['strDrinkAlternate', 'strTags', 'strVideo', 'strCategory', 'strIBA', 'strGlass', 'strInstructionsES', 'strInstructionsFR', 'strInstructionsIT', 'strInstructionsZH-HANS', 'strInstructionsZH-HANT', 'strDrinkThumb', 'strImageSource', 'strImageAttribution', 'strCreativeCommonsConfirmed', 'dateModified']

for i in jsonCocktails:  
    l = range(len([i]))
    
    for j in l:       
        tmp = [i][j]
        
        if tmp.get("strInstructionsDE") is not None:

            for delete in uselessKeys:
                tmp.pop(delete,None)
            
            parsedCocktails.update(tmp.items())
        
        else:
            jsonCocktails.remove(i)
    parsedDataset.append(dict(parsedCocktails))

# Deduplication of cocktails
deduplicated = set()
cleanDataset = []
for d in parsedDataset:
    
    t = tuple(d.items())
    
    if t not in deduplicated:
        deduplicated.add(t)
        cleanDataset.append(d)

print(f'_____________________________________________________________________\r\n\n Number of cocktails w/ DE distruction:\t{len(cleanDataset)}')
print(f'_____________________________________________________________________\r\n\n R a n d o m   c o c k t a i l   s a m p l e :\n')
pprint.pprint(cleanDataset[random.randint(0, len(cleanDataset))])



# 2. "Create a relational database in sqlite for the downloaded data, under the assumption that your database could grow to over 10 million datasets."

'''
parsedKeys = []

for h in parsedDataset:
    l = range(len([h]))

    for g in l:       
        parsedKeys = list([h][g].keys())
            
print(parsedKeys)
'''

connectSQLite = sqlite3.connect('the_cocktail.db')
print(f'\r\nDB connection has been established. (the_cocktail.db)\n')

crsr = connectSQLite.cursor()
crsr.execute("create table if not exists cocktails (drink_id,drink_name,alcoholic,instructions,instructions_de,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15)")
crsr.executemany("insert into cocktails values (:idDrink,:strDrink,:strAlcoholic,:strInstructions,:strInstructionsDE,:strIngredient1,:strIngredient2,:strIngredient3,:strIngredient4,:strIngredient5,:strIngredient6,:strIngredient7,:strIngredient8,:strIngredient9,:strIngredient10,:strIngredient11,:strIngredient12,:strIngredient13,:strIngredient14,:strIngredient15,:strMeasure1,:strMeasure2,:strMeasure3,:strMeasure4,:strMeasure5,:strMeasure6,:strMeasure7,:strMeasure8,:strMeasure9,:strMeasure10,:strMeasure11,:strMeasure12,:strMeasure13,:strMeasure14,:strMeasure15)", cleanDataset)
crsr.execute("create unique index idx_drink_id on cocktails (drink_id)")
connectSQLite.commit()



# 4/a. "Which alcoholic drinks can be mixed with lemon and whiskey?"

query1 = (f'''
select
     drink_id
    ,drink_name
    ,alcoholic
  from cocktails
 where 1=1
   and lower(alcoholic) = 'alcoholic'
   and (lower(i1) like '%lemon%'
    or lower(i2) like '%lemon%'
    or lower(i3) like '%lemon%'
    or lower(i4) like '%lemon%'
    or lower(i5) like '%lemon%'
    or lower(i6) like '%lemon%'
    or lower(i7) like '%lemon%'
    or lower(i8) like '%lemon%'
    or lower(i9) like '%lemon%'
    or lower(i10) like '%lemon%'
    or lower(i11) like '%lemon%'
    or lower(i12) like '%lemon%'
    or lower(i13) like '%lemon%'
    or lower(i14) like '%lemon%'
    or lower(i15) like '%lemon%')
   and (lower(i1) like '%lemon%'
    or lower(i2) like '%whiskey%'
    or lower(i3) like '%whiskey%'
    or lower(i4) like '%whiskey%'
    or lower(i5) like '%whiskey%'
    or lower(i6) like '%whiskey%'
    or lower(i7) like '%whiskey%'
    or lower(i8) like '%whiskey%'
    or lower(i9) like '%whiskey%'
    or lower(i10) like '%whiskey%'
    or lower(i11) like '%whiskey%'
    or lower(i12) like '%whiskey%'
    or lower(i13) like '%whiskey%'
    or lower(i14) like '%whiskey%'
    or lower(i15) like '%whiskey%')
 order by drink_name
;
            ''')

crsr.execute(query1)
result1 = crsr.fetchall()

print(f'_____________________________________________________________________\n\n4/a. Which alcoholic drinks can be mixed with lemon and whiskey?\n')
pprint.pprint(result1)




# 4/b. "Which drink(s) can be mixed with just 15g of Sambuca?"

# setting up temporary tables in order to avoid multiple level nest/subqueries
queryTmp = (f'''
create temporary table tmp1 as
select
     t.drink_id
  from (
        select
             drink_id
            ,drink_name
            ,case when lower(i1 ) like '%sambuca%' then 1 else 0 end as i1
            ,case when lower(i2 ) like '%sambuca%' then 1 else 0 end as i2
            ,case when lower(i3 ) like '%sambuca%' then 1 else 0 end as i3
            ,case when lower(i4 ) like '%sambuca%' then 1 else 0 end as i4
            ,case when lower(i5 ) like '%sambuca%' then 1 else 0 end as i5
            ,case when lower(i6 ) like '%sambuca%' then 1 else 0 end as i6
            ,case when lower(i7 ) like '%sambuca%' then 1 else 0 end as i7
            ,case when lower(i8 ) like '%sambuca%' then 1 else 0 end as i8
            ,case when lower(i9 ) like '%sambuca%' then 1 else 0 end as i9
            ,case when lower(i10) like '%sambuca%' then 1 else 0 end as i10
            ,case when lower(i11) like '%sambuca%' then 1 else 0 end as i11
            ,case when lower(i12) like '%sambuca%' then 1 else 0 end as i12
            ,case when lower(i13) like '%sambuca%' then 1 else 0 end as i13
            ,case when lower(i14) like '%sambuca%' then 1 else 0 end as i14
            ,case when lower(i15) like '%sambuca%' then 1 else 0 end as i15
          from cocktails
        ) t
 where (t.i1+t.i2+t.i3+t.i4+t.i5+t.i6+t.i7+t.i8+
         t.i9+t.i10+t.i11+t.i12+t.i13+t.i14+t.i15) >= 1
;

create temporary table tmp2 as
select
    drink_id
   ,drink_name
   ,case when lower(i1 ) like '%sambuca%' then i1  else null end as i1
   ,case when lower(i2 ) like '%sambuca%' then i2  else null end as i2
   ,case when lower(i3 ) like '%sambuca%' then i3  else null end as i3
   ,case when lower(i4 ) like '%sambuca%' then i4  else null end as i4
   ,case when lower(i5 ) like '%sambuca%' then i5  else null end as i5
   ,case when lower(i6 ) like '%sambuca%' then i6  else null end as i6
   ,case when lower(i7 ) like '%sambuca%' then i7  else null end as i7
   ,case when lower(i8 ) like '%sambuca%' then i8  else null end as i8
   ,case when lower(i9 ) like '%sambuca%' then i9  else null end as i9
   ,case when lower(i10) like '%sambuca%' then i10 else null end as i10
   ,case when lower(i11) like '%sambuca%' then i11 else null end as i11
   ,case when lower(i12) like '%sambuca%' then i12 else null end as i12
   ,case when lower(i13) like '%sambuca%' then i13 else null end as i13
   ,case when lower(i14) like '%sambuca%' then i14 else null end as i14
   ,case when lower(i15) like '%sambuca%' then i15 else null end as i15
   ,case when lower(i1 ) like '%sambuca%' then m1  else null end as m1
   ,case when lower(i2 ) like '%sambuca%' then m2  else null end as m2
   ,case when lower(i3 ) like '%sambuca%' then m3  else null end as m3
   ,case when lower(i4 ) like '%sambuca%' then m4  else null end as m4
   ,case when lower(i5 ) like '%sambuca%' then m5  else null end as m5
   ,case when lower(i6 ) like '%sambuca%' then m6  else null end as m6
   ,case when lower(i7 ) like '%sambuca%' then m7  else null end as m7
   ,case when lower(i8 ) like '%sambuca%' then m8  else null end as m8
   ,case when lower(i9 ) like '%sambuca%' then m9  else null end as m9
   ,case when lower(i10) like '%sambuca%' then m10 else null end as m10
   ,case when lower(i11) like '%sambuca%' then m11 else null end as m11
   ,case when lower(i12) like '%sambuca%' then m12 else null end as m12
   ,case when lower(i13) like '%sambuca%' then m13 else null end as m13
   ,case when lower(i14) like '%sambuca%' then m14 else null end as m14
   ,case when lower(i15) like '%sambuca%' then m15 else null end as m15
  from cocktails
 where drink_id in (select * from tmp1)
;

create temporary table tmp3 as
select drink_id ,drink_name ,max(i1 ) over (partition by drink_id) as ingredient ,max(m1 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i2 ) over (partition by drink_id) as ingredient ,max(m2 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i3 ) over (partition by drink_id) as ingredient ,max(m3 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i4 ) over (partition by drink_id) as ingredient ,max(m4 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i5 ) over (partition by drink_id) as ingredient ,max(m5 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i6 ) over (partition by drink_id) as ingredient ,max(m6 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i7 ) over (partition by drink_id) as ingredient ,max(m7 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i8 ) over (partition by drink_id) as ingredient ,max(m8 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i9 ) over (partition by drink_id) as ingredient ,max(m9 ) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i10) over (partition by drink_id) as ingredient ,max(m10) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i11) over (partition by drink_id) as ingredient ,max(m11) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i12) over (partition by drink_id) as ingredient ,max(m12) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i13) over (partition by drink_id) as ingredient ,max(m13) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i14) over (partition by drink_id) as ingredient ,max(m14) over (partition by drink_id) as quantity from tmp2
union
select drink_id ,drink_name ,max(i15) over (partition by drink_id) as ingredient ,max(m15) over (partition by drink_id) as quantity from tmp2
;

            ''')

crsr.executescript(queryTmp)


# qunatity conversions and final transformation on prefiltered sambuca cocktails
query2 = (f'''
select
     drink_id
    ,drink_name
    ,cast(gramm as text) || " g" as sambuca_quantity
  from (    
        select
            *
            ,case when measure like '%shot%'  then case when volume like '%/%' then (left_op / right_op) else volume end * 30
                          when measure like '%glass%' then case when volume like '%/%' then (left_op / right_op) else volume end * 147.86
                          when measure like '%oz%'    then case when volume like '%/%' then (left_op / right_op) else volume end * 28.35
                          when measure like '%cl%'    then case when volume like '%/%' then (left_op / right_op) else volume end * 10
                          when measure like '%ml%'    then case when volume like '%/%' then (left_op / right_op) else volume end
                          else 0 end as gramm
          from (
                select
                    *
                    ,(substr(quantity, 0, instr(quantity, ' '))) as volume
                    ,cast((case when quantity like '%/%' then substr(quantity, 0, instr(quantity, '/'))   else quantity end) as real) as left_op
                    ,cast((case when quantity like '%/%' then substr(quantity, instr(quantity, '/')+1, 1) else quantity end) as real) as right_op
                    ,substr(quantity,instr(quantity, ' ')) as measure
                  from tmp3
                 where ingredient is not null
                )
        )
where gramm between 14 and 16
''')

crsr.execute(query2)
result2 = crsr.fetchall()

print(f'_____________________________________________________________________\n\n4/b. Which drink(s) can be mixed with just 15g of Sambuca?\n ')
pprint.pprint(result2)


# 4/c. "Which drink has the most ingredients?"

query3 = (f'''
select
     t2.drink_id
    ,t2.drink_name
    ,max(t2.num_ingredients)
  from (
        select
             t.drink_id
            ,t.drink_name
            ,(t.i1+t.i2+t.i3+t.i4+t.i5+t.i6+t.i7+t.i8+t.i9
                 +t.i10+t.i11+t.i12+t.i13+t.i14+t.i15) as num_ingredients
          from (
                select
                    drink_id
                   ,drink_name
                   ,case when i1 is null then 0 else 1 end as i1
                   ,case when i2 is null then 0 else 1 end as i2
                   ,case when i3 is null then 0 else 1 end as i3
                   ,case when i4 is null then 0 else 1 end as i4
                   ,case when i5 is null then 0 else 1 end as i5
                   ,case when i6 is null then 0 else 1 end as i6
                   ,case when i7 is null then 0 else 1 end as i7
                   ,case when i8 is null then 0 else 1 end as i8
                   ,case when i9 is null then 0 else 1 end as i9
                   ,case when i9 is null then 0 else 1 end as i10
                   ,case when i11 is null then 0 else 1 end as i11
                   ,case when i11 is null then 0 else 1 end as i11
                   ,case when i12 is null then 0 else 1 end as i12
                   ,case when i13 is null then 0 else 1 end as i13
                   ,case when i14 is null then 0 else 1 end as i14
                   ,case when i15 is null then 0 else 1 end as i15
                  from cocktails
                 where 1=1
               ) t
       ) t2
;
            ''')

crsr.execute(query3)
result3 = crsr.fetchall()

print(f'_____________________________________________________________________\n\n4/c. Which drink has the most ingredients?\n')
pprint.pprint(result3)

connectSQLite.close()
print(f'\r\n\nDB connection has been closed. (the_cocktail.db)\n')