from collections import defaultdict


def compute_totals(totals: defaultdict(int), uomes: list) -> defaultdict(int):
    """
    Receive in input a dictionary containing previous computed totals and a list of
    UOMe with this form: {borrower, lender, value}. The output is a
    dictionary that associates to each user (borrower or lender) his own total.
    """    

    for uome in uomes:
        totals[uome[0]] -= uome[2] 
        totals[uome[1]] += uome[2]
        
    return totals


def borrowers_and_lenders(totals_dict: dict) -> (dict, dict):
    """
    Receive input a dictionary with a total associated to each user. 
    Outputs are two dictionaries listing borrowers and lenders with their
    respective total debt or credit
    """

    borrowers = {} 
    lenders = {}
    
    for user in totals_dict:
        if totals_dict[user] > 0:
            lenders[user] = totals_dict[user]
        elif totals_dict[user] < 0:
            borrowers[user] = abs(totals_dict[user])

    return borrowers, lenders


def debt_simplification(borrowers: dict, lenders: dict) -> dict:
    """
    Inputs are two dictionaries containing borrowers and lenders.
    The output is a list of simplified UOMe {lender, borrower, value}
    """
    
    simplified_debt = defaultdict(dict)
    for lender in sorted(lenders):
        for borrower in sorted(borrowers):
            credit, debit = lenders[lender], borrowers[borrower]
            
            if credit != 0 and debit != 0:
                transaction_value = min(credit, debit)
                simplified_debt[borrower][lender] = transaction_value

                if lenders[lender] >= borrowers[borrower]:
                    lenders[lender] -= transaction_value
                    borrowers[borrower] = 0
                else:
                    lenders[lender] = 0
                    borrowers[borrower] -= transaction_value
        
    return dict(simplified_debt)


def update_total_debt(current_totals: defaultdict(int), new_uomes: list) -> (defaultdict(int), dict):
    """
    Get the new state of the user graph when given a list of new UOMe's
    """

    new_totals = compute_totals(current_totals, new_uomes)
    new_user_debt = debt_simplification(*borrowers_and_lenders(new_totals))

    return new_totals, new_user_debt
