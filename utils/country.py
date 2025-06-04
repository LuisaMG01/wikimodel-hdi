import pycountry

class Country:
    def get_country_list(self):
        country_list = []
        for country in pycountry.countries:
            country_info = {
                'name': country.name, 
                'alpha_2': country.alpha_2
            }
            country_list.append(country_info)
        
        return country_list
