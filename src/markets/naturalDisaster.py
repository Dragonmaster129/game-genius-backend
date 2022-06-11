def disaster(data):
    # Find the highest item in realEstate and land
    # highest is a list for three items, the first being the category eg. realestate
    # the second being the index, and the third being the item's value
    highest = ["", 0]
    for i in data["assets"]:
        if i == "realestate" or i == "land":
            iteration = 0
            for item in data["assets"][i]:
                try:
                    if item["value"] > highest[2]:
                        highest = [i, iteration, item["value"]]
                    iteration += 1
                except IndexError:
                    highest = [i, iteration, item["value"]]
                    iteration += 1
    if highest[0] != "land":
        data["assets"][highest[0]][highest[1]]["value"] = 0
    data["assets"][highest[0]][highest[1]]["disaster"] = True

    return data
