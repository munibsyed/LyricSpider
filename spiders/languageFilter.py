import string

'''A class which provides utility functions for explicit language filtering'''

class LanguageFilter:
   
    def __init__(self):
         #words that are basically always dirty
        self.main_dirty = ["fuck","shit","fag","faggot","titty", "titties","nigger","pussy","dick","blowjob","blow job","ballsack","nutsack","nigga","bitch","beeotch","cunt", "bastard","slut","whore","bimbo","bollock","boner", "cunny", "dildo", "douche", "dyke","kike"]
        self.additional_dirty = []
        #words that may exist as substrings of other words, so they are not always dirty
        self.sometimes_dirty = ['tit','ass',"arse","cock","cum", "wank"]
        
    def is_dirty(self, someStr):
        someStr = someStr.lower()
        #remove punctuation
        #Is this ideal? Run time trials for different punctuation stripping methods 
        someStr = ''.join([c for c in someStr if c not in string.punctuation])
        dirty_found = []
        for dirty in self.main_dirty:
            if dirty in someStr:
                dirty_found.append(dirty)

        for dirty in self.sometimes_dirty:
            whole_word = " " + dirty + " "
            
            if whole_word in someStr:
                dirty_found.append(dirty)

        
        return ", ".join(dirty_found)
