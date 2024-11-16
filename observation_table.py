from white_box_oracle import WhiteBoxOracle
from automata.fa.dfa import DFA

class ObservationTable:
  def __init__(self, input_symbols):
    self.input_symbols = input_symbols
    self.S = {''} # Set
    self.E = {''} # Set
    self.R = input_symbols.copy() # S.I
    self.f = {} # Dict

  def fill(self, oracle:WhiteBoxOracle):
    for s in self.S:
      for e in self.E:
        if (s, e) not in self.f:
          self.f[(s, e)] = oracle.membership_query(s + e)
    for r in self.R:
      for e in self.E:
        if (r, e) not in self.f:
          self.f[(r, e)] = oracle.membership_query(r + e)

  def row(self, s):
    return {e: self.f[(s, e)] for e in self.E}

  def make_close(self):
    candidate_r = None
    for r in self.R:
      flag = False
      for s in self.S:
        if self.row(r) == self.row(s):
          flag = True
          break
      if not flag:
        candidate_r = r
        break
    if candidate_r == None:
      return False
    else:
      self.S.add(candidate_r)
      self.R.discard(candidate_r)
      add_to_r = set()
      for c in self.input_symbols:
        print('c:' + c)
        if candidate_r + c not in self.R or candidate_r + c not in self.S:
          add_to_r.add(candidate_r + c)
      self.R.update(add_to_r)
      return True

  def make_consistent(self):
    for s1 in self.S:
      for s2 in self.S:
        if self.row(s1) == self.row(s2):
          print('s1:' + s1 + ' s2:' + s2)
          for a in self.input_symbols:
            s1a = s1 + a
            s2a = s2 + a
            if self.row(s1a) != self.row(s2a):
              print('s1a:' + s1a + ' s2a:' + s2a)
              for e in self.E:
                if self.row(s1a)[e] != self.row(s2a)[e]:
                  self.E.add(a + e)
                  return True
    return False

  def counterexample_processing(self, counterexample):
    for i in range(1,len(counterexample)+1):
      prefix = counterexample[:i]
      if prefix not in self.S:
        if prefix not in self.R:
          self.S.add(prefix)
        else:
          self.S.add(prefix)
          self.R.discard(prefix)
        for c in self.input_symbols:
          if prefix + c not in self.R or prefix + c not in self.S:
            self.R.add(prefix + c)

  def build_DFA(self):
    initial_state = '[\u03B5]'
    states = {initial_state}
    final_states = set()
    row_states = {frozenset(self.row('').items()): initial_state}
    for s in self.S:
      row_s = frozenset(self.row(s).items())
      if row_s not in row_states:
        row_states[row_s] = '[' + s + ']'
    for key in row_states:
      if key != frozenset(self.row('').items()):
        states.add(row_states[key])
    transitions = {}
    for s in self.S:
      transitions[row_states[frozenset(self.row(s).items())]] = {}
      for c in self.input_symbols:
        next_state = row_states[frozenset(self.row(s + c).items())]
        transitions[row_states[frozenset(self.row(s).items())]][c] = next_state
    for s in self.S:
      if self.row(s)[''] == True:
        final_states.add(row_states[frozenset(self.row(s).items())])

    return DFA(
      states=states,
      input_symbols=self.input_symbols,
      transitions=transitions,
      initial_state=initial_state,
      final_states=final_states
    )

  def to_string(self):
    ret = 'E:'
    for e in self.E:
      if e == '':
        ret += ' \u03B5'
      else:
        ret += ' ' + e
    ret += '\nS:\n'
    for s in self.S:
      if s == '':
        ret += '\u03B5:'
      else:
        ret += ' ' + s + ':'
      for e in self.E:
        ret += ' ' + str(self.f[(s, e)])
      ret += '\n'
    ret += 'R:'
    for r in self.R:
      ret += '\n' + r + ':'
      for e in self.E:
        ret += ' ' + str(self.f[(r, e)])
    return ret
