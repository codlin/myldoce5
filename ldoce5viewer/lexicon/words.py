
class WordInfo:
    Name = ""
    Phonetic = ""
    PhoneticAudio = ""
    Hyphenation = ""
    Paraphrases = []
    Sentences = []
    def ParaphrasesToString(self):
        pad = int(4-len(self.Paraphrases))
        while pad > 0:
            self.Paraphrases.append((" ", " "))
            pad -= 1

        araphrases = ""
        for item in self.Paraphrases:
            #cixing
            speech = item[0]
            #shiyi
            definitions = item[1]
            definitions = definitions.strip().replace(" ", "")
            araphrase = speech + "\t" +definitions + "\t"
            araphrases +=  araphrase
        return araphrases

    def SentencesToString(self):
        sentences = ""
        for item in self.Sentences:
            #item[0]sample, item[1]audio, item[2]translate
            str = "%s\t[sound:%s]\t%s\t" %(item[0], item[1], item[2])
            #print(str)
            sentences += str
        return sentences

    def toString(self):
        str = "%s\t/%s/\t[sound:%s]\t<img src=\"%s.jpg\" />\t%s%s\n" %(self.Hyphenation.strip(), self.Phonetic.strip(), self.PhoneticAudio.strip(), self.Hyphenation.strip(), self.ParaphrasesToString(), self.SentencesToString())
        return str