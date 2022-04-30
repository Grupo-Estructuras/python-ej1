import matplotlib.pyplot as plt


def createBarChart(langDataArr):
    fig = plt.figure(figsize = (10, 6))
    langs = [language["name"] for language in langDataArr]
    repoAmmount = [language["repoAmmount"] for language in langDataArr]
    
    plt.bar(langs[0:10], repoAmmount[0:10], color ='orange', width = 0.420)
    plt.xlabel("Lenguajes")
    plt.ylabel("Apariciones")
    plt.show()
