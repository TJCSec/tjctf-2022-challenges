#include <emscripten.h>

const Uint8 data0[] = {54, 207, 136, 110, 149, 51, 241, 109, 192, 238, 84, 233, 138, 47, 205, 149, 40, 106, 26, 37, 132, 122, 242, 129, 239, 147, 185, 193, 47, 122, 48, 116, 141, 224, 211, 23, 126, 19, 141, 71, 22, 131, 180, 52, 43, 114, 0, 55, 75, 72, 105, 147, 251, 123, 105, 109, 169, 109, 40, 208, 153, 139, 0, 180, 255, 143, 62, 239, 221, 236, 52, 224, 25, 231, 213, 115, 36, 56, 202, 154, 154, 242, 15, 44, 5, 41, 160, 185, 96, 60, 73, 53, 56, 37, 98, 45, 52, 137, 111, 218, 144, 160, 235, 59, 116, 215, 99, 187, 191, 230, 33, 243, 248, 13, 247, 229, 122, 63, 120, 77, 6, 149, 13, 69, 136, 198, 39, 131, 243, 33, 37, 40, 136, 229, 220, 180, 228, 7, 3, 228, 118, 135, 21, 220, 180, 202, 138, 22, 192, 200, 243, 122, 57, 249, 133, 118, 150, 221, 223, 127, 130, 180, 81, 217, 35, 24, 76, 242, 46, 220, 68, 63, 212, 119, 106, 127, 27, 10, 156, 248, 84, 60, 19, 57, 233, 230, 69, 131, 228, 129, 10, 233, 172, 160, 197, 80, 162, 133, 196, 205, 65, 178, 134, 20, 229, 98, 67, 54, 236, 162, 209, 219, 218, 37, 248, 102, 240, 9, 151, 247, 29, 32, 20, 112, 178, 122, 123, 188, 78, 201, 33, 201, 221, 66, 16, 121, 254, 66, 212, 132, 200, 15, 171, 133, 248, 235, 225, 158, 26, 159, 118, 244, 29, 58, 215, 169};

const Uint8 data1[] = {203, 50, 117, 147, 107, 207, 13, 145, 59, 21, 169, 23, 119, 210, 48, 104, 213, 151, 228, 219, 121, 134, 14, 122, 19, 111, 68, 63, 209, 135, 205, 137, 112, 29, 45, 233, 131, 238, 178, 187, 234, 188, 72, 201, 213, 50, 253, 202, 116, 182, 148, 172, 196, 135, 86, 145, 150, 145, 212, 144, 100, 180, 252, 73, 2, 176, 1, 208, 33, 211, 205, 27, 226, 216, 46, 76, 216, 7, 49, 165, 97, 14, 200, 19, 58, 208, 158, 64, 94, 197, 121, 206, 196, 222, 152, 214, 207, 115, 152, 27, 160, 158, 18, 5, 180, 23, 89, 64, 67, 26, 218, 9, 199, 50, 54, 213, 67, 198, 70, 141, 54, 93, 205, 190, 116, 58, 221, 121, 9, 195, 195, 197, 115, 28, 37, 77, 29, 239, 250, 37, 178, 123, 233, 38, 126, 54, 113, 237, 254, 49, 205, 131, 192, 0, 124, 130, 106, 33, 35, 132, 126, 133, 147, 236, 216, 225, 181, 11, 16, 226, 179, 195, 22, 180, 135, 131, 231, 55, 96, 193, 168, 197, 232, 194, 18, 11, 129, 65, 25, 124, 247, 21, 81, 159, 23, 178, 157, 126, 251, 242, 189, 141, 122, 232, 50, 159, 189, 203, 40, 102, 235, 51, 229, 217, 4, 154, 12, 245, 168, 52, 215, 232, 43, 141, 79, 67, 134, 131, 176, 246, 221, 53, 33, 125, 236, 132, 3, 187, 41, 121, 53, 242, 86, 120, 5, 21, 29, 99, 230, 99, 139, 10, 224, 199, 42, 84};

const Uint8 data2[] = {98, 155, 237, 30, 239, 101, 167, 59, 153, 183, 47, 147, 226, 123, 153, 193, 124, 52, 96, 82, 255, 44, 172, 216, 153, 238, 194, 187, 85, 46, 100, 32, 223, 186, 171, 109, 5, 104, 146, 199, 107, 163, 201, 79, 81, 108, 84, 99, 94, 48, 18, 140, 219, 6, 72, 237, 136, 237, 85, 207, 226, 158, 86, 230, 171, 154, 33, 207, 93, 204, 188, 99, 154, 198, 86, 83, 89, 33, 147, 140, 195, 128, 89, 13, 36, 161, 130, 49, 66, 180, 94, 177, 185, 69, 60, 116, 109, 215, 18, 140, 134, 130, 99, 25, 46, 141, 125, 63, 62, 103, 75, 173, 224, 19, 161, 243, 103, 183, 90, 23, 17, 245, 87, 193, 9, 71, 67, 221, 173, 127, 86, 81, 12, 109, 84, 60, 108, 125, 139, 178, 46, 6, 148, 130, 252, 75, 14, 146, 226, 64, 209, 242, 177, 113, 13, 8, 23, 92, 162, 38, 212, 160, 3, 192, 167, 144, 196, 122, 14, 254, 196, 191, 134, 56, 27, 2, 77, 20, 28, 227, 38, 76, 120, 82, 159, 158, 22, 209, 159, 250, 113, 178, 248, 188, 156, 56, 189, 238, 222, 214, 56, 146, 6, 105, 185, 25, 57, 68, 211, 235, 202, 177, 197, 165, 133, 230, 141, 116, 136, 186, 77, 110, 1, 36, 224, 105, 47, 163, 52, 214, 92, 180, 160, 93, 109, 2, 133, 52, 128, 208, 156, 93, 255, 209, 172, 156, 183, 229, 127, 226, 44, 129, 79, 104, 133, 251};

const Uint32 data3[] = {482, 482, 482, 481, 483, 494, 494, 494, 510, 510, 490, 483, 482, 482, 482, 482, 482, 482, 483, 482, 490, 494, 493, 510, 504, 501, 490, 483, 483, 482, 482, 482, 479, 482, 480, 483, 490, 491, 123, 505, 501, 126, 501, 484, 483, 122, 482, 482, 120, 480, 490, 123, 126, 501, 130, 517, 130, 517, 501, 122, 490, 120, 494, 479, 492, 123, 123, 126, 505, 126, 524, 519, 519, 130, 519, 126, 492, 124, 497, 124, 497, 494, 396, 128, 128, 524, 131, 524, 131, 524, 105, 509, 497, 496, 502, 497, 497, 502, 488, 400, 100, 131, 524, 131, 416, 416, 122, 509, 497, 497, 500, 502, 127, 125, 400, 100, 117, 524, 131, 416, 105, 430, 416, 509, 497, 497, 501, 502, 502, 451, 470, 483, 509, 524, 524, 524, 524, 491, 524, 400, 406, 497, 497, 502, 400, 497, 509, 509, 131, 524, 131, 524, 524, 524, 524, 496, 497, 497, 492, 497, 494, 97, 396, 109, 509, 524, 524, 524, 129, 131, 512, 505, 396, 384, 464, 492, 494, 120, 505, 115, 491, 500, 495, 495, 506, 493, 399, 396, 490, 490, 490, 493, 482, 122, 410, 452, 125, 495, 123, 124, 510, 129, 517, 501, 418, 490, 483, 481, 370, 373, 113, 451, 123, 517, 501, 517, 501, 501, 123, 382, 385, 380, 120, 482, 479, 109, 492, 123, 490, 123, 501, 501, 501, 125, 501, 490, 490, 474, 482, 482, 482, 479, 492, 492, 492, 490, 507, 499, 504, 501, 492, 490, 479, 479, 479, 479};

const Uint32 data4[] = {4294727324, 4294792337, 4294792337, 4294794887, 4294855546, 4294795142, 4294800244, 4294866029, 4294800744, 4294788463, 4294727324, 4294727324, 4294727324, 4294727324, 4294662570, 4294662570, 4294662570, 4294663589, 4294737801, 4294795163, 4294796672, 4294866544, 4294867563, 4294866288, 4294853785, 4294796672, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294802274, 4294796672, 4294867563, 4294867307, 4294866797, 4294867563, 4294731905, 4294731148, 4294727834, 4294729364, 4294729363, 4294733462, 4294664099, 4294663590, 4294734473, 4294663007, 4294800507, 4294802290, 4294801522, 4294867563, 4294867563, 4294797437, 4294855546, 4294796417, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4294793867, 4294858136, 4282392347, 4294867563, 4294867307, 4294866797, 4294802290, 4294800506, 4294789219, 4294734709, 4294735227, 4282329104, 4294752375, 4294739572, 4294739057, 4294683486, 4282328290, 4294738045, 4294737267, 4294934378, 4294802284, 4294802284, 4294867563, 4294796672, 4282396172, 4282324260, 4282324260, 4294792337, 4294792337, 4294792337, 4294791824, 4282324260, 4294797665, 4294800245, 4282391834, 4294867050, 4294867050, 4294867570, 4294802290, 4282326813, 4294731149, 4294794907, 4282334458, 4282319856, 4281925314, 4294681250, 4294680743, 4282378724, 4282327071, 4294738045, 4294802301, 4294737267, 4294867573, 4294802284, 4294867563, 4294867563, 4286735489, 4282259239, 4282324260, 4294792337, 4294792337, 4294792337, 4294792337, 4294792337, 4282392812, 4294867563, 4294867306, 4294867050, 4282391834, 4282326788, 4294737276, 4294802288, 4282326814, 4294802301, 4294722124, 4282375658, 4282327019, 4294737288, 4282375459, 4294754112, 4282375658, 4294737288, 4294738054, 4282259740, 4294802284, 4282588700, 4294867563, 4294867563, 4282391326, 4294727314, 4282324260, 4294792337, 4294791824, 4294791824, 4294791824, 4282324260, 4282584606, 4294867570, 4286675308, 4294801779, 4286675054, 4282246418, 4294805107, 4282327069, 4282311696, 4294805107, 4282326557, 4282375383, 4281867295, 4294671996, 4281917143, 4282326559, 4294671996, 4294671996, 4282375639, 4282259731, 4282326815, 4282588674, 4282326813, 4294802290, 4294730127, 4282324266, 4282324519, 4294727324, 4294791824, 4294792337, 4294792347, 4282324263, 4286676034, 4294867050, 4282392091, 4294933610, 4282392603, 4294754175, 4294737276, 4282326815, 4294754173, 4294737276, 4282327074, 4281868834, 4294738057, 4294738057, 4282327074, 4294673033, 4281868834, 4294738057, 4294738313, 4282376732, 4294788210, 4282456346, 4294867563, 4294933610, 4294731447, 4294727071, 4282258474, 4294792337, 4282322982, 4282324519, 4294791824, 4294792344, 4282202050, 4282326814, 4282326813, 4294802290, 4294754173, 4282327071, 4294738045, 4294738045, 4282327071, 4294673289, 4294543499, 4282198560, 4294543499, 4294543499, 4294673289, 4282327330, 4282327330, 4294673289, 4294673033, 4294737276, 4294754173, 4294805116, 4294737267, 4294802290, 4282321367, 4281866534, 4281866534, 4294662557, 4281932587, 4282257963, 4294727324, 4282259232, 4281866790, 4282193900, 4293356913, 4294738292, 4281869340, 4294738242, 4294673534, 4281869340, 4294738242, 4294871935, 4282327330, 4294673289, 4294673289, 4294673289, 4294543499, 4294543499, 4282198560, 4294543499, 4279882531, 4291255162, 4280734238, 4294670704, 4282376986, 4294737267, 4282322985, 4282330927, 4294727324, 4294727324, 4282324519, 4281866534, 4294792347, 4294597530, 4294791583, 4279646947, 4279902211, 4291275368, 4282326812, 4294738045, 4294738045, 4281869603, 4294738045, 4294673289, 4294543499, 4282262051, 4294543499, 4294543499, 4294673289, 4282132769, 4293425035, 4281405984, 4279690531, 4278963237, 4291728762, 4294738045, 4294737267, 4294738292, 4294740089, 4294658191, 4294598302, 4294598302, 4294662557, 4294727324, 4294662557, 4294791583, 4294662557, 4294343038, 4292963441, 4278960389, 4278372632, 4281472799, 4292832892, 4282263072, 4282262051, 4294543499, 4294543499, 4294543499, 4282262051, 4294214794, 4292571272, 4294292106, 4292062852, 4278897455, 4292702600, 4280559071, 4291400057, 4294673534, 4294738292, 4294737267, 4294737267, 4294742118, 4294662303, 4294662557, 4294598302, 4294598302, 4294727324, 4282261291, 4282325032, 4294010738, 4294016116, 4290927214, 4291386232, 4282196001, 4279565340, 4278646052, 4281933345, 4294543499, 4294543499, 4281999138, 4279159598, 4282194723, 4293042821, 4282133795, 4293557385, 4281934115, 4281998882, 4279957038, 4292306811, 4294673534, 4294738292, 4294738292, 4294738292, 4294668679, 4294667149, 4294598302, 4294662557, 4294662557, 4294598302, 4294598302, 4282325032, 4279971375, 4291838825, 4291711355, 4281341470, 4281472799, 4281216539, 4294476413, 4281345059, 4294543499, 4294543499, 4281476643, 4281800995, 4278503726, 4281023788, 4281473058, 4290861958, 4290926727, 4282323746, 4290943877, 4294673534, 4294673534, 4294738292, 4294738292, 4294738292, 4294738292, 4294594408, 4294598302, 4294598302, 4294598302, 4294662557, 4282325032, 4294660497, 4278790621, 4292231785, 4282323228, 4281341470, 4281604127, 4279250715, 4282063900, 4281345059, 4282262051, 4294543499, 4281476643, 4292761224, 4282134051, 4281733922, 4281341730, 4290861958, 4290926727, 4282323746, 4291930244, 4291583866, 4281932831, 4282327069, 4294738292, 4294738292, 4294738292, 4294742400, 4294599831, 4294598302, 4294598302, 4294598302, 4282325032, 4280686394, 4281341758, 4292897124, 4292372600, 4293753213, 4294937215, 4292590971, 4278439704, 4294029706, 4282262051, 4294543499, 4294029706, 4293836677, 4294291850, 4279222575, 4294412170, 4293491593, 4292102792, 4291718791, 4293425801, 4294348157, 4278439448, 4278910227, 4294738292, 4294738292, 4294738292, 4294670971, 4294658444, 4294598302, 4294598302, 4294598302, 4282325032, 4280762149, 4292242543, 4293228395, 4293439868, 4292324218, 4281604127, 4292964220, 4282061290, 4282262051, 4282262051, 4294543499, 4282262051, 4292308360, 4291584903, 4291190406, 4282259491, 4291930244, 4293239429, 4278385710, 4293491593, 4292635512, 4281932831, 4281476125, 4294738292, 4294738292, 4294738292, 4294738292, 4294809190, 4294599831, 4294662557, 4294598302, 4294598302, 4293022843, 4293375594, 4292649338, 4291978107, 4293753213, 4294673534, 4294673534, 4282134230, 4294543499, 4294543499, 4294543499, 4282262051, 4294543499, 4294543499, 4294543499, 4294412170, 4293425801, 4292636808, 4279028015, 4279698220, 4293636220, 4294213246, 4294476926, 4294738292, 4294738292, 4294738292, 4294737267, 4294676354, 4294726017, 4294598302, 4293414799, 4279176904, 4292374153, 4291466102, 4293292925, 4294673534, 4294673534, 4294673534, 4294673534, 4294543499, 4294543499, 4294543499, 4282262051, 4294543499, 4294543499, 4294543499, 4294543499, 4294543499, 4294543499, 4294543499, 4282262051, 4281258273, 4279617317, 4291734649, 4291452026, 4294738292, 4293225329, 4292238960, 4293889909, 4294738292, 4294605665, 4294662557, 4291517335, 4278257662, 4279372820, 4280476187, 4291189114, 4281604127, 4281669919, 4281998623, 4294673534, 4282262051, 4294543499, 4294543499, 4282262051, 4282262051, 4294543499, 4294543499, 4282262051, 4282262051, 4282262051, 4294543499, 4282262051, 4294478728, 4281869603, 4292906876, 4292437882, 4291318639, 4292519275, 4293496938, 4291252849, 4294737267, 4294730373, 4294728088, 4291646357, 4291579201, 4280428034, 4293883763, 4294938492, 4294871423, 4279225112, 4294086270, 4294673534, 4282327328, 4294541963, 4294541707, 4282262051, 4282262051, 4294543499, 4294541707, 4294544011, 4282262051, 4294478730, 4294673289, 4294410377, 4280795856, 4294424131, 4292256634, 4293834108, 4294417781, 4293031025, 4291250801, 4292238960, 4294802290, 4294799999, 4294663312, 4292430470, 4281930265, 4291124590, 4282195485, 4293288057, 4281537566, 4280750111, 4281340191, 4294738045, 4282260764, 4282323234, 4294539659, 4282260771, 4282326818, 4282326050, 4294664841, 4282325282, 4282178849, 4282262051, 4293882762, 4282326307, 4293877573, 4278895899, 4293883260, 4280690460, 4281533725, 4293945458, 4293685107, 4291057264, 4294737267, 4294737267, 4294729371, 4294727324, 4294202779, 4278792966, 4294013299, 4292655486, 4294675580, 4293822845, 4294347901, 4294673534, 4294724930, 4282249760, 4294679177, 4282187297, 4294596232, 4282253088, 4294541707, 4294594696, 4294543755, 4294673289, 4294673289, 4278501420, 4279512349, 4280427807, 4293554043, 4279056666, 4278594816, 4291714158, 4291976047, 4293751154, 4294802290, 4294802291, 4294725784, 4294792337, 4294726814, 4294801782, 4282195485, 4293039738, 4282314526, 4291671934, 4281932575, 4282327071, 4282324255, 4282325794, 4294537355, 4294602120, 4294668169, 4294667401, 4294667145, 4282326050, 4294737801, 4294673033, 4294738057, 4278926637, 4278795034, 4293545853, 4292100223, 4293948541, 4294606195, 4294408050, 4294802290, 4282326813, 4294867563, 4294799987, 4294793372, 4294727324, 4282259241, 4282320879, 4281997850, 4291994734, 4291541366, 4292716400, 4292436089, 4294754173, 4294735484, 4294736521, 4294733449, 4294666889, 4281866274, 4281866530, 4294733193, 4294737545, 4294674569, 4294673289, 4293752968, 4291209349, 4278661403, 4293346429, 4292691071, 4279516684, 4280352774, 4282194971, 4294867563, 4282129924, 4282588930, 4294794895, 4294727579, 4294791824, 4279633615, 4293946502, 4278396928, 4293749117, 4278594071, 4279382545, 4291660405, 4282327069, 4294803315, 4281863711, 4294673801, 4282327330, 4294726537, 4282380834, 4294674057, 4294666364, 4282376479, 4282326815, 4294737276, 4282114590, 4282259729, 4278333464, 4294207082, 4281011742, 4293748846, 4278463503, 4291514239, 4280026398, 4286676846, 4282331352, 4294792337, 4294662030, 4293733508, 4278931446, 4291773294, 4290986354, 4291315575, 4279050521, 4291588474, 4282326815, 4282259731, 4282261220, 4294742908, 4294723452, 4282332631, 4282381855, 4294742140, 4282325994, 4282376938, 4282327074, 4294738057, 4294738057, 4294802288, 4290924920, 4292180582, 4292560751, 4279772948, 4291314791, 4294082411, 4293874793, 4282388513, 4282324539, 4294792337, 4294660495, 4280970036, 4291771731, 4279175418, 4293676166, 4281602848, 4294013299, 4293421681, 4282326813, 4282326813, 4294802288, 4294738057, 4294722113, 4294722113, 4282376938, 4294738057, 4282326815, 4294737276, 4282326815, 4294737276, 4282326815, 4282326813, 4293948274, 4293089132, 4281533469, 4290468966, 4278988311, 4293680752, 4281154080, 4294793899, 4282324260, 4294792337, 4294660495, 4278419166, 4278222558, 4281733890, 4291974515, 4294464679, 4282333694, 4294798975, 4294867570, 4282129949, 4282326813, 4294802290, 4282326815, 4282326815, 4282326815, 4294737276, 4282326815, 4282326815, 4294737276, 4294737276, 4294737276, 4294802290, 4294867059, 4292698480, 4279054849, 4285806353, 4281664015, 4292428935, 4279045849, 4282324260, 4294791824, 4294791824, 4294792337, 4281996065, 4281930529, 4294594958, 4294792347, 4282325792, 4282324503, 4294787478, 4282134773, 4294861450, 4282324244, 4294930811, 4282259743, 4282259743, 4294802299, 4294802299, 4294737276, 4282326815, 4282326815, 4294737276, 4282259729, 4282326813, 4282326556, 4294866295, 4282319849, 4282594790, 4294525829, 4292894065, 4282126883, 4294791824, 4294792337, 4294792337, 4294791824, 4294792337, 4294792337, 4294792337, 4294792347, 4294792347, 4294794641, 4294798975, 4294867827, 4294856035, 4294794898, 4294858908, 4294791337, 4294791337, 4294794402, 4294793368, 4294730394, 4294731159, 4294731413, 4294731413, 4294731651, 4282334970, 4282331637, 4294859422, 4294789231, 4294867053, 4294797182, 4294792337, 4294792337, 4294792337, 4294791824, 4294792337};

Uint32 checkStrip(Uint8 *pixels, int x, int y, int width)
{
    Uint32 *p = (Uint32 *) pixels;
    Uint32 r = 0;
    for (int yy = y; yy < y + 3; yy++)
    {
        r ^= p[yy * width + x];
    }

    return r;
}

bool checkFlag(Uint8 *pixels, int width, int height)
{
    int i = 0;
    for (int y = 0; y < height; y += 2)
    {
        int yy = y;
        for (int x = (y / 2) % 2; x < width; x += 2)
        {
            yy++;
            if (yy % 2 == 0)
                yy -= 2;
            if (yy >= height)
                continue;

            Uint8 r = pixels[4 * (yy * width + x) + 2];
            Uint8 g = pixels[4 * (yy * width + x) + 1];
            Uint8 b = pixels[4 * (yy * width + x) + 0];
            if ((r ^ data0[i]) != data1[i] ||
                (g ^ data0[i]) != data2[i] ||
                (Uint32) r + (Uint32) g + (Uint32) b != data3[i])
                return false;

            i++;
        }
    }

    i = 0;
    for (int y = 0; y < height - 3 + 1; y++)
    {
        for (int x = 0; x < width; x++)
        {
            if (checkStrip(pixels, x, y, width) != data4[i])
                return false;
            i++;
        }
    }

    return true;
}