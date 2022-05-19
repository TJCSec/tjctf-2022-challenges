# n = 16519373013990995627535962183175664350164472552141312288365799496052801671886687906446297212095085998013560122310878527538500348103061350452116798395939788963882512360671263385131933902754153960343186236815410593224686454409120487932036301657632908242234855989053940904593325149317472440804040502913230808326252515367924407850640358142519261324794288164900165650234019747177896169224076927209616508069870771948404643648065799075884841625755326173919117549301484174961319889375207096729666075409621457556815959460218103256293496409375813446636980583935666947245697541761516944368140366914811354579092804200491557737727
# e = 3
# c = 13408145991089856825215963469258397662258666714235959642030097494343239415939424654264120500107251599240947177873803553698781171721735568475154671721266261955803526080521452968971499798809587976092501662355395909018410048963473046670790268742336539402021993679017216001395352250761149363992198667765500068625634639520632912896965358016366362091977903796033152037791426653106883854213403831515008097898993031320968351774393762599078386483442860337277686175443744873813757505622172686017644755463070416062308823104557463095582334710232272057017641525167002218446869226686249365220614359213114888067989760205028241346253

# paste from server, if you're fast it should be no problem :fizzemoji:
(n, e) = (1900909491409543427357118984980690849009499471592688158630180393725024987041942908870259255263086445207694776983355354046699493766916018781805349727325118916333289300691117376726154266384721100157597391719105648741886086960226147599332364892427065049369182401799269686532277507202127849670241403344070297161019430097689838705033226708407173006935053633001561667068967491034998000566990378148289571620798452601277939295209675318645388012786301939633628881142397211, 3)
c = 1241602596071674789655701351413676360580912339610461043162637032934779293962038668473625752011274505211684387305526578214261624959855005791429469352600490557717043304501160688265822167448535508748735131753561249055089735288936634307606046641307995381252778048842932343198308890523799546972729091240124669097355128484642724608097843142654942473186423444612498337231144242099752914221096766832735322135041411636686108259161479314474846661114012324678097965962989087

R.<x> = PolynomialRing(Integers(n))
f = (2^1385 * 31415 + 2^500 * x^2 + x)^3 - c
f = f.monic()
print(f.small_roots(X=2^200, epsilon=1/(f.degree()*4)))