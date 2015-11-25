from negotiator_base import BaseNegotiator
from random import random, randint


class StandardNegotiator(BaseNegotiator):

    def __init__(self):
        self.moveFirst = False
        self.firstOffer = False
        self.currIter = 0
        self.otherNegoWants = {}
        self.visited = []

        BaseNegotiator.__init__(self)

    def get_offer_util(self,offer):
        if offer is None:
            return 0
        totalutil = 0
        for item, util in self.preferences.iteritems():
            if item in offer:
                totalutil = totalutil + util
        return totalutil


    def generate_offers(self):
        offers = []
        offer_size = min(self.iter_limit, len(self.preferences)/2)
        if len(self.preferences) % 2 == 1:
            if not self.moveFirst:
                offer_size += len(self.preferences)/2 + 1
                
            else:
                offer_size += len(self.preferences)/2
        else:
            offer_size += len(self.preferences)/2 
        print "AFDS " + str(offer_size) 
        for x in xrange(0, self.iter_limit):
            curr_offer = []
            for y in xrange(0, offer_size):
                curr_offer += [self.get_highest_item(curr_offer)]
            if self.get_offer_util(curr_offer) < (.4 * self.total_util):
                break
            offers += [curr_offer]
            offer_size-=1
        return offers
    
    def get_highest_item(self, ignore):
        highest_util = 0
        highest_item = None
        for item, util in self.preferences.iteritems():
            if util > highest_util and ignore is not None and item not in ignore:
                highest_util = util
                highest_item = item
        return highest_item

    def get_lowest_item(self, ignore):
        lowest_util = 10000
        lowest_item = None
        for item, util in self.preferences.iteritems():
            if util < lowest_util:
                if ignore is not None and item in ignore:
                    continue
                else:
                    lowest_util = util
                    lowest_item = item
        return lowest_item

    def get_total_util(self):
        self.total_util = 0
        for item, util in self.preferences.iteritems():
            self.total_util+=util


    def make_offer(self, offer):
        modifiedOffers = []
        # init dictionary
        if len(self.otherNegoWants) == 0:
            for item in self.preferences:
                self.otherNegoWants[item] = 0

        # init total util
        if "total_util" not in locals():
            self.get_total_util()

        # init moveFirst
        if offer is None:
            self.moveFirst = True
        # update dictionary
        else:
            for item in offer:
                self.otherNegoWants[item] = self.otherNegoWants[item] + 1


        self.currIter+=1
        self.offer = offer
        #print "Current Iter: " + str(self.currIter)
        #print "Offers: " + str(offers)
        #print "Modified Offer: " + str(modifiedOffers)
        #print "offer given:" + str(offer)



        # evaluate offer
        print "Expected val: " + str(.5 * self.total_util)
        if self.offer is not None:
            print "Offered val: " + str(self.get_offer_util(BaseNegotiator.set_diff(self)))
        if self.moveFirst and self.offer is not None and self.get_offer_util(BaseNegotiator.set_diff(self)) > (.5 * self.total_util):
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer
            
        elif self.offer is not None and self.get_offer_util(BaseNegotiator.set_diff(self)) >= (.4 * self.total_util):
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer

        # make offer
        offers = self.generate_offers()
        print "test"
        print "All offers: " + str(offers)
        # will try best offer first, rest will be random
        choice = 0
        while choice in self.visited: 
            choice = randint(0, len(offers)-1)
        self.visited += [choice]
        # if we've visited all, empty
        if len(self.visited) == len(offers):
            self.visited = []
        self.offer = offers[choice]

        print "Current Iter: " + str(self.currIter)
        print "Current Offer: " + str(self.offer)
      

        return self.offer


