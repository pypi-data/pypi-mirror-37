class RNA:
    
    def checkRna(rna):
        rna = str(rna)
        rnaValidity = True
        for ch in rna:
            if ch in 'GUACguac':
                pass
            elif ch not in 'GUACguac':
                print('Invalid Character \'{}\''.format(ch))
                rnaValidity = False

        if rnaValidity:
            print('Valid RNA')

    def complimentRna(rna):
        rna = str(rna)
        rnaValidity = True
        complete = ''
        for ch in rna:
            if ch in 'GUACguac':
                if ch in 'Gg':
                    complete += 'C'
                elif ch in 'Uu':
                    complete += 'A'
                elif ch in 'Aa':
                    complete += 'U'
                elif ch in 'Cc':
                    complete += 'G'
            else:
                print('Invalid Character \'{}\''.format(ch))
                rnaValidity = False
                
        if rnaValidity == True:
            print(complete)
            
    def bases():
        print('Valid RNA bases:\nA - Adenine\nU - Uracil\nG - Guanine\nC - Cytosine')

    def compliments():
        print('RNA compliments:\nA and U\nC and G')
