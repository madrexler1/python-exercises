class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''

    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.probability = np.random.uniform(0, 1) # generate the probability that the user clicks bbased on a U[0,1]

    def __repr__(self):
        '''User object with secret probability'''
        return f"User(probability={self.probability:.2f})"

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return f"User with a secret click probability of {self.probability:.2f}"

    def show_ad(self):
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        return np.random.rand() < self.probability # randomly determines true if the random prob is less than the user prob

class Auction:
    '''Class to represent an online second-price ad auction'''
    
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store balances for each bidder in the auction'''
        self.users = users
        self.bidders = bidders
        self.balances = {bidder: 0 for bidder in bidders} # need a dictionary here

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return f"Auction(users={len(self.users)}, bidders={len(self.bidders)})"

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return f"Auction with {len(self.users)} users and {len(self.bidders)} bidders"

    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''

        user = np.random.choice(self.users) # select a user
        
        bids = {bidder: bidder.bid(id(user)) for bidder in self.bidders} # populate dictionary with bids from each bidder
        
        sorted_bidders = sorted(bids, key=bids.get, reverse=True) # sort the bids so can determin "second-highest"
        
        winner = sorted_bidders[0] # winner is the highest bid

        if len(sorted_bidders) > 1:
            second_highest_bid = bids[sorted_bidders[1]] # get the second highest bid
        else:
            second_highest_bid = 0
        
        clicked = user.show_ad() # define the process of showing the ad to users
        
        winner.notify(auction_winner=True, price=second_highest_bid, clicked=clicked) # "notify" winner
        self.balances[winner] -= second_highest_bid # subtract the winning bid about from the winner's balance
        
        for loser in sorted_bidders[1:]:
            loser.notify(auction_winner=False, price=second_highest_bid, clicked=clicked) # "notifying" losers

        if self.balances[winner] < -1000:
            self.bidders.remove(winner)
            print(f"Bidder removed from the auction due to low balance: {winner}")
        
        return {
            "winner": winner,
            "winning_bid": bids[winner],
            "price_paid": second_highest_bid,
            "clicked": clicked,
            "user": user
        }