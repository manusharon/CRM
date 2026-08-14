# generate_agencies.py
from faker import Faker
import random, csv

fake = Faker(['en_IN'])
states = ['Kerala','Tamil Nadu']
kerala_cities = ['Kochi','Thiruvananthapuram','Kozhikode','Kollam','Alappuzha','Thrissur','Palakkad','Kannur','Kottayam']
tn_cities = ['Chennai','Coimbatore','Madurai','Tiruchirappalli','Salem','Tirunelveli','Vellore','Erode']
specializations = [['UAE','Saudi','Qatar'], ['Schengen'], ['UK','US'], ['Thailand','Malaysia'], ['Bali','Indonesia']]

def gen_agency(i):
    state = random.choice(states)
    city = random.choice(kerala_cities if state=='Kerala' else tn_cities)
    name = f"{fake.last_name()} Travels {random.choice(['Pvt Ltd','Tours','Holidays','Agency'])}"
    slug = name.lower().replace(' ','-') + '-' + str(i)
    return {
        'name': name,
        'slug': slug,
        'primary_contact_name': fake.name(),
        'primary_contact_mobile': fake.phone_number(),
        'email': fake.company_email(),
        'address': fake.address().replace('\n',' '),
        'city': city,
        'district': city,
        'state': state,
        'pincode': fake.postcode(),
        'gst_number': '22' + ''.join([str(random.randint(0,9)) for _ in range(13)]),
        'pan': ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)]) + ''.join([str(random.randint(0,9)) for _ in range(4)]) + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'iata_code': random.choice([None] + [f'IATA{random.randint(100,999)}']),
        'website': fake.url(),
        'specialization_countries': '|'.join(random.choice(specializations)),
        'success_rate': round(random.uniform(70,99),2),
        'rating': round(random.uniform(3.5,5.0),2),
        'status': random.choice(['active','pending','suspended'])
    }

rows = 1500
with open('agencies_kerala_tn.csv','w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name','slug','primary_contact_name','primary_contact_mobile','email','address','city','district','state','pincode','gst_number','pan','iata_code','website','specialization_countries','success_rate','rating','status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(rows):
        writer.writerow(gen_agency(i+1))
print("CSV generated: agencies_kerala_tn.csv")
