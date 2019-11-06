# /usr/bin/python

import torch
import sys
import numpy as np

class ReRanker:
    def __init__(self):
        self.rerun = False
        self.pred_change = {}
        print "ReRanker initializing"
        try:
            device = torch.device('cuda')
            D_in, H, D_out =  3, 3, 1
            self.entitymodel = torch.nn.Sequential(
               torch.nn.Linear(D_in, H),
               torch.nn.ReLU(),
               torch.nn.Linear(H, H),
               torch.nn.ReLU(),
               torch.nn.Linear(H, D_out)
             ).to(device)
            self.entitymodel.load_state_dict(torch.load('../data/wikirerankerentity1094.model'))
            self.entitymodel.eval()
            D_in, H, D_out =  3, 3, 1
            self.relationmodel = torch.nn.Sequential(
               torch.nn.Linear(D_in, H),
               torch.nn.ReLU(),
               torch.nn.Linear(H, H),
               torch.nn.ReLU(),
               torch.nn.Linear(H, D_out)
             ).to(device)
            self.relationmodel.load_state_dict(torch.load('../data/wikirerankerrelation1092.model'))
            self.relationmodel.eval()
        except Exception,e:
            print e
            sys.exit(1)
        print "ReRanker initialized"


    def reRank(self, topklists):
        rerankedlists = {}
        for k1, v1 in topklists['nodefeatures'].iteritems():
            if k1 == 'chunktext' or k1 == 'ertypes':
                continue
            uris = []
            lvnstn = []
            featurevectors = []
            for k2, v2 in v1.iteritems():
                uris.append((k2,v2))
                featurevectors.append([v2['connections'],v2['esrank'],v2['sumofhops']])
            if len(featurevectors) == 0:
                rerankedlists[k1] = []
            else:
                featurevectors = torch.FloatTensor(featurevectors).cuda()
                predictions = None
                if 'wikidata.dbpedia.org' in uris[0][0]:
                    predictions = self.entitymodel(featurevectors).reshape(-1).cpu().detach().numpy()
                else:
                    predictions =  self.relationmodel(featurevectors).reshape(-1).cpu().detach().numpy()
                max_pred = (np.max(predictions))
                self.pred_change[k1]= 'correct'
                l = [(float(p),u) for p,u in zip(predictions, uris)]
                rerankedlists[k1] = sorted(l, key=lambda x: x[0], reverse=True)
        changes = self.pred_change.values()
        if 'change' in changes:
                self.rerun = True
        return {'rerankedlists': rerankedlists, 'chunktext':topklists['chunktext'], 'ertypes': topklists['ertypes'], 'er-rerun': self.rerun, 'changes': self.pred_change}
                
if __name__ == '__main__':
    r = ReRanker()

    print r.reRank({'chunktext': [{'chunk': 'Who', 'surfacelength': 3, 'class': 'entity', 'surfacestart': 0}, {'chunk': 'the parent organisation', 'surfacelength': 23, 'class': 'relation', 'surfacestart': 7}, {'chunk': 'Barack Obama', 'surfacelength': 12, 'class': 'entity', 'surfacestart': 34}, {'chunk': 'is', 'surfacelength': 2, 'class': 'relation', 'surfacestart': 4}], 'nodefeatures': {0: {u'http://dbpedia.org/resource/Yara-ma-yha-who': {'connections': 0.0, 'esrank': 12, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/WHO-DT': {'connections': 0.5, 'esrank': 3, 'sumofhops': 0.75}, u'http://dbpedia.org/resource/Who_Made_Who': {'connections': 0.25, 'esrank': 20, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Vinnie_Who': {'connections': 0.25, 'esrank': 28, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Who': {'connections': 0.0, 'esrank': 1, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who_Knows_Who': {'connections': 0.25, 'esrank': 21, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Girls_Who_Like_Boys_Who_Like_Boys': {'connections': 0.0, 'esrank': 22, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who_Made_Who_(song)': {'connections': 0.25, 'esrank': 18, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Girls_Who_Like_Boys_Who_Like_Boys_(book)': {'connections': 0.5, 'esrank': 24, 'sumofhops': 0.75}, u'http://dbpedia.org/resource/Who_Is_Dr_Who': {'connections': 0.25, 'esrank': 16, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Chi_(Who)': {'connections': 0.0, 'esrank': 8, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who_Made_Who_World_Tour': {'connections': 0.0, 'esrank': 14, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who%3F_(novel)': {'connections': 0.5, 'esrank': 4, 'sumofhops': 0.75}, u'http://dbpedia.org/resource/Vem_\xe4r_det': {'connections': 0.0, 'esrank': 23, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Doctor_Who': {'connections': 0.5, 'esrank': 26, 'sumofhops': 0.75}, u'http://dbpedia.org/resource/Who_Cares': {'connections': 0.0, 'esrank': 29, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who%3F_(album)': {'connections': 0.25, 'esrank': 11, 'sumofhops': 0.375}, u"http://dbpedia.org/resource/Who_I_Am_Hates_Who_I've_Been": {'connections': 0.25, 'esrank': 15, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Who_Shall_Live_and_Who_Shall_Die': {'connections': 0.0, 'esrank': 19, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who,_What,_Wear': {'connections': 0.0, 'esrank': 6, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who_Dunnit': {'connections': 0.25, 'esrank': 30, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Who_Killed_Who%3F': {'connections': 0.25, 'esrank': 17, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/The_Who': {'connections': 0.5, 'esrank': 31, 'sumofhops': 0.875}, u'http://dbpedia.org/resource/Who_Booty': {'connections': 0.25, 'esrank': 25, 'sumofhops': 0.375}, u'http://dbpedia.org/resource/Ledipasvir': {'connections': 0.0, 'esrank': 27, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who%3F_Who%3F_Ministry': {'connections': 0.0, 'esrank': 2, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who_Covers_Who%3F': {'connections': 0.0, 'esrank': 13, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who,_whom%3F': {'connections': 0.0, 'esrank': 10, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who,_Me': {'connections': 0.0, 'esrank': 5, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/WHO/PES': {'connections': 0.0, 'esrank': 7, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Who%3F_(song)': {'connections': 0.0, 'esrank': 9, 'sumofhops': 0.0}}, 1: {u'http://dbpedia.org/property/organizations': {'connections': 0.0, 'esrank': 16, 'sumofhops': 0.0}, u'http://dbpedia.org/ontology/parent': {'connections': 1.25, 'esrank': 5, 'sumofhops': 1.625}, u'http://dbpedia.org/ontology/organisation': {'connections': 0.0, 'esrank': 6, 'sumofhops': 0.0}, u'http://dbpedia.org/property/organiztion': {'connections': 0.0, 'esrank': 17, 'sumofhops': 0.0}, u'http://www.telegraph.co.uk/finance/property/renting/11908002/Generation-rent-the-reluctant-rise-of-the-older-tenant.html': {'connections': 0.0, 'esrank': 18, 'sumofhops': 0.0}, u'http://dbpedia.org/property/organisations': {'connections': 0.0, 'esrank': 13, 'sumofhops': 0.0}, u'http://dbpedia.org/property/organization': {'connections': 0.25, 'esrank': 14, 'sumofhops': 0.375}, u'http://dbpedia.org/property/parnet': {'connections': 0.0, 'esrank': 26, 'sumofhops': 0.0}, u'http://dbpedia.org/property/parent': {'connections': 3.25, 'esrank': 12, 'sumofhops': 4.875}, u'http://dbpedia.org/property/organisation': {'connections': 0.0, 'esrank': 8, 'sumofhops': 0.0}, u'http://dbpedia.org/ontology/parentOrganisation': {'connections': 0.5, 'esrank': 1, 'sumofhops': 0.75}, u'http://dbpedia.org/property/parantOrganization': {'connections': 0.0, 'esrank': 9, 'sumofhops': 0.0}, u'http://dbpedia.org/property/urbanisation': {'connections': 0.0, 'esrank': 15, 'sumofhops': 0.0}, u'http://dbpedia.org/property/theN': {'connections': 0.0, 'esrank': 19, 'sumofhops': 0.0}, u'http://dbpedia.org/property/perent': {'connections': 0.0, 'esrank': 25, 'sumofhops': 0.0}, u'http://dbpedia.org/property/parentCo.': {'connections': 0.0, 'esrank': 11, 'sumofhops': 0.0}, u'http://dbpedia.org/property/theE': {'connections': 0.0, 'esrank': 20, 'sumofhops': 0.0}, u'http://dbpedia.org/property/theA': {'connections': 0.0, 'esrank': 21, 'sumofhops': 0.0}, u'http://dbpedia.org/property/prarent': {'connections': 0.0, 'esrank': 23, 'sumofhops': 0.0}, u'http://dbpedia.org/property/theW': {'connections': 0.0, 'esrank': 22, 'sumofhops': 0.0}, u'http://dbpedia.org/ontology/Organisation': {'connections': 1.0, 'esrank': 7, 'sumofhops': 1.5}, u'http://dbpedia.org/property/parentOrganisation': {'connections': 0.0, 'esrank': 2, 'sumofhops': 0.0}, u'http://dbpedia.org/property/parentOrganization': {'connections': 0.0, 'esrank': 3, 'sumofhops': 0.0}, u'http://dbpedia.org/property/parents': {'connections': 1.0, 'esrank': 24, 'sumofhops': 1.5}, u'http://dbpedia.org/property/agent': {'connections': 0.0, 'esrank': 10, 'sumofhops': 0.0}, u'http://dbpedia.org/property/parentOraganisation': {'connections': 0.0, 'esrank': 4, 'sumofhops': 0.0}}, 2: {u'http://dbpedia.org/resource/Barack_Obama_Selma_50th_anniversary_speech': {'connections': 0.0, 'esrank': 13, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Economic_policy_of_Barack_Obama': {'connections': 0.0, 'esrank': 8, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_Green_Charter_High_School': {'connections': 0.0, 'esrank': 31, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Assassination_threats_against_Barack_Obama': {'connections': 0.0, 'esrank': 4, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/United_States_Senate_career_of_Barack_Obama': {'connections': 0.0, 'esrank': 21, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Efforts_to_impeach_Barack_Obama': {'connections': 0.0, 'esrank': 12, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Invitations_to_the_first_inauguration_of_Barack_Obama': {'connections': 0.0, 'esrank': 9, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_Tucson_memorial_speech': {'connections': 0.0, 'esrank': 17, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama,_Sr.': {'connections': 0.25, 'esrank': 22, 'sumofhops': 0.125}, u'http://dbpedia.org/resource/Barack_Obama_%22Hope%22_poster': {'connections': 0.0, 'esrank': 26, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_presidential_campaign,_2008': {'connections': 0.0, 'esrank': 20, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/List_of_topics_related_to_Barack_Obama': {'connections': 0.0, 'esrank': 2, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_%22Joker%22_poster': {'connections': 0.0, 'esrank': 3, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Foreign_policy_of_the_Barack_Obama': {'connections': 0.0, 'esrank': 14, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Illinois_Senate_career_of_Barack_Obama': {'connections': 0.0, 'esrank': 15, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_in_comics': {'connections': 0.0, 'esrank': 24, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama': {'connections': 1.5, 'esrank': 1, 'sumofhops': 2.375}, u'http://dbpedia.org/resource/List_of_things_named_after_Barack_Obama': {'connections': 0.0, 'esrank': 18, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Native_American_Policy_of_the_Barack_Obama_Administration': {'connections': 0.0, 'esrank': 29, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_Democratic_Club_of_Upper_Manhattan': {'connections': 0.0, 'esrank': 28, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Public_image_of_Barack_Obama': {'connections': 0.0, 'esrank': 7, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_on_social_media': {'connections': 0.0, 'esrank': 23, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Second_inauguration_of_Barack_Obama': {'connections': 0.0, 'esrank': 16, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_presidential_campaign_endorsements': {'connections': 0.0, 'esrank': 25, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_Male_Leadership_Academy': {'connections': 0.0, 'esrank': 27, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Space_policy_of_the_Barack_Obama_administration': {'connections': 0.0, 'esrank': 11, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Presidential_transition_of_Barack_Obama': {'connections': 0.5, 'esrank': 6, 'sumofhops': 0.5}, u'http://dbpedia.org/resource/First_inauguration_of_Barack_Obama': {'connections': 0.0, 'esrank': 19, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Timeline_of_the_presidency_of_Barack_Obama': {'connections': 0.0, 'esrank': 30, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/Barack_Obama_College_Preparatory_High_School': {'connections': 0.0, 'esrank': 10, 'sumofhops': 0.0}, u'http://dbpedia.org/resource/List_of_books_and_films_about_Barack_Obama': {'connections': 0.0, 'esrank': 5, 'sumofhops': 0.0}}, 3: {u'http://www.smh.com.au/business/property/old-is-new-at-refashioned-amp-square-20110522-1eytn.html': {'connections': 0.0, 'esrank': 24, 'sumofhops': 0.0}, u'http://www.news.com.au/money/property/mining-boom-is-strangling-heart-of-gunnedah/story-e6frfmd0-1226298825863': {'connections': 0.0, 'esrank': 28, 'sumofhops': 0.0}, u'http://dbpedia.org/property/causeIs': {'connections': 0.0, 'esrank': 11, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isSiSpecs': {'connections': 0.0, 'esrank': 30, 'sumofhops': 0.0}, u'http://dbpedia.org/property/theGovernorIs412YearsOfAgeAndHerNameIsEthelWinkleberryTimezone': {'connections': 0.0, 'esrank': 29, 'sumofhops': 0.0}, u'http://www.timeslive.co.za/sundaytimes/decor/property/2015/11/13/Real-estate-crowdfunding-is-unchartered-territory-in-SA': {'connections': 0.0, 'esrank': 27, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isBladed': {'connections': 0.0, 'esrank': 7, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isOn': {'connections': 0.0, 'esrank': 10, 'sumofhops': 0.0}, u'http://www.independent.co.uk/property/house-and-home/is-elmbridge-britains-beverly-hills-2190344.html': {'connections': 0.0, 'esrank': 22, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isMulti': {'connections': 0.0, 'esrank': 12, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isRanged': {'connections': 0.0, 'esrank': 6, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isRangedl': {'connections': 0.0, 'esrank': 15, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isTube': {'connections': 0.0, 'esrank': 21, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isUk': {'connections': 0.0, 'esrank': 5, 'sumofhops': 0.0}, u'http://www.telegraph.co.uk/property/overseasproperty/3360841/Caribbean-property-Rio-Ferdinand-is-ahead-of-the-game.html': {'connections': 0.0, 'esrank': 25, 'sumofhops': 0.0}, u'http://dbpedia.org/property/10,000IsADiceGameThatIsPlayedWithFiveDiceA': {'connections': 0.0, 'esrank': 2, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isThermal': {'connections': 0.0, 'esrank': 18, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isVehicle': {'connections': 0.0, 'esrank': 13, 'sumofhops': 0.0}, u'http://dbpedia.org/property/is': {'connections': 0.0, 'esrank': 1, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isMissile': {'connections': 0.0, 'esrank': 8, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isShip': {'connections': 0.0, 'esrank': 19, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isSeries': {'connections': 0.0, 'esrank': 4, 'sumofhops': 0.0}, u'http://dbpedia.org/property/remains': {'connections': 0.0, 'esrank': 31, 'sumofhops': 0.0}, u'http://www.telegraph.co.uk/property/9285761/Hovis-Hill-is-this-the-greatest-street-since-sliced-bread.html': {'connections': 0.0, 'esrank': 26, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isArtillery': {'connections': 0.0, 'esrank': 3, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isStack': {'connections': 0.0, 'esrank': 14, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isExplosive': {'connections': 0.0, 'esrank': 20, 'sumofhops': 0.0}, u'http://www.telegraph.co.uk/finance/property/3293690/When-an-Englishmans-home-is-his-business.html': {'connections': 0.0, 'esrank': 23, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isBomb': {'connections': 0.0, 'esrank': 9, 'sumofhops': 0.0}, u'http://dbpedia.org/property/isSeason': {'connections': 0.0, 'esrank': 16, 'sumofhops': 0.0}, u'http://dbpedia.org/property/featIs': {'connections': 0.0, 'esrank': 17, 'sumofhops': 0.0}}}, 'ertypes': ['entity', 'relation', 'entity', 'relation']})
