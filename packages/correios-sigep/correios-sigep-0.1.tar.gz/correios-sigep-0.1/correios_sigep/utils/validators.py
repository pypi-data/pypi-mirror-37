def get_dv_cep(cep):
    if not isinstance(cep, str):
        raise Exception('cep must be a valid string')
    
    lst_number = [int(n) for n in cep]
    sum_cep = sum(lst_number)
    mod = sum_cep + (10 - sum_cep % 10)

    return mod - sum_cep