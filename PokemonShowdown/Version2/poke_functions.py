"""
Functions used for webscraping data from Pokemon Showdown

Functions include:
"""

#function accepts the starting url and tier you want to extract data from,
#then it runs through all the links and extracts the data based on the desired tier
def scrape_starter_usage_data(url,tier,filename):
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    PATH = '/Users/frankpang/Downloads/chromedriver'
    driver = webdriver.Chrome(PATH)

    driver.get(url)
    #gets all links for dates where data is stored and puts into a list to loop through
    elems = driver.find_elements_by_css_selector("[href]")
    links = [elem.get_attribute('href') for elem in elems]

    # Final dataframe where all the data is stored
    usage_data = pd.DataFrame()

    print("Links scraped:")
    for link in links[1:]:
        driver.get(link)
        sub_elems = driver.find_elements_by_css_selector("[href]")
        sub_links = [elem.get_attribute('href') for elem in sub_elems]
        # takes the x numbered link from each year (2nd for leads)
        for sub_link in sub_links[2:3]:
            driver.get(sub_link)
            sub_sub_elems = driver.find_elements_by_css_selector("[href]")
            sub_sub_links = [elem.get_attribute('href') for elem in sub_sub_elems]
            for sub_sub_link in sub_sub_links:
                if tier in sub_sub_link:
                    print(sub_sub_link[:-3] + "txt")
                    driver.get(sub_sub_link)

                    # gets text in raw format to make into table
                    texts = driver.find_element_by_xpath(
                        "//pre[@style='word-wrap: break-word; white-space: pre-wrap;']")
                    # splits text by lines
                    text_data_raw = texts.text.split("\n")

                    # creates and cleans the column headers
                    columns = text_data_raw[2].strip().split("|")[1:-1]
                    for i in range(0, len(columns)):
                        new = columns[i].strip()
                        columns[i] = columns[i].replace(columns[i], new)

                    # cleans rows of data
                    data_raw = text_data_raw[4:-1]
                    data = []
                    for i in range(0, len(data_raw)):
                        row = data_raw[i].strip().split("|")[1:-1]
                        for i in range(0, len(row)):
                            new = row[i].strip()
                            row[i] = row[i].replace(row[i], new)
                        data.append(row)

                    # creates dataframe with rows of data and columns
                    poke_df = pd.DataFrame(data, columns=columns)

                    url_info = url_data(str(sub_sub_link))
                    poke_df["date"] = url_info[0]
                    poke_df["tier"] = url_info[1]
                    poke_df["battle_type"] = url_info[2]
                    usage_data = usage_data.append(poke_df)

    driver.close()
    usage_data.to_csv(filename, index=False)
    print("Done!")


# function accepts a url as input and returns the revelant data from the link such as date and tier info
def url_data(url):
    url_list=url.split("/")

    date_data = url_list[4]

    tier_data = url_list[-1]
    tier_data = tier_data[:-4]

    if "double" in url:
        battle_data = "Doubles"
    else:
        battle_data = "Singles"
    return [date_data,tier_data,battle_data]

def scrape_pokedex(url,filename):
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time

    PATH = '/Users/frankpang/Downloads/chromedriver'
    driver = webdriver.Chrome(PATH)
    columns = ["Name", "Typing", "Size", "Abilities", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed",
               "Total Base Stats"]

    driver.get(url)
    time.sleep(10)
    elems = driver.find_elements_by_css_selector("[href]")
    links = [elem.get_attribute('href') for elem in elems][12:]
    pokedex = []

    for link in links[1050:]:
        poke_list = []
        driver.get(link)
        name = driver.find_element_by_class_name("subtle").text

        types_raw = driver.find_element_by_class_name("typeentry")
        types_formatted = types_raw.text.split("\n")[-1].replace(" ", ",")

        size = driver.find_element_by_class_name("sizeentry").text.split("\n")[1]
        try:
            ability = driver.find_element_by_class_name("abilityentry").text.split("\n")[1].replace(" | ", ",").replace(
                " (H)", "")
        except IndexError:
            ability="N/A"

        poke_list.extend([name, types_formatted, size, ability])

        stats_raw = driver.find_element_by_class_name("stats").text.split("\n")[1::2]
        stats_clean = [i.split(": ")[1].replace(" at level", "") for i in stats_raw]
        poke_list.extend(stats_clean)
        pokedex.append(poke_list)

    pokemon_table = pd.DataFrame(pokedex, columns=columns)
    pokemon_table.to_csv(filename, index=False)
    print("Created Pokedex")

    driver.close()


def scrape_moveset_data(url,tier,filename):
    import pandas as pd
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    PATH = '/Users/frankpang/Downloads/chromedriver'
    driver = webdriver.Chrome(PATH)

    driver.get(url)
    #gets all links for dates where data is stored and puts into a list to loop through
    elems = driver.find_elements_by_css_selector("[href]")
    links = [elem.get_attribute('href') for elem in elems]

    # Final dataframe where all the data is stored
    moveset_data = pd.DataFrame()

    print("Links scraped:")

    # loops through list of links and takes the xth link to get moveset
    for link in links[1:]:
        driver.get(link)
        sub_elems = driver.find_elements_by_css_selector("[href]")
        sub_links = [elem.get_attribute('href') for elem in sub_elems]

        # needs an if statement because the moveset link is not always in the same place
        for sub_link in sub_links[5:7]:
            if "moveset" in sub_link:

                # try statement used to catch any empty pages
                try:
                    driver.get(sub_link)
                    sub_sub_elems = driver.find_elements_by_css_selector("[href]")
                    sub_sub_links = [elem.get_attribute('href') for elem in sub_sub_elems]
                    for sub_sub_link in sub_sub_links:
                        if tier in sub_sub_link:
                            print(sub_sub_link[:-3] + "txt")
                            driver.get(sub_sub_link)

                            # gets text in raw format to make into table
                            texts = driver.find_element_by_xpath(
                                "//pre[@style='word-wrap: break-word; white-space: pre-wrap;']")
                            # splits text by lines
                            text_data_raw = texts.text.split("+----------------------------------------+")

                            # create separate list for each columns of data to be collected
                            # columns with multiple elements and percent data will be added as dictionary
                            pokemon = []
                            usage = []
                            ability = []
                            item = []
                            ev = []
                            moves = []
                            teammates = []
                            checks = []


                            # cleans rows of data
                            data_raw = text_data_raw[1:-1]

                            #since data is stored vertically, counter is used to add data to each new
                            #column
                            counter = 0

                            # splits data by rows
                            for i in range(0, len(data_raw)):
                                if counter!=8:
                                    row = data_raw[i].strip().split("|")[1:-1]
                                    #Removes all "\n" from list of values per row
                                    if " \n " in row:
                                        row = list(filter((" \n ").__ne__, row))
                                    for i in range(0, len(row)):
                                        new = row[i].strip()
                                        row[i] = row[i].replace(row[i], new)

                                    #add data to specific column lists

                                    #adds pokemon to pokemon list
                                    if counter==0:
                                        pokemon.append(row[0])
                                        #print(pokemon)

                                    #adds usage count per pokemon
                                    elif counter==1:
                                        use_count = row[0].split(": ")
                                        usage.append(use_count[1])

                                    #creates a dictionary for abilities and percent usage
                                    elif counter==2:
                                        ability_dict={}
                                        for i in range(1,len(row)):
                                            ability_name = row[i][:-8].strip()
                                            ability_num = row[i][-8:].strip()
                                            ability_dict[ability_name]=ability_num
                                        ability.append(ability_dict)

                                    # creates a dictionary for items and percent usage
                                    elif counter==3:
                                        item_dict = {}
                                        for i in range(1, len(row)):
                                            item_name = row[i][:-8].strip()
                                            item_num = row[i][-8:].strip()
                                            item_dict[item_name] = item_num
                                        item.append(item_dict)

                                    # creates a dictionary for EV spreads and percent usage
                                    elif counter==4:
                                        ev_dict = {}
                                        for i in range(1, len(row)):
                                            ev_name = row[i][:-8].strip()
                                            ev_num = row[i][-8:].strip()
                                            ev_dict[ev_name] = ev_num
                                        ev.append(ev_dict)

                                    # creates a dictionary for moves and percent usage
                                    elif counter==5:
                                        moves_dict = {}
                                        for i in range(1, len(row)):
                                            moves_name = row[i][:-8].strip()
                                            moves_num = row[i][-8:].strip()
                                            moves_dict[moves_name] = moves_num
                                        moves.append(moves_dict)

                                    # creates a dictionary for teammates and percent usage
                                    elif counter==6:
                                        teammates_dict = {}
                                        for i in range(1, len(row)):
                                            teammates_name = row[i][:-8].strip()
                                            teammates_num = row[i][-8:].strip()
                                            teammates_dict[teammates_name] = teammates_num
                                        teammates.append(teammates_dict)

                                    # creates a dictionary for checks/counters and percent usage
                                    elif counter==7:
                                        checks_dict = {}
                                        for i in range(1, len(row)):
                                            checks_name = row[i][:-8].strip()
                                            checks_num = row[i][-8:].strip()
                                            checks_dict[checks_name] = checks_num
                                        checks.append(checks_dict)

                                    counter+=1

                                #resets the counter once one row has been collected
                                elif counter==8:
                                    counter=0

                            # creates dataframe with rows of data and columns
                            columns = ["Pokemon", "raw_usage", "Ability", "Item", "EV Spread", "Moves", "Teammates",
                                       "Checks & Counters"]
                            d = {"Pokemon":pokemon,"Raw Usage":usage,"Ability":ability,"Item":item,"EV Spread":ev,
                                 "Moves":moves,"Teammates":teammates,"Checks & Counters":checks}
                            poke_df = pd.DataFrame(data=d)

                            # adds additional info on date, tier, and single/double battle
                            url_info = url_data(str(sub_sub_link))
                            poke_df["date"] = url_info[0]
                            poke_df["tier"] = url_info[1]
                            poke_df["battle_type"] = url_info[2]
                            moveset_data = moveset_data.append(poke_df)

                # any empty pages will be skipped and noted
                except selenium.common.exceptions.NoSuchElementException:
                    print("skipping " + sub_sub_link[:-3] + "txt")

    driver.close()
    moveset_data.to_csv(filename, index=False)
    print("Done!")

def check_urls(url,tier):
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    PATH = '/Users/frankpang/Downloads/chromedriver'
    driver = webdriver.Chrome(PATH)

    driver.get(url)
    #gets all links for dates where data is stored and puts into a list to loop through
    elems = driver.find_elements_by_css_selector("[href]")
    links = [elem.get_attribute('href') for elem in elems]

    # Final dataframe where all the data is stored
    usage_data = pd.DataFrame()

    print("Links scraped:")
    for link in links[1:]:
        driver.get(link)
        sub_elems = driver.find_elements_by_css_selector("[href]")
        sub_links = [elem.get_attribute('href') for elem in sub_elems]
        #takes the x numbered link from each year (5th for moveset)
        for sub_link in sub_links[5:7]:
            if "moveset" in sub_link:
                try:
                    driver.get(sub_link)
                    sub_sub_elems = driver.find_elements_by_css_selector("[href]")
                    sub_sub_links = [elem.get_attribute('href') for elem in sub_sub_elems]
                    for sub_sub_link in sub_sub_links:
                        if tier in sub_sub_link:
                            print(sub_sub_link[:-3] + "txt")
                except selenium.common.exceptions.NoSuchElementException:
                    print("skipping " + sub_sub_link[:-3] + "txt")
