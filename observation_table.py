from abstract_oracle import AbstractOracle
from automata.fa.dfa import DFA

class ObservationTable:
  def __init__(self, input_symbols):
    self.input_symbols = input_symbols
    self.S = {''} # Set of prefixes
    self.E = {''} # Set of suffixes
    self.R = set() # S·Σ - S (boundary)
    self.f = {} # Dict for membership query results

    # Initialize R with all one-symbol extensions of S
    for s in self.S:
      for a in self.input_symbols:
        self.R.add(s + a)

  def fill(self, oracle: AbstractOracle):
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
    """
    Make the observation table closed.
    A table is closed if for each r ∈ R, there exists s ∈ S such that row(r) = row(s).

    Returns:
        True if the table was modified, False otherwise
    """
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

    if candidate_r is None:
      return False
    else:
      # Move candidate_r from R to S
      self.S.add(candidate_r)
      self.R.discard(candidate_r)

      # Add all one-symbol extensions of candidate_r to R
      for c in self.input_symbols:
        new_string = candidate_r + c
        if new_string not in self.S and new_string not in self.R:
          self.R.add(new_string)

      return True

  def make_consistent(self):
    """
    Make the observation table consistent.
    A table is consistent if for all s1, s2 ∈ S where row(s1) = row(s2),
    for all a ∈ Σ, row(s1·a) = row(s2·a).

    Returns:
        True if the table was modified, False otherwise
    """
    for s1 in self.S:
      for s2 in self.S:
        if self.row(s1) == self.row(s2):
          for a in self.input_symbols:
            s1a = s1 + a
            s2a = s2 + a

            # Check if rows are different
            if s1a in self.S or s1a in self.R:
              if s2a in self.S or s2a in self.R:
                if self.row(s1a) != self.row(s2a):
                  # Find a distinguishing suffix
                  for e in self.E:
                    if self.f.get((s1a, e), None) != self.f.get((s2a, e), None):
                      # Add a·e to E
                      self.E.add(a + e)
                      return True
    return False

  def counterexample_processing(self, counterexample):
    """
    Process a counterexample by adding all its prefixes to S.

    Args:
        counterexample: A string that is a counterexample to the current hypothesis
    """
    # Add all prefixes of the counterexample to S
    for i in range(len(counterexample) + 1):
      prefix = counterexample[:i]

      # If prefix is already in S, skip
      if prefix in self.S:
        continue

      # If prefix is in R, move it to S
      if prefix in self.R:
        self.R.discard(prefix)

      # Add prefix to S
      self.S.add(prefix)

      # Add all one-symbol extensions of prefix to R if they're not in S
      for c in self.input_symbols:
        new_string = prefix + c
        if new_string not in self.S and new_string not in self.R:
          self.R.add(new_string)

  def build_DFA(self):
    """
    Build a DFA from the observation table.

    Returns:
        A DFA that is consistent with the observation table
    """
    # Create states based on unique rows
    initial_state = '[\u03B5]'  # Epsilon state
    states = {initial_state}
    final_states = set()

    # Map from row contents to state names
    row_states = {}

    # First, add the initial state
    row_states[frozenset(self.row('').items())] = initial_state

    # Then add states for all other unique rows in S
    for s in self.S:
      row_s = frozenset(self.row(s).items())
      if row_s not in row_states:
        row_states[row_s] = '[' + s + ']'
        states.add(row_states[row_s])

    # Create transitions
    transitions = {}
    for s in self.S:
      state = row_states[frozenset(self.row(s).items())]
      transitions[state] = {}

      for c in self.input_symbols:
        s_c = s + c
        # Find the state corresponding to row(s·c)
        # If s·c is not in S, we need to find an s' in S such that row(s') = row(s·c)
        if s_c in self.S:
          next_state = row_states[frozenset(self.row(s_c).items())]
        else:
          # Find an s' in S such that row(s') = row(s·c)
          found = False
          for s_prime in self.S:
            if self.row(s_prime) == self.row(s_c):
              next_state = row_states[frozenset(self.row(s_prime).items())]
              found = True
              break

          if not found:
            # This should not happen if the table is closed
            raise ValueError(f"Table is not closed: no state found for {s_c}")

        transitions[state][c] = next_state

    # Determine final states
    for s in self.S:
      if self.row(s)[''] == True:  # Empty string is accepted from this state
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
