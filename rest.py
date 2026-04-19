'''
class Soru:
    def __init__(self,tex,cevaplar,cevap):
        self.tex = tex
        self.cevaplar = cevaplar
        self.cevap = cevap

    def cevapkontrol(self,cevap):
        return self.cevap == cevap
class Quiz:
    def __init__(self,sorularim):
        self.sorularim = sorularim
        self.score = 0
        self.soruindex = 0
    def sorual(self):
        return self.sorularim[self.soruindex]
    def displaysoru(self):
        soru = self.sorual()
        print(f'Soru {self.soruindex+1}:  {soru.tex}')
        for q in soru.cevaplar:
            print('-'+q)
        cevap = input('cevap : ')
        self.tahmin(cevap)
        self.soruoku()
    def tahmin(self,cevap):
        soru = self.sorual()
        if soru.cevapkontrol(cevap):
            self.score += 1
        self.soruindex +=1
        
    def soruoku(self):
        if (len(self.sorularim) == self.soruindex):
            self.showscore()
        else:
            self.displayprogress()
            self.displaysoru()

    def showscore(self):
        print(f'quiz bitt.skorun:{self.score}')

    def displayprogress(self):
        toplamsoru = len(self.sorularim)
        soruno = self.soruindex + 1
        if soruno > soruno:
            print('Quiz bitti.')
        else:
            print('')
            print(f' Soru {soruno} of {toplamsoru} '.center(100,'*'))

q1 = Soru('en iyi programlama dili hangisidir',['c#','python','java','javascript'],'python')
q2 = Soru('en popüler programlama dili hangisidir',['python','java','javascript','c#'],'python')
q3 = Soru('en çok kazandıran programlama dili hangisidir',['c#','java','javascript', 'python'],'python')

print(q1.cevapkontrol('python'))
print(q2.cevapkontrol('c#'))
print(q3.cevapkontrol('python'))
sorularim = [q1,q2,q3]

quiz = Quiz(sorularim)
soru = quiz.sorularim[quiz.soruindex]
print(soru.tex)
quiz.soruoku()
'''

