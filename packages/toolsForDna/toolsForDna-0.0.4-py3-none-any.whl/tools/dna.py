class DNA:
    
    def checkDna(dna):
        dna = str(dna)
        dnaValidity = True
        for ch in dna:
            if ch in 'GTACgtac':
                pass
            elif ch not in 'GTACgtac':
                print('Invalid Character \'{}\''.format(ch))
                dnaValidity = False

        if dnaValidity:
            print('Valid DNA')

    def bases():
        print('Valid DNA bases:\nA - Adenine\nT - Thymine\nG - Guanine\nC - Cytosine')

    def compliments():
        print('DNA compliments:\nA and T\nC and G')

    def complimentDna(dna):
        dna = str(dna)
        dnaValidity = True
        complete = ''
        for ch in dna:
            if ch in 'GTACgtac':
                if ch in 'Gg':
                    complete += 'C'
                elif ch in 'Tt':
                    complete += 'A'
                elif ch in 'Aa':
                    complete += 'T'
                elif ch in 'Cc':
                    complete += 'G'
            else:
                print('Invalid Character \'{}\''.format(ch))
                dnaValidity = False
                
        if dnaValidity:
            print(complete)
