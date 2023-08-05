def get_phone_number():
    pre_lst = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187",
"188"]
    return random.choice(pre_lst) + ''.join(random.sample(string.digits, 8))
