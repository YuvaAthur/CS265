

from itertools import permutations

l0 = 'ABCDE'
L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
L1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CT = 'PBFPVYFBQXZTYFPBFEQJHDXXQVAPTPQJKTOYQWIPBVWLXTOXBTFXQWAXBVCXQWAXFQJVWLEQNTOZQGGQLFXQWAKVWLXQWAEBIPBFXFQVXGTVJVWLBTPQWAEBFPBFHCVLXBQUFEVWLXGDPEQVPQGVPPBFTIXPFHXZHVFAGFOTHFEFBQUFTDHZBQPOTHXTYFTODXQHFTDPTOGHFQPBQWAQJJTODXQHFOQPWTBDHHIXQVAPBFZQHCFWPFHPBFIPBQWKFABVYYDZBOTHPBQPQJTQOTOGHFQAPBFEQJHDXXQVAVXEBQPEFZBVFOJIWFFACETAOINCFHQWAUVWFLQHGFXVAFXQHFUFHILTTAVWAFFAWTEVOITDHFHFQAITIXPFHXAFQHEFZQWGFLVWPTOFFA'
Fs ='etaoinshrdlcumwfgypbvkjxqz '
SETAOIN = ' ETAOINSHRDLCUMWFGYPBVKJXQZ' #space has the highest frequency of occurance! ref: http://www.data-compression.com/english.html 
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ' # announcements
ETAOIN2 = 'ETAOINSRHLDCUMWFGYPBVKJXQZ' # http://norvig.com/mayzner.html

def shift_cipher(s = 0, a=L):
    l = len(a)
    # check for duplicates
    u = "".join(set(L))
    print ("Alpha set is Unique? %s"%(l==len(u)))
    c = a[s:len(a)]+a[0:s] #cipher
    # using dictionary comprehension 
    # to convert lists to dictionary 
    d = {a[i]: c[i] for i in range(len(a))} #dictionary
    return c,d

def subs(c,d): # given character c and disctionary d, return substitute value
    return d[c]

def encrypt(s,d): # given string s and dictionary d, encrypt
    return ''.join(map(lambda x : d[x],s))

def decrypt(ct,g): # given ciphertext ct, and a shift guess g, decrypt
    c,d = shift_cipher(g,L)
    di = {v: k for k, v in d.items()} #dictionary inverse
    return ''.join(map(lambda x : di[x],ct))

def decrypt_brute(ct,a): #using shift only
    for i in range(len(a)):
        c,d = shift_cipher(i,L)
        di = {v: k for k, v in d.items()} #dictionary inverse
        pt = ''.join(map(lambda x : di[x],ct))
        print ("Suggestion %s \n"%pt)

def freq_decipher():
    sl= (''.join(sorted(CT))) # sort cipher text
    a = L1
    df= {a[i]: CT.count(a[i]) for i in range(len(L1))} #find frequency dictionary in CT
    # print (df) 
    #dr = {k: v for k, v in sorted(df.items(), key=(lambda item: item[1]))} #ascending order
    r = sorted(df, key=df.get, reverse=True) #sort the keys using values in reverse order
    dr = dict() # Ranks the frequency of occurance of each character
    drm = dict() # Maps found frequency with known (english) frequency --> decryption cipher
    i=0
    # print(len(ETAOIN))
    for l in r:
        dr[l]=df[l]
        drm[l]=ETAOIN2[i]
        i = i+1
    # print (dr) 
    # print (drm)
    return df,dr,drm 

def the_score(s): #'THE' occurs 7.14% : Ref: http://norvig.com/mayzner.html
    return s.count('THE')

def the_decipher(m):
    df,dr,drm = freq_decipher()
    r = sorted(df, key=df.get, reverse=True) #sort the keys using values in reverse order
    ctf = ''.join(r) #cipher text frequency 
    snip = 10 #upto first 10 letters since ETAOIN[:10] contains all letters of 'the'
    ctf_snip = ctf[:snip] 
    ctf_snip_ex = ctf[snip:]
    print ("First snip %s and Excluding snip %s"%(ctf_snip, ctf_snip_ex))

    print (list(drm)[snip:])
    drm_snip_ex = {k: drm[k] for k in list(drm)[snip:]} #exclude the first snip elements
    print (drm_snip_ex)

    perms = [''.join(p) for p in permutations(ETAOIN[:snip])]
    print ('Number of perms is %d'%len(perms))
    # print(perms)
    the_max = m
    good_perms = list()
    for p in perms:
        dc = {ctf_snip[i]: p[i] for i in range(len(ctf_snip))} # decrypt cipher dictionary based on permutation
        dc.update(drm_snip_ex) #merge the start and end of the dictionary
        # print(dc)
        pt = encrypt(CT,dc) #apply the decryption cipher!
        t = the_score(pt) #see if any instance of 'the' exists
        if t>=the_max:
            if t>the_max:
                the_max = t 
            # print(dc)
            # print("%s score of permutation %s is %d"%(pt,p,t))
            good_perms.append(dc)
    return the_max,snip,good_perms






def test01():
    s=5
    c,d = shift_cipher(s,L)
    print("%s shifted by %d gives cipher code %s \n"%(L,s,c))
    print (d)
    pt = 'Hello World'
    ct = encrypt(pt,d)
    print("Encrypting %s give %s\n"%(pt,ct))
    print("Decrypting %s gives %s \n"%(ct,decrypt(ct,s)))

def test02():
    print("Decrypting %s by brute force shift substitution: \n"%CT)
    decrypt_brute(CT,L1)

def test03():
    l = ''.join(list(permutations(l0))) 
    print (l)


def test04():
    print (CT + "\n")
    df,dr,drm = freq_decipher()
    pt = encrypt(CT,drm)
    # print ("\n Cipher text letter frequency raw\n")
    # print (df) 
    print ("\n Cipher text letter frequency \n")
    print (dr)
    print ("\n Mapping cipher letter frequency to English letter frequency \n")
    print (drm)
    print ("\n Decrypted text \n")
    print( pt + "\n")
    print ("\n Number of times 'the' occurs  \n")
    print (the_score(pt))

def test05(m):
    return the_decipher(m)

def main():
    s = 'this is the one'
    print("found %d 'THE' in %s"%(the_score(s),s))
    s = 'this is THE THE one'
    print("found %d 'THE' in %s"%(the_score(s),s))    
    s='the time has come the walrus said to talk of many things of shoes and ships and sealingwax of cabbages and kings and why these a is boiling hot and whether pigs have wings but wait a bit the oysters cried before we have our chat for some of us are out of breath and all of us are fat no hurry said the carpenter they thanked him much for that a loaf of bread the walrus said is what we chiefly need pepper and vinegar besides are very good indeed now if youre ready oysters dear we can begin to feed'.upper()
    print("found %d 'THE' in %s"%(the_score(s),s))  
    # m=2
    # m,s,l= test05(m)
    # print ("max THE occurances are %d for snip size %d"%(m,s)) # --> Found max THE = 8
    m,s,l= test05(8)
    print ("max THE occurances are %d for snip size %d giving %d good_perms"%(m,s,len(l))) # --> Found good_perms = 5040

if __name__ == "__main__":
    main()