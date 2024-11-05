from white_box_oracle import WhiteBoxOracle
class ObservationTable:
  def __init__(self, input_symbols):
    self.input_symbols = input_symbols
    self.S = {''}
    self.E = {''}
    self.R = input_symbols # S.I
    self.SUR = set()
    for s in self.S:
      for r in self.R:
          self.SUR.add(s + r)
    self.f = {}

  def fill(self, oracle):
    for s in self.SUR:
      for e in self.E:
        if (s, e) not in self.f:
          self.f[(s, e)] = oracle.membership_query(s + e)

  def row(self, s):
    return {e: self.f[(s, e)] for e in self.E}

  def make_close(self):
    row_in_S = set()
    for s in self.S:
      row_in_S.add(self.row(s))
    candidate_r = None
    for r in self.R:
      if not (self.row(r) not in row_in_S):
        candidate_r = r
        break
    if candidate_r == None:
      return False
    else:
      self.S.add(candidate_r)
      self.R.remove(candidate_r)
      return True

  def make_consistent(self):
    for i in range(len(self.S)):
      for j in range(i, len(self.S)):
        s1 = self.S[i]
        s2 = self.S[j]
        if self.row(s1) == self.row(s2):
          for a in self.input_symbols:
            s1a = s1 + a
            s2a = s2 + a
            if self.row(s1a) != self.row(s2a):
              for e in self.E:
                if self.row(s1a)[e] != self.row(s2a)[e]:
                  self.E.add(a + e)
                  return True
    return False

  def build_DFA(self):
    pass
