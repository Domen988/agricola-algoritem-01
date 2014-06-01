class Cohort:
    'nosi vse lastnosti kohorte in tudi njeno casovno zgodovino'
    cohCount = 0

    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.GER = 0
        self.SUS = 0
        self.WD = 0
        self.TWD = 0
        self.Tsum = 0
        self.INC1 = 0
        self.INC2 = 0
        self.GERhistory = []
        Cohort.cohCount += 1

    def set_GER(self, currentGER):
        self.GER = currentGER
        self.GERhistory.append(currentGER)

    def GERstart(self):
        self.GERstart = None

    def fi(self):
        self.fi = None

    def PMO(self):
        """test"""
        self.PMO = 0

    def SUS(self):
        """Survival of sporangia"""
        self.SUS = 0

    def WD(self):
        """Duration of wetness"""
        self.WD = 0

    def TWD(self):
        """Average T for the wet period"""
        self.TWD = 0

    def Tsum(self):
        """sum of temperatures in whet hours"""
        self.Tsum = 0

    def REL(self):
        self.REL = 0

    def ro(self):
        """Time of the zoospore release"""
        self.ro = None

    def ZREstage(self):
        """True if ZRE happens"""
        self.ZREstage = False

    def delta(self):
        """zoospores dispersed time"""
        self.delta = None

    def alfa(self):
        self.alfa = None

    def tau(self):
        """Oil spots formation time"""
        self.tau = None

    def ZDIstage(self):
        """True if ZDI happens"""
        self.ZDIstage = False

    def ZINstage(self):
        """True if ZIN happens"""
        self.ZINstage = False

    def OSLstage(self):
        """True if OSL happens"""
        self.OSLstage = False

    def INC1(self):
        """Incubation progress confidence interval top border"""
        self.INC1 = 0

    def INC2(self):
        """Incubation progress confidence interval bottom border"""
        self.INC2 = 0