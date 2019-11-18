# ASIS 2019 final writeup
## Cursed app
> use angr to find a path in the elf
```python
import logging
import angr
import claripy
import hashlib

'''
bruteforce 0x10 bytes at once, so need to modify the script and run 0x3b/0x10+1 times
'''

logging.basicConfig()
base = 0x400000
angr.manager.l.setLevel('DEBUG')
p = angr.Project("cursed_app.elf",load_options={'auto_load_libs': False})
length = 0x3b
f = claripy.BVS('f', 8*length)
state = p.factory.blank_state(addr=0x00117F + base)
# state.memory.store(0xffff0000,f)
state.memory.store(0xdddd0000,f)
state.regs.esp= 0x00117F+base
state.regs.rbx= 0xdddd0000
for i in range(length):
    b=state.memory.load(0xdddd0000+i,1)
    state.add_constraints(b>=0x20)
    state.add_constraints(b<=0x7f)
for i in range(0x30):
    b=state.memory.load(0xdddd0000+i,1)
    state.add_constraints(b==ord('ASIS{y0u_c4N_s33_7h15_15_34513R_7h4n_Y0u_7h1nk_r'[i]))
sm = p.factory.simgr(state)
find = 0x01F3B

sm.explore(find=0x01F3B + base,avoid=[0x0001F4F+base])
print(sm)
print(sm.found)
for s in sm.found:
    x = s.solver.eval(s.memory.load(0xdddd0000,length), cast_to=bytes)
    print(x)
    if hashlib.sha256(x) == "dd791346264fc02ddcd2466b9e8b2b2bba8057d61fbbc824d25c7957c127250d":
        print("founded+++++++++")
```

## Close primes
> find two large close 512-bit primes that have a big prime gap.
[top 10k prime gaps recode](http://www.trnicely.net/gaps/g10k.html)

```
9377805670840016996446741383808930516890234095746631584854460251777184462990769752546763229345156837328451121268831558567987675686078157872050812483426349
```
## Primordial

> this is a problem about finding small integer roots of a bivariate polynomial modulo an integer.

Here we have **s0\*product_of_primes - r0** and **s1\*product_of_primes - r1**. since `p`,`q` are 512-bit primes, we can limit product_of_primes to a small range. and bruteforce `r0`,`r1` to with [Coron's reformulation of Coppersmith's algorithm](https://github.com/ubuntor/coppersmith-algorithm) to find a small_roots. So we recover `s0`,`s1`. 
ideas for [@ndh]():We can also limit `r0`,`r1` by the condition that `n - r0*r1` is divided by prime in the range [3x,6x]. So if we combine those two limits we can reduce the algorithm complexity.

```python

a = [256201040651931599305382461251925781858847170265198996852091190629324168449027728035542876334984578188245059186229973899465052910204193443350680384306794366570, 1168489079156465704987173290774096471177444024124720198139827803196157871127649219224446996884272620699035170, 2305567963945518424753102147331756070, 195133959955058134502488637025552252876537200920889365778484014616008832503770745901542489344429915739687480227261852231729170, 1268272178988474870180783637732839510919079989588742918676346230708618204152237747680057948402909410467856442998771862105666479007064598335966363172634437241238747784918327090, 2184388827958183606469810778001988127598001347644753877628597514732473285653996655943128229044607914390526120724168070692914015911034911541522425303161947419103871515655013288351117524591190137770, 101711813138816844924236837117014535397962326595284001750280202679841694874264008030110521904988877540733288496933299638087626005351064797010220112569797363528290, 2043779758005154482257388030892804056228591188672553240869361360495290305558100337270153956915591354354320728837959427210, 367009731827331916465034565550136732339800312955331782619462457039988073311157667212930, 5397346292805549782720214077673687806275517530364350655459511599582614290, 5766152219975951659023630035336134306565384015606066319856068810, 241082053687382222648054619345722264112075157980955375182430625956709108572686416743259175238063841107603427680307546952079823995015888303888838076396562271875349850191770041556830, 7858321551080267055879090, 47952908052796135760256600170199578387740533448517890811411728517171138658867337095151452769077564443190074989606933241597341551376625294861617115261811011811910212652094403655944384810, 1492182350939279320058875736615841068547583863326864530410, 627440385707582426053018125484090845262177494922473844946893937672054123806336803541937264773086545786776463753253544153470, 279734996817854936178276161872067809674997230, 64266330917908644872330635228106713310880186591609208114244758680898150367880703152525200743234420230, 166589903787325219380851695350896256250980509594874862046961683989710, 1719620105458406433483340568317543019584575635895742560438771105058321655238562613083979651479555788009994557822024565226932906295208262756822275663694110, 29819592777931214269172453467810429868925511217482600306406141434158090, 225319534991831177328890236228992001350685163362356544091910, 962947420735983927056946215901134429196419130606213075415963491270, 16681652761084211919179159418724436936084403222565933843061705761318156534633165693010396587115320816578125913093533540343113453511622786292849190442459895794911314610, 4343825573072363215565699965702960859395702691913457985649917484000586881515424606782330843435957697765930, 19361386640700823163471425054312320082662897612571563761906962414215012369856637179096947335243680669607531475629148240284399976570, 1046322248591969947499039362662952313119442645521837107384098209556854703828264398196758421712367190993062011826876505861905813621385722628389241720214572813750754455998751365120185294279180075991830, 3217644767340672907899084554130, 23768741896345550770650537601358310, 1645783550795210387735581011435590727981167322669649249414629852197255934130751870910, 2942626865402493898331284542303571951088352644057408163982241834590761494552755795081340947570555476723564832943786222982984870085996747879272304344859483158326560985889390, 72047817630210000485677936198920432067383702541010310, 6989612506894284794136067796445539076219364950255126280242854713992307588011296425371356170001319422146234757586190553403764537021369947456703810795390696338067840821590, 1062411448280052319722448549835623701226301211611796930357321893850294264731624591303255041960530, 2566376117594999414479597815340071648394470, 62797802135946735863734268232365323600796854989079318289826397214991489160762431714712874321823048719463864215556568570809157897364620234601356930764612312239892910549558645813243759770009793795858849126367670, 2159704595610254721415747050533376368260798239989520222949435936418441984820398307416727184404426847652711313512004598759003964186453790, 557940830126698960967415390, 525896479052627740771371797072411912900610967452630, 61076929465933196099278943388997855150356143888238371488665496574810764573680243467182799164806563626522181311132959748531230210, 267064515689275851355624017992790, 92325987091692603167246758916442447848897069587880156248625475693453150629759757766750033011164044499544063264686235401999614947429856005620610, 549161853502009618788279315138319508227961635491925683786857917896831682397918944745465091658459774732581839818468216291753585410058971079473435253750711325456377790869635629970, 31964081287196888554640742530273949712805599189441373009521636182430667982828077742788853029807931798207106885718293402541861369758591699412090677759187666930105491469725350718941073722934985042092154205321144030, 261546705642188677527611215060743478325487449257450867559845540208082579687704696223087912212929304531286298200244292923511657074872113330370, 19078266889580195013601891820992757757219839668357012055907516904309700014933909014729740190, 24647906487115793512432470614609487044327490547070674282967249490409801198254927547005559122946385681862066942895590, 6408618978071972467109041692977377947361419109761187605191204559105169094422546906281089567965658301640092918433248067534136392244670, 4445236185272185438169240794291312557432222642727183809026451438704160103479600800432029464270, 4677492136955425281519937426128454234685227725149365904986290181439985622385431811441388070759331722463653363435049401912021447346969831994694700863301814601935485044229150510387831958439379310, 23984823528925228172706521638692258396210, 35375166993717494840635767087951744212057570647889977422429870, 124846525121166472890127769845656706959834701767553316679575342375728606681436245953703527478773456698735316531921607496638484885416740029028542605893861455745313937474271661656548230159065196413238268640890, 87714969705038411076272137418539099801877190558970371113762453702525982911939243939521562715111692818014473106390, 749417494676758388331264226535081599786496989276363517363454269937199368732678212673604332988336116135490825788665595769374375572699465130, 1030893141925860008499560888835674370998623848299590975192766715520279329390, 256041159035492609053110100510385311995538591998443060216114576417920917800321526504084465112487730, 10014646650599190067509233131649940057366334653200433090, 198962376391690981640415251545285153602734402721821058212203976095413910572270, 39195588149163123383161804554421175259738677336198748467804183290796540382737190, 10102574809838931493563579754057136575994012365333403682475788728812063979234193977195222615030954044197955428585419874540003126019373287245560908992012558535497807870905292679023395158616370, 16516447045902521732188973253623425320896207954043566485360902980990824644545340710198976591011245999110, 31610054640417607788145206291543662493274686990, 40729680599249024150621323470, 316660540451402206051523961799780143689087330537799173695893334666158783075592938409825136155637880209438531070, 12164225777291775545094262227518041831435735609411974226225152299039532954922737365042617099319896354948428967312205572919655268168725818308532229330, 106799349783510324633088196370154963001649294985563231205816767298822135097700082617263814630462281610668318462376243299771362029792038518622755267843677086440779983634954128409675690, 658614500390569664024119437665618976500892468548069400648049333237337193956369480811164206516669866807827915645835408481915303111064764635862931579194844130, 33145029365917644537041586451002838777754047982048976093256545773949681076083753038263261851007891975336318712022358509317861766127318306017798990, 40786437068665554814618971683922828694582892964708884701862361274616519644579867220074319283900539893834048687270253154873138028145776983601098265140488742774844290, 232862364358497360900063316880507363070, 21914478980127834042437266277781207323197423785972676100815159932347210367102373052484213915468446950537864270250368491409985088979117759751759021674647632398042967182007142470766583858170, 250193437116566077936127795281877168256181767069245123606363411574606426215303098103614283524596105608688009082007229452181332435704889837732550312412548007505639153255053430173443347012154702230938414110, 6975357535853769564018389183934484833544679824821000822079731605785973739106144495802573231793827147966964944839451970, 16653286350629578936967826858272727800371717177698955337960772451046378019053428503992992428529932466865902687459230862724309773644226275393699243112536774470584961055726907724568299409649127206930012340972316039630, 83311209124804345037562846379881038241134671040860314654617977748077292641632790457335110, 4014476939333036189094441199026045136645885247730, 7799922041683461553249199106329813876687996789903550945093032474868511536164700810, 4537256214929832278320159810864229603125529382310666386381981807541745792186181037160896178046321340395764004807452678699031415026934730229082521540090, 509558935064289364432032169616857776489168568369134671296055828054188240764364761921821351373922822013621199759688858354748131233614846920025560717744496960296617420071391914813530238313960697008021210]
b = [2310, 6, 223092870, 9699690, 6469693230, 30030, 510510, 210, 200560490130, 30]
c = [1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014, 1016, 1018, 1020, 1022, 1024, 1026, 1028, 1030, 1032, 1034, 1036, 1038, 1040, 1042, 1044, 1046, 1048, 1050, 1052, 1054, 1056, 1058, 1060, 1062, 1064, 1066, 1068, 1070, 1072, 1074, 1076, 1078, 1080, 1082, 1084, 1086, 1088, 1090, 1092, 1094, 1096, 1098, 1100, 1102, 1104, 1106, 1108, 1110, 1112, 1114, 1116, 1118, 1120, 1122, 1124, 1126, 1128, 1130, 1132, 1134, 1136, 1138, 1140, 1142, 1144, 1146, 1148, 1150, 1152, 1154, 1156, 1158, 1160, 1162, 1164, 1166, 1168, 1170, 1172, 1174, 1176, 1178, 1180, 1182, 1184, 1186, 1188, 1190, 1192, 1194, 1196, 1198, 1200, 1202, 1204, 1206, 1208, 1210, 1212, 1214, 1216, 1218, 1220, 1222, 1224, 1226, 1228, 1230, 1232, 1234, 1236, 1238, 1240, 1242, 1244, 1246, 1248, 1250, 1252, 1254, 1256, 1258, 1260, 1262, 1264, 1266, 1268, 1270, 1272, 1274, 1276, 1278, 1280, 1282, 1284, 1286, 1288, 1290, 1292, 1294, 1296, 1298, 1300, 1302, 1304, 1306, 1308, 1310, 1312, 1314, 1316, 1318, 1320, 1322, 1324, 1326, 1328, 1330, 1332, 1334, 1336, 1338, 1340, 1342, 1344, 1346, 1348, 1350, 1352, 1354, 1356, 1358, 1360, 1362, 1364, 1366, 1368, 1370, 1372, 1374, 1376, 1378, 1380, 1382, 1384, 1386, 1388, 1390, 1392, 1394, 1396, 1398, 1400, 1402, 1404, 1406, 1408, 1410, 1412, 1414, 1416, 1418, 1420, 1422, 1424, 1426, 1428, 1430, 1432, 1434, 1436, 1438, 1440, 1442, 1444, 1446, 1448, 1450, 1452, 1454, 1456, 1458, 1460, 1462, 1464, 1466, 1468, 1470, 1472, 1474, 1476, 1478, 1480, 1482, 1484, 1486, 1488, 1490, 1492, 1494, 1496, 1498, 1500, 1502, 1504, 1506, 1508, 1510, 1512, 1514, 1516, 1518, 1520, 1522, 1524, 1526, 1528, 1530, 1532, 1534, 1536, 1538, 1540, 1542, 1544, 1546, 1548, 1550, 1552, 1554, 1556, 1558, 1560, 1562, 1564, 1566, 1568, 1570, 1572, 1574, 1576, 1578, 1580, 1582, 1584, 1586, 1588, 1590, 1592, 1594, 1596, 1598, 1600, 1602, 1604, 1606, 1608, 1610, 1612, 1614, 1616, 1618, 1620, 1622, 1624, 1626, 1628, 1630, 1632, 1634, 1636, 1638, 1640, 1642, 1644, 1646, 1648, 1650, 1652, 1654, 1656, 1658, 1660, 1662, 1664, 1666, 1668, 1670, 1672, 1674, 1676, 1678, 1680, 1682, 1684, 1686, 1688, 1690, 1692, 1694, 1696, 1698, 1700, 1702, 1704, 1706, 1708, 1710, 1712, 1714, 1716, 1718, 1720, 1722, 1724, 1726, 1728, 1730, 1732, 1734, 1736, 1738, 1740, 1742, 1744, 1746, 1748, 1750, 1752, 1754, 1756, 1758, 1760, 1762, 1764, 1766, 1768, 1770, 1772, 1774, 1776, 1778, 1780, 1782, 1784, 1786, 1788, 1790, 1792, 1794, 1796, 1798, 1800, 1802, 1804, 1806, 1808, 1810, 1812, 1814, 1816, 1818, 1820, 1822, 1824, 1826, 1828, 1830, 1832, 1834, 1836, 1838, 1840, 1842, 1844, 1846, 1848, 1850, 1852, 1854, 1856, 1858, 1860, 1862, 1864, 1866, 1868, 1870, 1872, 1874, 1876, 1878, 1880, 1882, 1884, 1886, 1888, 1890, 1892, 1894, 1896, 1898, 1900, 1902, 1904, 1906, 1908, 1910, 1912, 1914, 1916, 1918, 1920, 1922, 1924, 1926, 1928, 1930, 1932, 1934, 1936, 1938, 1940, 1942, 1944, 1946, 1948, 1950, 1952, 1954, 1956, 1958, 1960, 1962, 1964, 1966, 1968, 1970, 1972, 1974, 1976, 1978, 1980, 1982, 1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026, 2028, 2030, 2032, 2034, 2036, 2038, 2040, 2042, 2044, 2046, 2048, 2050, 2052, 2054, 2056, 2058, 2060, 2062, 2064, 2066, 2068, 2070, 2072, 2074, 2076, 2078, 2080, 2082, 2084, 2086, 2088, 2090, 2092, 2094, 2096, 2098, 2100, 2102, 2104, 2106, 2108, 2110, 2112, 2114, 2116, 2118, 2120, 2122, 2124, 2126, 2128, 2130, 2132, 2134, 2136, 2138, 2140, 2142, 2144, 2146, 2148, 2150, 2152, 2154, 2156, 2158, 2160, 2162, 2164, 2166, 2168, 2170, 2172, 2174, 2176, 2178, 2180, 2182, 2184, 2186, 2188, 2190, 2192, 2194, 2196, 2198, 2200, 2202, 2204, 2206, 2208, 2210, 2212, 2214, 2216, 2218, 2220, 2222, 2224, 2226, 2228, 2230, 2232, 2234, 2236, 2238, 2240, 2242, 2244, 2246, 2248, 2250, 2252, 2254, 2256, 2258, 2260, 2262, 2264, 2266, 2268, 2270, 2272, 2274, 2276, 2278, 2280, 2282, 2284, 2286, 2288, 2290, 2292, 2294, 2296, 2298, 2300, 2302, 2304, 2306, 2308, 2310, 2312, 2314, 2316, 2318, 2320, 2322, 2324, 2326, 2328, 2330, 2332, 2334, 2336, 2338, 2340, 2342, 2344, 2346, 2348, 2350, 2352, 2354, 2356, 2358, 2360, 2362, 2364, 2366, 2368, 2370, 2372, 2374, 2376, 2378, 2380, 2382, 2384, 2386, 2388, 2390, 2392, 2394, 2396, 2398, 2400, 2402, 2404, 2406, 2408, 2410, 2412, 2414, 2416, 2418, 2420, 2422, 2424, 2426, 2428, 2430, 2432, 2434, 2436, 2438, 2440, 2442, 2444, 2446, 2448, 2450, 2452, 2454, 2456, 2458, 2460, 2462, 2464, 2466, 2468, 2470, 2472, 2474, 2476, 2478, 2480, 2482, 2484, 2486, 2488, 2490, 2492, 2494, 2496, 2498, 2500, 2502, 2504, 2506, 2508, 2510, 2512, 2514, 2516, 2518, 2520, 2522, 2524, 2526, 2528, 2530, 2532, 2534, 2536, 2538, 2540, 2542, 2544, 2546, 2548, 2550, 2552, 2554, 2556, 2558, 2560, 2562, 2564, 2566, 2568, 2570, 2572, 2574, 2576, 2578, 2580, 2582, 2584, 2586, 2588, 2590, 2592, 2594, 2596, 2598, 2600, 2602, 2604, 2606, 2608, 2610, 2612, 2614, 2616, 2618, 2620, 2622, 2624, 2626, 2628, 2630, 2632, 2634, 2636, 2638, 2640, 2642, 2644, 2646, 2648, 2650, 2652, 2654, 2656, 2658, 2660, 2662, 2664, 2666, 2668, 2670, 2672, 2674, 2676, 2678, 2680, 2682, 2684, 2686, 2688, 2690, 2692, 2694, 2696, 2698, 2700, 2702, 2704, 2706, 2708, 2710, 2712, 2714, 2716, 2718, 2720, 2722, 2724, 2726, 2728, 2730, 2732, 2734, 2736, 2738, 2740, 2742, 2744, 2746, 2748, 2750, 2752, 2754, 2756, 2758, 2760, 2762, 2764, 2766, 2768, 2770, 2772, 2774, 2776, 2778, 2780, 2782, 2784, 2786, 2788, 2790, 2792, 2794, 2796, 2798, 2800, 2802, 2804, 2806, 2808, 2810, 2812, 2814, 2816, 2818, 2820, 2822, 2824, 2826, 2828, 2830, 2832, 2834, 2836, 2838, 2840, 2842, 2844, 2846, 2848, 2850, 2852, 2854, 2856, 2858, 2860, 2862, 2864, 2866, 2868, 2870, 2872, 2874, 2876, 2878, 2880, 2882, 2884, 2886, 2888, 2890, 2892, 2894, 2896, 2898, 2900, 2902, 2904, 2906, 2908, 2910, 2912, 2914, 2916, 2918, 2920, 2922, 2924, 2926, 2928, 2930, 2932, 2934, 2936, 2938, 2940, 2942, 2944, 2946, 2948, 2950, 2952, 2954, 2956, 2958, 2960, 2962, 2964, 2966, 2968, 2970, 2972, 2974, 2976, 2978, 2980, 2982, 2984, 2986, 2988, 2990, 2992, 2994, 2996, 2998]
def coron(pol, X, Y, k=2, debug=False):
    """
    Returns all small roots of pol.
    Applies Coron's reformulation of Coppersmith's algorithm for finding small
    integer roots of bivariate polynomials modulo an integer.
    Args:
        pol: The polynomial to find small integer roots of.
        X: Upper limit on x.
        Y: Upper limit on y.
        k: Determines size of lattice. Increase if the algorithm fails.
        debug: Turn on for debug print stuff.
    Returns:
        A list of successfully found roots [(x0,y0), ...].
    Raises:
        ValueError: If pol is not bivariate
    """

    if pol.nvariables() != 2:
        raise ValueError("pol is not bivariate")

    P.<x,y> = PolynomialRing(ZZ)
    pol = pol(x,y)

    # Handle case where pol(0,0) == 0
    xoffset = 0

    while pol(xoffset,0) == 0:
        xoffset += 1

    pol = pol(x+xoffset,y)

    # Handle case where gcd(pol(0,0),X*Y) != 1
    while gcd(pol(0,0), X) != 1:
        X = next_prime(X, proof=False)

    while gcd(pol(0,0), Y) != 1:
        Y = next_prime(Y, proof=False)

    pol = P(pol/gcd(pol.coefficients())) # seems to be helpful
    p00 = pol(0,0)
    delta = max(pol.degree(x),pol.degree(y)) # maximum degree of any variable

    W = max(abs(i) for i in pol(x*X,y*Y).coefficients())
    u = W + ((1-W) % abs(p00))
    N = u*(X*Y)^k # modulus for polynomials

    # Construct polynomials
    p00inv = inverse_mod(p00,N)
    polq = P(sum((i*p00inv % N)*j for i,j in zip(pol.coefficients(),
                                                 pol.monomials())))
    polynomials = []
    for i in range(delta+k+1):
        for j in range(delta+k+1):
            if 0 <= i <= k and 0 <= j <= k:
                polynomials.append(polq * x^i * y^j * X^(k-i) * Y^(k-j))
            else:
                polynomials.append(x^i * y^j * N)

    # Make list of monomials for matrix indices
    monomials = []
    for i in polynomials:
        for j in i.monomials():
            if j not in monomials:
                monomials.append(j)
    monomials.sort()

    # Construct lattice spanned by polynomials with xX and yY
    L = matrix(ZZ,len(monomials))
    for i in range(len(monomials)):
        for j in range(len(monomials)):
            L[i,j] = polynomials[i](X*x,Y*y).monomial_coefficient(monomials[j])

    # makes lattice upper triangular
    # probably not needed, but it makes debug output pretty
    L = matrix(ZZ,sorted(L,reverse=True))

    if debug:
        print("Bitlengths of matrix elements (before reduction):")
        print(L.apply_map(lambda x: x.nbits()).str())

    L = L.LLL()

    if debug:
        print("Bitlengths of matrix elements (after reduction):")
        print(L.apply_map(lambda x: x.nbits()).str())

    roots = []

    for i in range(L.nrows()):
        if debug:
            print("Trying row %d" % i)

        # i'th row converted to polynomial dividing out X and Y
        pol2 = P(sum(map(mul, zip(L[i],monomials)))(x/X,y/Y))

        r = pol.resultant(pol2, y)

        if r.is_constant(): # not independent
            continue

        for x0, _ in r.univariate_polynomial().roots():
            if x0-xoffset in [i[0] for i in roots]:
                continue
            if debug:
                print("Potential x0:",x0)
            for y0, _ in pol(x0,y).univariate_polynomial().roots():
                if debug:
                    print("Potential y0:",y0)
                if (x0-xoffset,y0) not in roots and pol(x0,y0) == 0:
                    roots.append((x0-xoffset,y0))
    return roots
n = 129267954332200676615739227295907855158658739979210900708976549380609989409956408435684374935748935918839455337906315852534764123844258593239440161506513191263699117749750762173637210021984649302676930074737438675523494086114284695245002078910492689149197954131695708624630827382893369282116803593958219295071
#ZZ = Zmod(n)
tmp = []
for i in a:
    for j in b:
        if 2**473 < i//j < 2**479:
            tmp.append(i//j)
print(len(tmp))
def test():
    for a1 in tmp:
        print(a1)
        for a2 in tmp:
            for b1 in c[:300]:
                for b2 in c[:300]:
                    P.<x,y> = PolynomialRing(ZZ)
                    pol = (a1*x-b1)*(a2*y-b2) - n # Should have a root at (x0,y0)
                    XX = next_prime(2^36)
                    YY = next_prime(2^36)
                    kk = 2
                    root = coron(pol, XX, YY, k=2, debug=0)
                    if root:
                        x0_2, y0_2 = root[0]
                        print(a1*x0_2-b1)
                        return
test()
print("done!!!")
p = 13394842547433505159787676402528436220648284157653666605416822687362016499172239825461692829479269475930001888028646916852110203355231711337735488785028939
n = 129267954332200676615739227295907855158658739979210900708976549380609989409956408435684374935748935918839455337906315852534764123844258593239440161506513191263699117749750762173637210021984649302676930074737438675523494086114284695245002078910492689149197954131695708624630827382893369282116803593958219295071
q = n/p
e = 65537
phi = (p-1)*(q-1)
d = inverse_mod(e,phi)
enc = 123828011786345664757585942310038992331055176660679165398920365204623335291878173959876308977115607518900415801962848580747200997185606420410437572095447682798017319498742987210291931673054112968527192210375048958877146513037193636705010232608708929769672565897606711155251354598146987357344810260248226805138
from Crypto.Util.number import *
print(long_to_bytes(pow(enc,d,n))) 
```
## Serifin
> The problem is converting a bignumber from float to int. so we can recover `q` by bruteforce a some bytes. After that, we solve a rsa like problem `pow(m,2,n)=c`. to recover `m` we can get m1 mod q, m2 mod p by solve `x^2 - c = 0` over PolynomialRing field `p` and `q`, and use `crt` to get `m`.

```
import random
print(hex(int(float(random.randint(1,2**512)))))
0x44e3bf0e9c552c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```
```python
import gmpy2
c = 78643169701772559588799235367819734778096402374604527417084323620408059019575192358078539818358733737255857476385895538384775148891045101302925145675409962992412316886938945993724412615232830803246511441681246452297825709122570818987869680882524715843237380910432586361889181947636507663665579725822511143923
n = 420908150499931060459278096327098138187098413066337803068086719915371572799398579907099206882673150969295710355168269114763450250269978036896492091647087033643409285987088104286084134380067603342891743645230429893458468679597440933612118398950431574177624142313058494887351382310900902645184808573011083971351
mul = 3.6634615384615383
pp1 = 10718841513477904890207301699752584410662537695964131954151123981554118623721990017759084195679992488466167639761764341239311468015184628316819286481548196
print(hex(int(pp1*mul)))
t = 0x2edc24bf9255aaa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# for i in range(0xaa-0x20,0xaa+0x20):
#     q = ((0x2edc24bf9255a<< 8+ i)<<456
#     for j in range(0,10):
#         q = gmpy2.next_prime(q)
#         if n%q ==0:
#             print(q)
#             break
# print("DDD")
p = 39268063621491165558293370755773815300739539018598511154583095766289789691669875090357609442626770422364550257841199885538175542665396553281747272813511469
q = n/p
print(n%p)
d = lcm((p-1)*(q-1),3)
#d = inverse(3,(p-1)*(q-1))
print(d)
from Crypto.Util.number import *
print(pow(c,d,n))
print(long_to_bytes(pow(c,d,n)))
P.<a> = PolynomialRing(Zmod(p), implementation='NTL')
f = a^3 - c
res_p = [int(i[0]) for i in f.monic().roots()]
P.<a> = PolynomialRing(Zmod(q), implementation='NTL')
f = a^3 - c
res_q = [int(i[0]) for i in f.monic().roots()]
for i in res_p:
    for j in res_q:
        print(long_to_bytes(crt([int(i),int(j)],[p,q])))
```

## Golden Delicious
* first recover n1, n2 using two points on the ecc.
* misc part: gcd(n1,n2) = common factor, so reduce curve 512 to curve 256. reconstruct by crt.
* the curve order is equal to GF(p), [smart attack](https://crypto.stackexchange.com/questions/70454/why-smarts-attack-doesnt-work-on-this-ecdlp) mentioned by [@ndh]().
```sage
from Crypto.PublicKey import RSA
import json
from Crypto.Util import number
from hashlib import sha256
(A_1, B_1) = (4100133310575364011719743521079184461074386086908714625945625015559982177755652249240883318459158099254673716037393799806563567496713759930310260790170700L, 1122736575135956550498512579475613266532272320672056044481173789518413402619422268998022672611181357437113262000853974968410911833838413926464792002813447L)
(A_2, B_2) = (7195356291935324092974083800656294719909791991638016800688869531480914420851344517648017858841138300709252000726562477192528094479414307745557474907942803L, 6294820679829743993553990213393473947712658480308258869413745721454083757402985469790896377224901851178278372055326475131634987824882821588180629785125494L)
P1_x,P1_y = (2020 , 1541289077285950476559411104738671299410620709860226880193167593009859736744811748999762048127883283085467497522757803253784396241175263384974343969389613)
P2_x,P2_y = (2019 , 4974488224848659884031032545639754297422048908695379071395934742158247177808858717918207312066922185990894913147917789468490894652686551750625949315572060)
Q1_x,Q1_y = (618557765800750819209991316860882839555616891049138511957097251334207165235365069009990394212384430641656483864543452461074647961570036980133121226790676 , 1912192017248939370370171524353367472317941092660336078617752789285987994955919216772863103147273102025883679405387407568801952770276812434793253510856342)
Q2_x,Q2_y = (3498315230862051726722937542044146709141760804952759034107762377825674224891256652411838536715783050883855279807866167028753678099833796125634334124551556, 1700134660303914635540188684404266565369868807277098991690614159152164658899818711426168666271084645702085789685102435043642173628403538966759243249623606)
pp1 = gcd((P1_y^2 -P1_x^3 -A_1*P1_x - B_1),(Q1_y^2 - Q1_x^3 -A_1*Q1_x - B_1))
pp2 = gcd((P2_x^3 +A_2*P2_x + B_2-P2_y^2),(Q2_y^2 - Q2_x^3 -A_2*Q2_x - B_2))

share_p = int(gcd(pp1,pp2))
q1 = int(pp1/share_p)
q2 = int(pp2/share_p/2)

E1 = EllipticCurve(GF(share_p),[A_1,B_1])
E2 = EllipticCurve(GF(q1),[A_1,B_1])
E3 = EllipticCurve(GF(share_p),[A_2,B_2])
E4 = EllipticCurve(GF(q2),[A_2,B_2])

point1 = (2020 , 1541289077285950476559411104738671299410620709860226880193167593009859736744811748999762048127883283085467497522757803253784396241175263384974343969389613)
point2 = (2019 , 4974488224848659884031032545639754297422048908695379071395934742158247177808858717918207312066922185990894913147917789468490894652686551750625949315572060)
ppoint1 = (618557765800750819209991316860882839555616891049138511957097251334207165235365069009990394212384430641656483864543452461074647961570036980133121226790676 , 1912192017248939370370171524353367472317941092660336078617752789285987994955919216772863103147273102025883679405387407568801952770276812434793253510856342)
ppoint2 = (3498315230862051726722937542044146709141760804952759034107762377825674224891256652411838536715783050883855279807866167028753678099833796125634334124551556, 1700134660303914635540188684404266565369868807277098991690614159152164658899818711426168666271084645702085789685102435043642173628403538966759243249623606)
xp1 = E1.point(point1)
xxp1 = E1.point(ppoint1)
xq1 = E2.point(point1)
xxq1 = E2.point(ppoint1)
xp2 = E3.point(point2)
xxp2 = E3.point(ppoint2)
xq2 = E4.point(point2)
xxq2 = E4.point(ppoint2)
#print(x2.discrete_log(x1))
def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])
    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break
    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break
    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp
    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()
    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)
rsp1 = SmartAttack(xp1,xxp1,share_p)
rsq1 = SmartAttack(xq1,xxq1,q1)
rsp2 = SmartAttack(xp2,xxp2,share_p)
rsq2 = SmartAttack(xq2,xxq2,q2)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(crt([rsp1,rsq1],[share_p,q1])))
print(long_to_bytes(crt([rsp2,rsq2],[share_p,q2])))
```

## Hardest Mt.
by [@ndh]().
> here we given a puzzle : find `x` such that `pow(x,x,n) = a.` notice that n is 512 bit length not is not a prime.
* decomposite n into p,q using `yafu` or [online factordb](http://factordb.com/index.php)
* so here the problem is we find `x` that `x = a mod n`, `x = 1 mod phi`. Because because `a^1 = a mod n`, the base `(a)` has cycle of length `n`, and the exponent `(1)` has cycle of length `phi(n)`
* So crt to find such `x`.