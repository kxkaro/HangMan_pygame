

class Score:
    
    def __init__(self, max_trials):
        self.max_trials = max_trials
        self.current_score = max_trials
        self.total_score = 0


    def decrease_current(self, n = 1):
        self.current_score -= n


    def update(self):
        self.total_score += self.current_score
        self.current_score = self.max_trials


    def reset(self):
        self.current_score = self.max_trials
        self.total_score = 0