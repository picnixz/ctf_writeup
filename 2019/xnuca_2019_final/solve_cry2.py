from sage.all import *
p =3288422216999903423661700108901083108575994106944884145571316999921204146787666227291955543324239046057785823700493841038265850996232357479480102071642589
n = 16597746147249532247313381804232853931084270059271432789681424149662363475662745587224756968693512120654332090998063914792173867021664880270091034083347370105767920555864814140123045223783344892866301669542507057829821168626181601212308267787015983118032887285133151191383891486184889114994173062857860171351
e = 7
d0 = 343451398509615859442849377366687472790356452786853392072112558231250061287660705568272638120099956860613924535278628288281586489537632281361059909399161556241133504579321799133085157979094796960482574697558530316982367870152118359
known_bits = 500
d0 = d0 % (2 ** 510)
X = var('X')
P.<x> = PolynomialRing(Zmod(n))
for k in range(1, e+1,1):
    print(k)
    try:
        results = solve_mod([e * d0 * X - k * X * (n - X + 1)*(p-1) + k * n *(p-1)== X], 2 ** known_bits)
        for m in results:
            print(m[0])
            f = x * 2 ** known_bits + ZZ(m[0])
            f = f.monic()
            roots = f.small_roots(X = 2 ** (512-500), beta=0.3)
            if roots:
                print(roots)
                x0 = roots[0]
                q1 = gcd(2 ** known_bits * x0 + ZZ(m[0]), n)
                print('[+] Found factorization!')
                print('q1 =', ZZ(q1))
                print('q2 =', n / ZZ(q1))
                break
    except:
        continue
p =3288422216999903423661700108901083108575994106944884145571316999921204146787666227291955543324239046057785823700493841038265850996232357479480102071642589

n = 54580397182739912335376330801514560808534378753846350995419578067656755867243870073445854335844358326878566119551057553139363647728400886863767875291906080633173065202701573390251537106493792229480326778970832492725717643550358608531505584646072555177837299213009013314327846948963544662473070227953727161317904038137823434569495135916298611352964518151986315681391530493052604576831259172476211158951329919970235487267372187125876292271088905311799477569267739
c = 49869844698848599191424033997655237749665530908239044936694535125887900603704350719900641922970802648673249568670750527924761908125543162254223888002099942596941033383503096686373752238771229983034735635693504897316301489736557100581419752458242416211917551111923109367626016272287394002810362989991474456088280552255576029205508896664588713771229744677826904374660549517673984057742367379244384117320892862126982326170099417167974101776171209333436778309094577
n1 = n/p
q2 =  5517831324006942795599422725480474271762380946611190781111978686110731952752858710698005823515027868947630505335349062725169538285013125885077529317183573
q1 = n1/q2
d = inverse_mod(7,(p-1)*(q2-1)*(q1-1))
from Crypto.Util.number import long_to_bytes
long_to_bytes(pow(c,d,n))

# >>  XNUCA{it_m4y_raiN_if_1t_i5_cloudy}