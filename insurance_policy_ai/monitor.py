import random

def check_policy_updates():

    companies = [
        "Aetna",
        "Cigna",
        "United Health",
        "Humana",
        "Blue Cross"
    ]

    policies = [
        "Cancer Coverage",
        "ICU Coverage",
        "Emergency Care",
        "Mental Health Coverage",
        "Surgery Coverage"
    ]

    updates = []

    for i in range(5):   # generate more policies

        status = random.choices(
            ["Changed", "Same"],
            weights=[70, 30]   # 70% changed, 30% same
        )[0]

        updates.append({
            "company": random.choice(companies),
            "policy_name": random.choice(policies),
            "status": status
        })

    return updates

