class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    def __init__(self, num_users, num_rounds):
        '''Initialize the number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.current_round = 0
        self.budget = 0  

    def __repr__(self):
        '''Return a representation of the Bidder object'''
        return f"Bidder(num_users={self.num_users}, num_rounds={self.num_rounds}, current_round={self.current_round})"

    def __str__(self):
        '''Return a string representation of the Bidder object'''
        return f"Bidder with {self.num_users} users, {self.num_rounds} rounds, currently in round {self.current_round}"

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        # Example bid logic: Bid a fraction of the remaining budget
        bid_amount = self.budget / (self.num_rounds - self.current_round + 1)
        return max(0, bid_amount)  # Ensure non-negative bid amount

    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        self.current_round += 1
        if auction_winner:
            self.budget -= price  # Deduct the price from the budget if the bidder won
            # Example logic: Update strategy based on click
            if clicked:
                # Increase bid slightly if the ad was clicked
                self.budget += 10  # Example reward for click, can be adjusted as needed
            else:
                # Decrease bid slightly if the ad was not clicked
                self.budget -= 5  # Example penalty for no click, can be adjusted as needed
