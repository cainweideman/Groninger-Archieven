def create_page_object(year, page_number, person_list):
    return {
        "year": year,
        "page": page_number,
        "register": person_list,
    }