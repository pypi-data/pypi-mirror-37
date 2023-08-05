# -*- coding: utf-8 -*-
class Lineage(object):
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.name = ""
        self.val = val

    def eval(self, prefix, is_tail):
        f = Formatter()
        print(prefix + ("└───" if is_tail else "├───")+ self.val)
        if self.right is not None:
            self.right.eval(prefix + ("     " if is_tail else "│    "), False)
        if self.left is not None:
            self.left.eval(prefix + ("     " if is_tail else "│    "), True)

    def output(self):
        print(self.name)
        self.eval("", True)

class colors:
    INACTIVE = '\033[31m'
    ALUM = '\033[33m'
    BOLD = '\033[1m'
    END = '\033[0m'
    BIG = '\033[36m'

class Formatter():
    alum = lambda self, name: colors.ALUM + name + colors.END
    bold = lambda self, name: colors.BOLD + name + colors.END
    big = lambda self, name: colors.BIG + name + colors.END
    inactive = lambda self, name: colors.INACTIVE + name + colors.END

#-------------------------------------------------------------------------------------------------------------------------

def lineage_builder():
    f = Formatter()
    lineages = []

    royalty = Lineage(f.alum('Aneesh Jindal'))
    royalty.name = f.bold("Royalty")
    royalty.left = Lineage('Abhinav Koppu')
    royalty.left.left = Lineage('Victor Sun')
    royalty.left.left.left = Lineage('Sumukh Shivakumar')
    royalty.left.left.left.left = Lineage('Kanyes Thaker')
    royalty.left.left.left.left.left = Lineage(f.big('Ayush Kumar'))
    royalty.left.left.left.left.left.left = Lineage("Vaibhav Gattani")
    
    mabgs = Lineage('Kevin Jiang')
    mabgs.name = f.bold("mABGs")
    mabgs.left = Lineage('Candice Ye')
    mabgs.right = Lineage('Sharie Wang')
    mabgs.left.left = Lineage(f.inactive('Amy Shen'))
    mabgs.left.left.left = Lineage('Xin Yi Chen')
    mabgs.left.left.left.left = Lineage(f.big('Angela Dong'))
    mabgs.left.left.left.left.left = Lineage("Kayli Jiang")
    mabgs.right.left = Lineage('Paul Shao')

    mdbros = Lineage(f.alum('Akkshay Khoslaa'))
    mdbros.name = f.bold("MDBros")
    mdbros.left = Lineage('Vineeth Yeevani')
    mdbros.left.left = Lineage(f.big('Japjot Singh'))
    mdbros.left.left.left = Lineage("Sai Yandapalli")

    sahils_lineage = Lineage(f.alum('Sahil Lamba'))
    sahils_lineage.left = Lineage(f.inactive('Mudit Mittal'))
    sahils_lineage.left.left = Lineage(f.inactive('Emaan Hariri'))
    sahils_lineage.left.left.left = Lineage(f.big('Levi Walsh'))
    sahils_lineage.left.left.left.right = Lineage("Ajay Raj Merchia")
    sahils_lineage.left.left.left.left = Lineage(f.big('Joey Hejna'))
    sahils_lineage.left.left.left.left.left = Lineage(f.big('Ethan Wong'))
    sahils_lineage.left.left.left.left.right = Lineage("Shomil Jain")
    sahils_lineage.left.left.left.left.left.left = Lineage("Shubha Jagannatha")

    krishnans_lineage = Lineage(f.alum('Krishnan Rajiyah'))
    krishnans_lineage.left = Lineage('Zach Govani')
    krishnans_lineage.left.right = Lineage('Stephen Jayakar')
    krishnans_lineage.left.left = Lineage(f.big('Tigersunny Chen'))
    krishnans_lineage.left.left.left = Lineage("Andres Medrano")
    krishnans_lineage.left.right.left = Lineage(f.big('Julie Deng'))
    krishnans_lineage.left.right.left.left = Lineage("Kiana Go")

    mansis_lineage = Lineage(f.inactive("Mansi Shah"))
    mansis_lineage.left = Lineage("Shreya Reddy")
    mansis_lineage.left.right = Lineage(f.inactive("Julia Luo"))
    mansis_lineage.left.left = Lineage(f.big("Niky Arora"))
    mansis_lineage.left.left.left = Lineage("Anmol Parande")

    peters_lineage = Lineage(f.inactive('Peter Schafhalter'))
    peters_lineage.left = Lineage(f.big('Aayush Tyagi'))
    peters_lineage.left.right = Lineage("Austin Davis")
    peters_lineage.left.left = Lineage(f.big('Mudabbir Khan'))
    peters_lineage.left.left.left = Lineage("Michelle Mao")

    codys_lineage = Lineage("Cody Hsieh")
    codys_lineage.left = Lineage(f.inactive("Kedar Thakkar"))
    codys_lineage.left.left = Lineage("Daniel Andrews")
    codys_lineage.left.left.right = Lineage(f.inactive("Kaden Dippe"))
    codys_lineage.left.left.left = Lineage(f.big("Will Oakley"))
    codys_lineage.left.left.left.left = Lineage("Brandon David")
    codys_lineage.left.left.right.left = Lineage("Fang Shuo")

    shaans_lineage = Lineage(f.inactive("Shaan Appel"))
    shaans_lineage.left = Lineage(f.inactive("Mohit Katyal"))
    shaans_lineage.left.left = Lineage("Noah Pepper")
    shaans_lineage.left.left.left = Lineage(f.big("Max Miranda"))
    shaans_lineage.left.left.left.left = Lineage("Anand Chandra")

    ashwins_lineage = Lineage(f.inactive("Ashwin Vaidyanathan"))
    ashwins_lineage.left = Lineage(f.inactive("Jessica Chen"))
    ashwins_lineage.left.left = Lineage("Sarah Tang")
    ashwins_lineage.left.left.right = Lineage(f.inactive("Annie Tang"))
    ashwins_lineage.left.left.left = Lineage(f.big("Natasha Wong"))
    ashwins_lineage.left.left.left.left = Lineage("Alcoholic")

    aparnas_lineage = Lineage(f.alum('Aparna Krishnan'))
    aparnas_lineage.left = Lineage('Shubham Goenka')
    aparnas_lineage.left.left = Lineage('Shivendra Kushwah')
    aparnas_lineage.left.left.left = Lineage(f.big('Shubham Gupta'))
    aparnas_lineage.left.left.left.left = Lineage("Jaiveer Singh")

    jessicas_lineage = Lineage(f.inactive('Jessica Ji'))
    jessicas_lineage.left = Lineage('Vidya Ravikumar')
    jessicas_lineage.left.left = Lineage(f.big('Radhika Dhomse'))
    jessicas_lineage.left.left.right = Lineage("Anika Bagga")
    jessicas_lineage.left.left.left = Lineage(f.inactive('Samanvi Rai'))

    kristins_lineage = Lineage(f.alum("Kristin Ho"))
    kristins_lineage.left = Lineage(f.inactive("Carol Wang"))
    kristins_lineage.left.left =Lineage("Aditya Yadav")

    connors_lineage = Lineage(f.alum("Connor Killion"))
    connors_lineage.left = Lineage(f.inactive("Eliot Han"))
    connors_lineage.left.left = Lineage("Boris Yue")
    connors_lineage.left.left.left = Lineage(f.inactive("Suyash Gupta"))

    jareds_lineage = Lineage(f.inactive("Jared Gutierrez"))
    jareds_lineage.left = Lineage("Eric Kong")
    jareds_lineage.left.left = Lineage(f.inactive("Louie McConnell"))

    taruns_lineage = Lineage('Tarun Khasnavis')
    taruns_lineage.left = Lineage(f.inactive("Ben Goldberg"))
    taruns_lineage.left.left = Lineage(f.inactive("Mark Siano"))

    youngs_lineage = Lineage(f.inactive("Young Lin"))
    youngs_lineage.left = Lineage("Leon Kwak")
    youngs_lineage.left.left = Lineage(f.inactive("Adhiraj Datar"))

    jeffrys_lineage = Lineage(f.inactive("Jeffrey Zhang"))
    jeffrys_lineage.left = Lineage("Rochelle Shen")
    jeffrys_lineage.left.left = Lineage(f.inactive("Shireen Warrier"))

    justins_lineage = Lineage(f.alum("Justin Kim"))
    justins_lineage.left = Lineage("Srujay Korlakunta")

    sirjans_lineage = Lineage(f.alum("Sirjan Kafle"))
    sirjans_lineage.left = Lineage("Sayan Paul")

    lineages.extend([royalty, mabgs, mdbros, sahils_lineage, krishnans_lineage, mansis_lineage, peters_lineage, codys_lineage, shaans_lineage, ashwins_lineage, aparnas_lineage, jessicas_lineage, kristins_lineage, connors_lineage, jareds_lineage, taruns_lineage, youngs_lineage, jeffrys_lineage, justins_lineage])



    return lineages

def class_builder():
    f = Formatter()
    classes = []
    alpha_class = [f.bold("ALPHA CLASS, FALL 2015: "), 'Abhinav Koppu', 'Akkshay Khoslaa', 'Aneesh Jindal', 'Aparna Krishnan', 'Ashwin Vaidyanathan', 'Cody Hsieh', 'Connor Killion', 'Jeffrey Zhang', 'Julie Deng #1', 'Justin Kim', 'Krishnan Rajiyah', 'Lisa Lee', 'Peter Schafhalter', 'Sahil Lamba', 'Sameer Suresh', 'Sirjan Kafle', 'Tarun Khasnavis']
    beta_class = [f.bold("BETA CLASS, SPRING 2016: "), 'Alice Wang', 'Christine Munar', 'Edward Liu', "Eric D'sa", 'Jared Gutierrez', 'Jessica Cherny', 'Jessica Ji', 'Kevin Jiang', 'Kristin Ho', 'Mansi Shah', 'Mudit Mittal', 'Richard Hu', 'Shaan Appel', 'Wilbur Shi', 'Young Lin']
    gamma_class = [f.bold("GAMMA CLASS, FALL 2016: "), 'Aayush Tyagi', 'Ben Goldberg', 'Candice Ye', 'Eliot Han', 'Emaan Hariri', 'Jessica Chen', 'Katharine Jiang', 'Kedar Thakkar', 'Leon Kwak', 'Mohit Katyal', 'Rochelle Shen', 'Sayan Paul', 'Sharie Wang', 'Shreya Reddy', 'Shubham Goenka', 'Victor Sun', 'Vidya Ravikumar']
    delta_class = [f.bold("DELTA CLASS, SPRING 2017: "),'Adhiraj Datar', 'Amy Shen', 'Boris Yue', 'Daniel Andrews', 'Eric Kong', 'Julia Luo', 'Levi Walsh', 'Mark Siano', 'Radhika Dhomse', 'Sarah Tang', 'Shireen Warrier', 'Shivendra Kushwah', 'Sumukh Shivakumar', 'Zach Govani']
    epsilon_class = [f.bold("EPSILON CLASS, FALL 2017: "), 'Annie Tang', 'Carol Wang', 'Joey Hejna', 'Kaden Dippe', 'Kanyes Thaker', 'Louie McConnell', 'Noah Pepper', 'Samanvi Rai', 'Srujay Korlakunta', 'Stephen Jayakar', 'Suyash Gupta', 'Vineeth Yeevani', 'Xin Yi Chen']
    zeta_class = [f.bold("ZETA CLASS, SPRING 2018: "), 'Aditya Yadav', 'Angela Dong', 'Ayush Kumar', 'Ethan Wong', 'Fang Shuo', 'Japjot Singh', 'Julie Deng #2', 'Max Miranda', 'Mudabbir Khan', 'Natasha Wong', 'Niky Arora', 'Paul Shao', 'Shubham Gupta', 'Tigersunny Chen', 'Will Oakley']
    eta_class = [f.bold("ETA CLASS, FALL 2019: "), 'Ajay Merchia', 'Anand Chandra', 'Andres Medrano', 'Anika Bagga', 'Anmol Parande', 'Austin Davis', 'Brandon David', 'Isabella Lau', 'Jaiveer Singh', 'Kayli Jiang', 'Kiana Go', 'Michelle Mao', 'Sai Yandapalli', 'Shomil Jain', 'Shuba Jagannatha', 'Vaibhav Gattani']
    classes.extend([alpha_class, beta_class, gamma_class, delta_class, epsilon_class, zeta_class, eta_class])
    return classes

def relationship_builder():
    f = Formatter()
    relationships = []
    tigerchelley = f.inactive("~~~~~~ Tigersunny Chen   ❤   Rochelle Shen ~~~~~~")
    shivendradihka = f.inactive("~~~~~ Radhika Dhomse   ❤   Shivendra Kushwah~~~~~")
    vicyi = f.inactive("~~~~~~~~ Xin Yi Chen     ❤     Victor Sun~~~~~~~~")
    relationships.extend([tigerchelley, shivendradihka, vicyi])
    return relationships

def main():
    f = Formatter()

    print("\n───────────────────────CLASSES───────────────────────\n")
    for year in class_builder():
        print(year[0] + "\n" + ", ".join(year[1:]) + '\n')

    print("\n───────────────────────LINEAGES───────────────────────\n")
    for lineage in lineage_builder():
        lineage.output()

    print("\n───────────────────────KEY───────────────────────\n")
    print(f.bold("Akkshay Khoslaa") + ": Family name")
    print(f.big("Akkshay Khoslaa") + ": Big for this semester")
    print(f.inactive("Akkshay Khoslaa") + ": Inactive member")
    print(f.alum("Akkshay Khoslaa") + ": MDB Alum")
    print()


if __name__ == "__main__":
    main()


