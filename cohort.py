class Cohort:
    'nosi vse lastnosti kohorte in tudi njeno casovno zgodovino'
    cohCount = 0

    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.GER = 0
        self.SUS = 0
        self.SUZ = 0
        self.WD = 0
        self.TWD = 0
        self.Tsum = 0
        self.WDZIN = 0
        self.TWDZIN = 0
        self.TsumZIN = 0
        self.INC1 = 0
        self.INC2 = 0
        self.fi = 0
        self.ZRE = 0
        self.ZDI = 0
        self.GEOstage = False
        self.ZREstage = False
        self.OSLstage = False
        self.ZINstage = False
        self.ZDIstage = False
        self.GERhistory = []

        self.alfa = 0
        self.delta = 0
        self.epsilon = 0
        self.fi = 0
        self.ro = 0
        self.tau1 = 0
        self.tau2 = 0
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

    def GEO(self):
        """germinated oospores"""
        self.GEO = 0

    def GEOstage(self):
        """true if GEO stage occured"""
        self.GEOstage = false

    def eta(self):
        """test"""
        self.eta = 0

    def SUS(self):
        """Survival of sporangia"""
        self.SUS = 0

    def SUZ(self):
        """"survival of zoospores"""
        self.SUZ = 0

    def WD(self):
        """Duration of wetness"""
        self.WD = 0

    def WDZIN(self):
        """wetness duration for calculating ZIN stage"""
        self.WDZIN = 0

    def TWD(self):
        """Average T for the wet period"""
        self.TWD = 0

    def TsumZIN(self):
        """sum of temperatures in whet hours for ZIN stage"""
        self.TsumZIN = 0

    def TWDZIN(self):
        """Average T for the wet period for ZIN stage"""
        self.TWDZIN = 0

    def Tsum(self):
        """sum of temperatures in whet hours"""
        self.Tsum = 0

    def REL(self):
        self.REL = 0

    def ro(self):
        """Time of the zoospore release"""
        self.ro = None

    def ZRE(self):
        """zoospores released"""
        self.ZRE = 0

    def ZREstage(self):
        """True if ZRE happens"""
        self.ZREstage = False

    def delta(self):
        """zoospores dispersed time"""
        self.delta = None

    def alfa(self):
        """time of zoospores infection"""
        self.alfa = None

    def tau1(self):
        """Oil spots formation time"""
        self.tau1 = None

    def tau2(self):
        """Oil spots formation time"""
        self.tau2 = None

    def ZDI(self):
        """zoospores dispersed stage"""
        self.ZDI = 0

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