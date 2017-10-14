from constants import PAD, ROOT


## Copyright 2010 Yoav Goldberg
##
## This file is part of easyfirst
##
##    easyfirst is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    easyfirst is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with easyfirst.  If not, see <http://www.gnu.org/licenses/>.


class BaselineFeatureExtractor:  # {{{
    LANG = 'ENG'

    def __init__(self):
        self.versions = None
        self.vocab = set()

    def extract(self, parsed, deps, i):
        """
        i=T4:
           should I connect T4 and T5 in:
              t1 t2 t3 T4 T5 t6 t7 t8
           ?
           focus: f1=T4 f2=T5
           previous: p1=t3 p2=t2
           next:     n1=t6 n2=t7
        returns (feats1,feats2)
        where feats1 is a list of features for connecting T4->T5  (T4 is child)
        and   feats2 is a list of features for connecting T4<-T5  (T5 is child)
        """
        # LANG = self.LANG
        CC = ['CC', 'CONJ']
        IN = ['IN']

        j = i + 1
        features = []

        f1 = parsed[i]
        f2 = parsed[j]
        n1 = parsed[j + 1] if j + 1 < len(parsed) else PAD
        p1 = parsed[i - 1] if i - 1 >= 0 else PAD


        f1_form = f1['form']
        f2_form = f2['form']
        p1_form = p1['form']
        n1_form = n1['form']


        f1_tag = f1['tag']
        f2_tag = f2['tag']
        p1_tag = p1['tag']
        n1_tag = n1['tag']
        
        if f1_tag in IN: f1_tag = "%s%s" % (f1_tag, f1_form)
        if f2_tag in IN: f2_tag = "%s%s" % (f2_tag, f2_form)
        if p1_tag in IN: p1_tag = "%s%s" % (p1_tag, p1_form)
        if n1_tag in IN: n1_tag = "%s%s" % (n1_tag, n1_form)



        left_child = deps.left_child
        f1lc = left_child(f1)
        if f1lc: f1lc = f1lc['tag']
        f2lc = left_child(f2)
        if f2lc: f2lc = f2lc['tag']
        n1lc = left_child(n1)
        if n1lc: n1lc = n1lc['tag']
        p1lc = left_child(p1)
        if p1lc: p1lc = p1lc['tag']


        ## TO-VERB (to keep, to go,...)
        if f1_tag[0] == 'V' and f1lc == 'TO': f1_tag = "%s_TO" % f1_tag
        if f2_tag[0] == 'V' and f2lc == 'TO': f2_tag = "%s_TO" % f2_tag
        if p1_tag[0] == 'V' and p1lc == 'TO': p1_tag = "%s_TO" % p1_tag
        if n1_tag[0] == 'V' and n1lc == 'TO': n1_tag = "%s_TO" % n1_tag

        f1rc_form = None
        right_child = deps.right_child
        f1rc = right_child(f1)
        if f1rc:
            f1rc_form = f1rc['form']
            f1rc = f1rc['tag']

        f2rc_form = None
        f2rc = right_child(f2)
        if f2rc:
            f2rc_form = f2rc['form']
            f2rc = f2rc['tag']

        n1rc_form = None
        n1rc = right_child(n1)
        if n1rc:
            n1rc_form = n1rc['form']
            n1rc = n1rc['tag']

        p1rc = right_child(p1)
        if p1rc: p1rc = p1rc['tag']


        # this should help in cases of A CC B D, telling B not to B->D if CC is not built yet and in matching type
        # hope this helps (Many money managers and (some traders had already left))
        if f1_tag in CC: f1_tag = "%s-%s-%s-%s" % (f1_form, f1_tag, f1lc, f1rc)
        if f2_tag in CC: f2_tag = "%s-%s-%s-%s" % (f2_form, f2_tag, f2lc, f2rc)
        if p1_tag in CC: p1_tag = "%s-%s-%s-%s" % (p1_form, p1_tag, p1lc, p1rc)
        if n1_tag in CC: n1_tag = "%s-%s-%s-%s" % (n1_form, n1_tag, n1lc, n1rc)

        append = features.append


        # unigram
        if f1_form: append("f1w_%s" % (f1_form))
        if f2_form: append("f2w_%s" % (f2_form))
        if p1_form: append("p1w_%s" % (p1_form))
        if n1_form: append("n1w_%s" % (n1_form))

        append("f1t_%s" % (f1_tag))
        append("f2t_%s" % (f2_tag))
        append("p1t_%s" % (p1_tag))
        append("n1t_%s" % (n1_tag))


        # bigram
        append("f1tf2t_%s_%s" % (f1_tag, f2_tag))

        append("p1tf1t_%s_%s" % (p1_tag, f1_tag))

        append("f2tn1t_%s_%s" % (f2_tag, n1_tag))



        return features

    # }}}


FeaturesExtractorTest = BaselineFeatureExtractor
