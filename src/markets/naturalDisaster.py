def disaster(data):
    # Find the highest item in realEstate and land
    highest = ""
    for i in data["assets"]:
        if i == "realestate" or i == "land":
            for item in data["assets"][i]:
                print(item)
    return data
