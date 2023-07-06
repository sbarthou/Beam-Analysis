def reactions(self):
    for support_list in self.supports:
        support = support_list[0]
        if self.load_pos > self.L/2:
            support.yreaction = self.P * (self.load_pos/self.L)