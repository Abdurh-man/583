def Ch(x,y,z):
    x_and_y = x & y
    notx_and_z = ~x & z
    xored = x_and_y ^ notx_and_z
    return xored

def Parity(x,y,z):
    xored = x ^ y ^ z
    return xored

def Maj(x,y,z):
    x_and_y = x & y
    x_and_z = x & z
    y_and_z = y & z
    xored = x_and_y ^ x_and_z ^ y_and_z
    return xored

def ft(x,y,z,t):
    if t >= 0 and t <= 19:
        return Ch(x,y,z)
    if t >= 20 and t <= 39:
        return Parity(x,y,z)
    if t >= 40 and t <= 59:
        return Maj(x,y,z)
    if t >= 60 and t <= 79:
        return Parity(x,y,z)

def ROTL(n,x):
    a = x << n
    b = x>>(32-n)
    return (a|b)&0xffffffff

# SHA-1 Constants Kt
#        0-19       20-39      40-59      60-79   
Kt = [0x5a827999,0x6ed9eba1,0x8f1bbcdc,0xca62c1d6]
# do val//20 to get indexs if val = 29//20 = 1 

def Pad(word):
    msg_size = len(word)*8
    k = msg_size%448
    padded_msg = ""
    
    if msg_size >= 448:
        k-= 64

    for block in word:
        for i in range(len(block)): 
            #adding the binary value of word to the padded msg 
            padded_msg += ''.join(f"{ord(block[i]):08b}")
            

    padded_msg += "1" 
    for i in range(448-k-1):
        padded_msg += "0" 
    #gettin the message size in binarry and adding zero's infront of it 
    size = bin(msg_size) 
    size = size[2:] 
    padded_msg +=size.zfill(64) 

    return padded_msg

#16 blocks of 32 bit words 
def Parsing(word):
    M = []
    for i in range(16):
        block = " "
        for j in range(32):
            block+=(word[(i*32)+j])
        M.append(int(block,2))
    return M

def H0():
    H = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    return H

#preparing the message schedule Wt
def Schedule_WT(M):
    W = [0] * 80
    for t in range(0,80): 
        if t < 16: 
            #break Mi ininto 16 words W0, W1 .. W15 
            W[t] = M[t]   
        if (t >= 16): 
            w = W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]
            W[t] = ROTL(1,w)
    return W

# #SHA 1 has a has value of five 32-bit words
def SHA1(word = "abc"):
    H = H0()
    padded_msg = Pad(word)
    N = len(padded_msg)//512 
    for i in range(1,N+1):
        #get the corressponding block
        M = Parsing(padded_msg[(i-1)*512:i*512])

        Wt = Schedule_WT(M)


        
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
            
        for t in range(80):
            T = (ROTL(5,a) + ft(b,c,d,t) + e + Kt[t//20] + Wt[t]) & 0xffffffff
            e = d
            d = c
            c = ROTL(30,b)
            b = a
            a = T


        

        H[0] = (H[0] + a)&0xffffffff
        H[1] = (H[1] + b)&0xffffffff
        H[2] = (H[2] + c)&0xffffffff
        H[3] = (H[3] + d)&0xffffffff
        H[4] = (H[4] + e)&0xffffffff

    string = f'{hex(H[0])[2:]}{hex(H[1])[2:]}{hex(H[2])[2:]}{hex(H[3])[2:]}{hex(H[4])[2:]}'
    return string

test1 = "This is a test of SHA-1."
test2 = "Kerckhoff's principle is the foundation on which modern cryptography is built."
test3 = "SHA-1 is no longer considered a secure hashing algorithm."
test4 = "SHA-2 or SHA-3 should be used in place of SHA-1."
test5 = "Never roll your own crypto!"

print(SHA1(test1))
print(SHA1(test2))
print(SHA1(test3))
print(SHA1(test4))
print(SHA1(test5))


def Wraper(msg,n):
    msg_digest = SHA1(msg)
    return msg_digest[:n]


import random
from collections import Counter

def attack(msg,n):
    Hash = []
    given_hash = Wraper(msg,n)
    Hash.append(given_hash)
    
    letters = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    preimage = 0
    collision = 0
    collion_check = False
    while True:
        string_to_try = ""
        for i in range(n):
            string_to_try += random.choice(letters)
        
        preimage+=1
        
        new_hash = Wraper(string_to_try,n)
        if Hash.count(new_hash) > 1 and collion_check == False:
            collision = preimage
            collion_check = True

        Hash.append(new_hash)

        if new_hash == given_hash:
            break

    return preimage, collision

def Sample(n):
    letters = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    
    x = [i for i in range(50)]
    preimage = []
    collision = []
    for i in range(50):
        random_string = ""
        for j in range(n):
                random_string += random.choice(letters)
        
        pre,col = attack(random_string,n)

        preimage.append(pre)
        collision.append(col)

    
    return preimage,collision


import matplotlib.pyplot as plt
from multiprocessing import Pool
from itertools import product

if __name__ == '__main__':
    letters = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            
    n = [2]
    msg = []
    for i in range(50):
            random_string = ""
            for j in range(n[0]):
                    random_string += random.choice(letters)


    pool = Pool(processes=5)
    for i in pool.imap_unordered(attack, product(msg,n)):
        print(i)
            # with Pool(processes=5) as pool:
    #     results = pool.imap_unordered(attack, product(n,msg))
    # print(results)
            
