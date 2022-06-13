def mentor(data):
    data["mentor"] = 3


def decrementMentor(data):
    if data["mentor"] > 0:
        data["mentor"] -= 1
        return True
    else:
        return False
