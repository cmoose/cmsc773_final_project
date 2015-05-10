#plotkl

import matplotlib.pyplot as plt
import os
fout = open('plotoutputs.txt', 'w')
for fname in os.listdir("."):
    if fname.endswith("grams.txt") and not fname.startswith('output'):
        fout.write(fname + '\n')
        print fname
        outfile = fname[:-4]+'_plot.png'
        #outfile2 = fname[:-4]+'_plot2.png'

        #print(fname)

        f = open(fname,'r')
        d1 = []
        d2 = []
        grams = []
        distr = 0
        for line in f:
            cnt=0
            line = line.strip()
            if line[0] != '#':
                line = line.split()
                grams.append(line[0])
                d1.append(float(line[1]))
                d2.append(float(line[2]))
            
        f.close()
        '''
        a = sorted(range(len(d1)), key=lambda i: d1[i])[-5:]
        b = sorted(range(len(d2)), key=lambda i: d2[i])[-5:]

        c = []
        for i in a:
            c.append(grams[i])

        fout.write(str(a) + ' ' + str(c) + '\n')
        print a, c

        c = []
        for i in b:
            c.append(grams[i])

        print b, c
        fout.write(str(b) + ' ' + str(c) + '\n')

        '''
        x = []
        for i in range(1, len(d1)+1):
            x.append(i)
        
        plt.plot(x,d1, 'g', alpha=0.5)
        plt.plot(x,d2, 'b', alpha=0.5)
        plt.savefig(outfile)
        #plt.show()

        #plt.plot(x,d2)
        #plt.savefig(outfile2)
        #plt.show()


fout.close()
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()
