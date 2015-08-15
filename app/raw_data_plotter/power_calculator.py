__author__ = 'rezwan'
# # Going to calculate power curve from wind data
# # source from http://xn--drmstrre-64ad.dk/wp-content/wind/miller/windpower%20web/en/tour/wres/pow/index.htm
# # convert JS to Python
#
#############################Weibull calculator################
# fmW=this.document.forms.calcform.elements;
# function plotweibull(m,k){ // m is the mean value, c is the scale parameter, k is the shape parameter
# 	var c = m/gamma(1+1/k);
# 	var fi=0;
# 	var u=0;
# 	var uc=0;
# 	var ucik=0;
# 	var kc=k/c;
# 	var akk=0;
# 	var sw=true;
# 	var median=0;
# 	var buf="<img src='../../../../res/puax.gif'>";
# 	for (var i=0;i<270;i++){
# 		u=i*0.10;
# 		uc=u/c;
# 		ucik=Math.pow(uc,k-1);
# 		fi=kc*ucik*Math.exp(-ucik*uc);
# 		akk+=fi;
# 		if (sw && akk >= 5){
# 			buf+="<IMG SRC='../../../../res/blpix.gif' WIDTH=1 HEIGHT="+(1000*fi)+">";
# 			sw=false;
# 			median=u;
# 		}else{
# 			buf+="<IMG SRC='../../../../res/bluepix.gif' WIDTH=1 HEIGHT="+(1000*fi)+">";
# 		}
# 	}
# 	buf+="<BR><IMG SRC='../../../../res/msax.gif' USEMAP='#msax' ISMAP BORDER='0'>";
# 	var help=(0.01*Math.round(100*median)).toString();
# 	help=help.substring(0,help.indexOf(".")+3);
# 	buf+="<div style='font-size: 12px; font-family: gillsans,frutiger,helvetica,arial narrow,verdana,arial; color: black; margin-top: 4px; line-height: 13px; overflow: auto;'>"+iiScale+" A ="+0.01*Math.round(c*100)+"; "+iiShape+" k ="+k+"; "+iiMean+" = "+0.01*Math.round(100*(c*gamma(1+1/k)))+"; "+iiMedian+" = "+help+"<br>&copy; 2003 www.windpower.org</div>";
# 	writeToLayer("frame1",buf);
# }
# function redraw(){
# 	if (ijLangNo==0){
# 		var iiK="k skal være mellem 1 og 3.";
# 		var iiM1="Med så lav en vindhastighed behøver du ikke bekymre dig om vindmøller.";
# 		var iiM2="Vi har aldrig hørt om så høj en gennemsnitlig vindhastighed før. Send os en e-mail, og fortæl, hvor du har opdaget dette her sted!";
# 		var iiM3="Skalaparameteren er sikkert fortket, for en får en middelvindhastighed på "+mean+" m/s her!";
# 	}
# 	else if (ijLangNo==1){
# 		var iiK="k mu§ zwischen 1 und 3 liegen.";
# 		var iiM1="Bei derart geringen Windgeschwindigkeiten ist es nicht sinnvoll, eine Windkraftanlage aufzustellen.";
# 		var iiM2="Wir haben noch nie von einer so hohen durchschnittlichen Windgeschwindigkeit geh&ouml;rt. Bitte teilen Sie uns Ihren Standort per Email mit.";
# 		var iiM3="Das Skalierungsparameter ist wahrscheinlich falsch, weil Sie in diesem Fall eine durchschnittliche Windgeschwindigkeit von "+mean+" m/s erhalten w&uuml;rden!";
# 	}
# 	else if (ijLangNo==2){
# 		var iiK="k must be between 1 and 3.";
# 		var iiM1="With such a low wind speed, do not bother about wind turbines.";
# 		var iiM2="We have never heard about such a high average wind speed before, please send us an e-mail if you are serious!";
# 		var iiM3="Your scale parameter is probably wrong, because you get a mean wind speed of "+mean+" m/s on this site!";
# 	}
# 	else if (ijLangNo==3){
# 		var iiK="k s—lo puede tomar los valores 1 y 3.";
# 		var iiM1="Con una velocidad de viento tan baja no vale la pena que se preocupe por instalar un aerogenerador.";
# 		var iiM2="Nunca hemos oido hablar de una velocidad media del viento tan alta. Por favor, envie un e-mail si habla en serio!";
# 		var iiM3="Posiblemente su par‡metro de escala no sea el correcto, pues obtiene una velocidad media del viento de "+mean+" m/s en este emplazamiento.";
# 	}
# 	else if (ijLangNo==4){
# 		var iiK="k doit tre un chiffre entre 1 et 3";
# 		var iiM1="Avec une si faible vitesse moyenne du vent, cela ne vaut pas la peine d'installer des Žoliennes.";
# 		var iiM2="Nous n'avons jamais entendu parler d'une vitesse moyenne du vent si ŽlevŽe&nbsp;! Envoyez-nous un e-mail nous indiquant o se trouve cette localitŽ extraordinaire.";
# 		var iiM3="Le paramtre d'Žchelle n'est probablement pas correct si vous obtenez ici une vitesse moyenne de "+mean+" m/s&nbsp;!";
# 	}
# 	else if (ijLangNo==5){
# 		var iiK="-FI";
# 		var iiM1="-FI";
# 		var iiM2="-FI";
# 		var iiM3="-FI";
# 	}
# 	var mean = 0;
# 	var k = fmW.k.value;
# 	if (k<1 || k>3){
# 		alert(iiK);
# 		k = 2;
# 		fmW.k.value = k;
# 	}
# 	mean = fmW.mean.value;
# 	if (fmW.radio1[0].checked){
# 		if (mean<2){
# 			alert(iiM1);
# 			mean = 2;
# 			fmW.mean.value = mean;
# 		}
# 		if (mean>12){
# 			alert(iiM2);
# 			mean = 12;
# 			fmW.mean.value = mean;
# 		}
# 	}
# 	else{
# 		mean = mean*gamma(1+1/k);
# 		if (mean<2 || mean>12) alert(iiM3);
# 	}
# 	plotweibull(mean,k);
# }

#######################gamma calculation
# function gamma(lambda)
# {
# 	var e = Math.floor(lambda);
# 	if (0>=e) return (Number.NaN);
# 	var v = 0;
# 	var i = 0;
# 	var x = 0;
# 	var g = new Array(1,0.9943,0.9888,0.9835,0.9784,0.9735,0.9687,0.9642,0.9597,0.9555,0.9514,0.9474,0.9436,0.9399,0.9364,0.9330,0.9298,0.9267,0.9237,0.9209,0.9182,0.9156,0.9131,0.9108,0.9085,0.9064,0.9044,0.9025,0.9007,0.8990,0.8975,0.8960,0.8946,0.8934,0.8922,0.8912,0.8902,0.8893,0.8885,0.8879,0.8873,0.8868,0.8864,0.8860,0.8858,0.8857,0.8856,0.8856,0.8857,0.8859,0.8862,0.8866,0.8870,0.8876,0.8882,0.8889,0.8896,0.8905,0.8914,0.8924,0.8935,0.8947,0.8959,0.8972,0.8986,0.9001,0.9017,0.9033,0.9050,0.9068,0.9086,0.9106,0.9126,0.9147,0.9168,0.9191,0.9214,0.9238,0.9262,0.9288,0.9314,0.9341,0.9368,0.9397,0.9426,0.9456,0.9487,0.9518,0.9551,0.9584,0.9618,0.9652,0.9688,0.9724,0.9761,0.9799,0.9837,0.9877,0.9917,0.9958,1);
# 	if (e>=1) {v=1; for (i=e;i>0;i--) v=v*i;}
# 	lambda-=e;
# 	x=lambda/0.01;
# 	i=Math.floor(x);
# 	return(v*g[i]);
# }
#
###############################################Full calculator
# // Copyright 1998 S¿ren Krohn & DWIA
# iiForm=document.forms.calcform.elements;
# p0=101.325; // Standard atmospheric pressure in kPa
# R=286.9; // Gas constant in J/kg K
# T0=273.15; // 0° C in °K
# beta=0.0065; // Lapse rate in °K/m altitude
# g=9.80665; // Normal gravitational acceleration at sea level m/s2
# turbines=new Turbines("turb");
# sites=new Sites("site");
# gWindow=null;
# gPowden=null;
# gProd=null;
#
# new Site("Melsbroek (B)",50,8.6,2,7.1,1.94,6.5,1.92,5.6,1.89);
# new Site("Middelkerke (B)",50,9.7,2.18,7.9,2.09,7.3,2.06,6.3,2.03);
# new Site("Berlin (D)",50,8.4,2.45,6.9,2.37,6.3,2.33,5.5,2.27);
# new Site("Frankfurt (D)",50,7.1,2.07,5.8,1.99,5.3,1.96,4.6,1.92);
# new Site("Helgoland (D)",50,9.5,2.26,7.8,2.18,7.1,2.13,6.2,2.08);
# new Site("Beldringe (DK)",50,9.5,2.12,7.7,2.03,7.1,1.99,6.1,1.96);
# new Site("Karup (DK)",50,11,2.31,9,2.2,8.2,2.17,7.1,2.13);
# new Site("Kastrup (DK)",50,10.4,2.49,8.5,2.38,7.8,2.35,6.7,2.29);
# new Site("Albacete (E)",50,9.7,1.60,7.8,1.52,7.1,1.5,6.2,1.51);
# new Site("Menorca (E)",50,9.4,1.56,7.6,1.52,7,1.5,6,1.49);
# new Site("Brest (F)",50,9.9,2.15,8.1,2.06,7.4,2.03,6.4,2.01);
# new Site("Carcassonne (F)",50,11,2.18,9,2.09,8.2,2.07,7.1,2.06);
# new Site("Bala, Wales (GB)",50,10.1,1.63,8.2,1.58,7.5,1.58,6.5,1.65);
# new Site("Dustaffnage, Scotland (GB)",50,10.2,2.03,8.3,1.96,7.6,1.94,6.6,1.92);
# new Site("Stornoway (GB)",50,11,1.94,9,1.87,8.3,1.86,7.2,1.83);
# new Site("Araxos (GR)",50,8.7,1.4,6.9,1.33,6.3,1.33,5.5,1.33);
# new Site("Heraklion (GR)",50,7.9,1.25,6.5,1.22,5.9,1.22,5.2,1.22);
# new Site("Brindisi (I)",50,8.9,1.59,7.2,1.53,6.6,1.52,5.8,1.51);
# new Site("Trapani, Sicily (I)",50,8.7,1.41,7.1,1.37,6.5,1.37,5.6,1.36);
# new Site("Cork (IRL)",50,10,2.07,8.2,1.99,7.5,1.96,6.5,1.94);
# new Site("Malin Head (IRL)",50,11.5,2.13,9.4,2.04,8.6,2.03,7.5,2.01);
# new Site("Findel (L)",50,8.1,2.16,6.7,2.08,6.1,2.05,5.3,2.01);
# new Site("Schipol (NL)",50,9.4,2.31,7.7,2.21,7,2.19,6.1,2.14);
# new Site("Texel Lichtschip (NL)",50,9.4,2.08,7.7,1.99,7,1.97,6.1,1.94);
# new Site("Flores, Açôres (P)",50,9.6,1.62,7.8,1.56,7.1,1.55,6.2,1.54);
# new Site("Lisboa (P)",50,9.4,2.15,7.7,2.09,7,2.06,6.1,2.03);
#
# iota30=new Array(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30);
#
# // pTurbineName is the power curve in kW from 1 to 30 m/s
# // h TurbineName are the availble tower heights in m
# // TurbinenName contains ("name in popup",rotorDiameter,kWlargeGenerator,kWsmallGenerator,startSpeed,stopSpeed,towerHeightName,powerCurveName,vectorWithWindSpeedsForPowerCurve);
#
# pExample=new Array(0,0,2,17,45,72,124,196,277,364,444,533,584,618,619,618,619,620,610,594,592,590,580,575,570,0,0,0,0,0);
# hExample=new Array(50,30,40,50,60,70);
# Example=new Turbine("User Example",43,600,125,5,25,hExample,pExample, iota30);
#
# pBonus_300=new Array(0,0,3.9,15.4,32,52,87.1,129,171.9,211.6,250.6,280.7,297.2,304.5,299.7,281.3,271.3,259.5,254.7,252.9,254,254.9,255.8,256.7,257.5,0,0,0,0,0);
# hBonus_300=new Array(30,40);
# Bonus_300=new Turbine("Bonus 300/33.4 Mk III",33.4,300,0,3,25,hBonus_300,pBonus_300, iota30);
#
# pBonus_600=new Array(0,0,3.9,21.2,49.3,83.2,130.7,202,280.8,361.3,433.7,498.6,548.1,577.3,596,610,606.9,593.4,571.3,545.6,524.7,510,500.7,478.7,457.7,0,0,0,0,0);
# hBonus_600=new Array(35,40,45,50,55,60);
# Bonus_600=new Turbine("Bonus 600/44 Mk IV",44,600,150,3,25,hBonus_600,pBonus_600, iota30);
#
# pBonus_1000=new Array(0,0,0,13,55,116.1,204,317.4,444.7,583.1,715.6,822.1,906.8,963.7,991,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,0,0,0,0,0);
# hBonus_1000=new Array(45,50,60,70);
# Bonus_1000=new Turbine("Bonus 1000/54",54,1000,200,3,25,hBonus_1000,pBonus_1000, iota30);
#
# pBonus_1300=new Array(0,0,0,32.1,91.6,172.5,291.2,439.3,604.3,770.6,928.7,1072.2,1183.1,1250.1,1281.7,1294,1298.2,1299.5,1299.8,1300,1300,1300,1300,1300,1300,0,0,0,0,0);
# hBonus_1300=new Array(45,68);
# Bonus_1300=new Turbine("Bonus 1300/62",62,1300,250,4,25,hBonus_1300,pBonus_1300,iota30);
#
# pBonus_2000=new Array(0,0,0,43,133,237,401,623,886,1190,1502,1740,1891,1962,1988,1996,1999,2000,2000,2000,2000,2000,2000,2000,2000,0,0,0,0,0);
# hBonus_2000=new Array(60,80);
# Bonus_2000=new Turbine("Bonus 2000/76",76,2000,400,4,25,hBonus_2000,pBonus_2000,iota30);
#
# pBonus_2300=new Array(0,0,0,52,148,288,476,729,1055,1419,1769,2041,2198,2267,2291,2298,2300,2300,2300,2300,2300,2300,2300,2300,2300,0,0,0,0,0);
# hBonus_2300=new Array(60,80);
# Bonus_2300=new Turbine("Bonus 2300/82.4",82.4,2300,400,3,25,hBonus_2300,pBonus_2300,iota30);
#
# pMicon_72_2000_500=new Array(0,0,0,54.9,185.3,369.4,618.8,941.4,1326.1,1741.3,2132.9,2435.5,2616.9,2701.8,2733.8,2744.1,2747.2,2748.0,2748.3,2750.0,2750.0,2750.0,2750.0,2750.0,2750.0,0,0,0,0,0);
# hMicon_72_2000_500=new Array(70,77.6);
# Micon_72_2000_500=new Turbine("NEG Micon 2750/92",92,2750,0,3,25,hMicon_72_2000_500,pMicon_72_2000_500,iota30);
#
# pMicon_72_2000_500=new Array(0,0,0,17.8,118.4,257.8,447.3,693.2,997.7,1345.0,1708.0,2055.4,2349.8,2554.2,2667.4,2718.5,2738.2,2745.1,2747.3,2750.0,2750.0,2750.0,2750.0,2750.0,2750.0,0,0,0,0,0);
# hMicon_72_2000_500=new Array(60,70,80);
# Micon_72_2000_500=new Turbine("NEG Micon 2750/80",80,2750,0,3,25,hMicon_72_2000_500,pMicon_72_2000_500,iota30);
#
# pMicon_72_2000_500=new Array(0,0,0,36,124,226,368,580,811,1103,1370,1633,1855,1945,1988,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,0,0,0,0,0);
# hMicon_72_2000_500=new Array(64,85);
# Micon_72_2000_500=new Turbine("NEG Micon 2000/72",72,2000,500,3,25,hMicon_72_2000_500,pMicon_72_2000_500,iota30);
#
# pMicon_M1500_750=new Array(0,0,0,48,124,223,356,576,808,1058,1285,1426,1451,1480,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,0,0,0,0,0);
# hMicon_M1500_750=new Array(62,70,78,80);
# Micon_M1500_750=new Turbine("NEG Micon 1500/72 50 Hz",72,1500,400,3,25,hMicon_M1500_750,pMicon_M1500_750, iota30);
#
# pMicon_M1500_750_60=new Array(0,0,0,0,74,202,356,576,808,1058,1285,1426,1451,1483,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,0,0,0,0,0);
# hMicon_M1500_750_60=new Array(62,70,78,80);
# Micon_M1500_750_60=new Turbine("NEG Micon 1500/72 60 Hz",72,1500,0,4,25,hMicon_M1500_750_60,pMicon_M1500_750_60, iota30);
#
# pNordtank_1500_64=new Array(0,0,0,9,63,159,285,438,615,812,1012,1197,1340,1437,1490,1497,1491,1449,1413,1389,1359,1329,1307,1288,1271,0,0,0,0,0);
# hNordtank_1500_64=new Array(60,68);
# Nordtank_1500_64=new Turbine("NEG Micon 1500/64",64,1500,0,4,25,hNordtank_1500_64,pNordtank_1500_64,iota30);
#
# pMicon_M2300_1000=new Array(0,0,0,10,51,104,186,291,412,529,655,794,911,986,1006,998,984,971,960,962,967,974,980,985,991,0,0,0,0,0); //NEW
# hMicon_M2300_1000=new Array(1); hMicon_M2300_1000[0]=59;
# Micon_M1500_1000=new Turbine("NEG Micon 1000/54",54,1000,250,3.5,25,hMicon_M2300_1000,pMicon_M2300_1000,iota30);
#
# pNM1000_60=new Array(0,0,0,33,86,150,248,385,535,670,780,864,924,964,989,1000,998,987,968,944,917,889,863,840,822,0,0,0,0,0); //NEW
# hNM1000_60=new Array(1); hNM1000_60 [0]=59;
# NM1000_60=new Turbine("NEG Micon 1000/60",60,1000,250,3.5,20,hNM1000_60, pNM1000_60, iota30);
#
# pMicon_52_900=new Array(0,0,0,27,67,117,199,303,420,541,644,732,801,849,880,894,900,897,892,887,883,880,879,881,884,0,0,0,0,0); //NEW
# hMicon_52_900=new Array(44,49,55,60,72.3);
# Micon_52_900=new Turbine("NEG Micon 900/52",52,900,0,3,25,hMicon_52_900,pMicon_52_900,iota30);
#
# pMicon_M1500_750_48m=new Array(0,0,0,13,48,95,168,259,362,472,576,662,724,755,742,691,637,600,581,573,571,573,580,590,604,0,0,0,0,0); //NEW
# hMicon_M1500_750_48m=new Array(40,45,46,50,52,56.5);
# Micon_M1500_750_48m=new Turbine("NEG Micon 750/48",48,750,175,4,25,hMicon_M1500_750_48m,pMicon_M1500_750_48m, iota30);
#
# pMicon_M1500_750=new Array(0,0,0,5,33,71,128,201,287,377,460,555,645,712,743,752,748,732,713,706,706,711,710,709,706,0,0,0,0,0); //NEW
# hMicon_M1500_750=new Array(40,45,46,50,52,56.5);
# Micon_M1500_750=new Turbine("NEG Micon 750/44 50 Hz",44,750,175,4,25,hMicon_M1500_750,pMicon_M1500_750, iota30);
#
# pMicon_M1500_750_60=new Array(0,0,0,9.2,31.5,60.3,95.5,153.2,221.5,300.1,384.9,468.7,554.1,633.1,691.6,717.3,723.6,726.5,723.8,717.6,709.5,700.7,691.2,683.3,678.7,0,0,0,0,0); //NEW
# hMicon_M1500_750_60=new Array(40,45,46,50,52,56.5);
# Micon_M1500_750_60=new Turbine("NEG Micon 750/44 60 Hz",44,750,175,4,25,hMicon_M1500_750_60,pMicon_M1500_750_60, iota30);
#
# pMicon_M1500_600=new Array(0,0,0,7.1,35.2,71.6,125,197.5,280.5,355.1,439.1,518.7,574.9,596.4,600.3,589.8,571.9,559.7,553.9,555.1,553.3,549.7,544.3,539.9,537.5,0,0,0,0,0); //NEW
# hMicon_M1500_600=new Array(40,46);
# Micon_M1500_600=new Turbine("NEG Micon 600/43",43,600,150,4,25,hMicon_M1500_600,pMicon_M1500_600, iota30);
#
# pMicon_M1800_600=new Array(0,0,5,26,52,93,153,235,329,424,500,557,607,631,645,645,635,625,615,605,0,0,0,0,0,0,0,0,0,0); //NEW
# hMicon_M1800_600=new Array(1); hMicon_M1800_600[0]=46;
# Micon_M1800_600=new Turbine("NEG Micon 600/48",48,600,150,4,25,hMicon_M1800_600,pMicon_M1800_600, iota30);
#
# pMicon_M1500_500=new Array(0,0,0.2,13.9,41.4,66.5,121.4,192.6,265.0,345.7,414.5,471.7,512.7,525.5,523.1,517.7,508.0,489.9,484.2,484.2,484.2,484.2, 484.2,484.2,484.2,0,0,0,0,0);
# hMicon_M1500_500=new Array(40,46);
# Micon_M1500_500=new Turbine("NEG Micon 500/43",43,500,125,3,25, hMicon_M1500_500, pMicon_M1500_500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,70,183,340,563,857,1225,1607,1992,2208,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,2300,0,0,0,0,0);
# hNordex_N80_2500=new Array(80,100,105);
# Nordex_N80_2500=new Turbine("Nordex N90/2300",90,2300,0,3,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,15,120,248,429,662,964,1306,1658,1984,2264,2450,2450,2470,2500,2500,2500,2500,2500,2500,2500,2500,2500,0,0,0,0,0);
# hNordex_N80_2500=new Array(60,80,100,105);
# Nordex_N80_2500=new Turbine("Nordex N80/2500",80,2500,0,4,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,25,87,214,377,589,855,1162,1453,1500,1500,1500,1500,1500,1500,1500,1500,1500,0,0,0,0,0,0,0,0,0,0);
# hNordex_N80_2500=new Array(61.5,85,90,96.5,100,111.5);
# Nordex_N80_2500=new Turbine("Nordex S77/1500",77,1500,0,3,20,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,24,86,188,326,526,728,1006,1271,1412,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,0,0,0,0,0);
# hNordex_N80_2500=new Array(65,85,98,114.5);
# Nordex_N80_2500=new Turbine("Nordex S70/1500",70,1500,0,3,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,20,81,159,225,385,571,760,925,1056,1168,1250,1294,1300,1287,1262,1232,1203,1179,1158,1146,1140,1138,0,0,0,0,0);
# hNordex_N80_2500=new Array(60,69);
# Nordex_N80_2500=new Turbine("Nordex N62/1300",62,1300,250,3,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,29,73,131,240,376,536,704,871,1016,1124,1247,1301,1344,1364,1322,1319,1314,1312,1307,1299,1292,1292,0,0,0,0,0);
# hNordex_N80_2500=new Array(46,60,65,69,85);
# Nordex_N80_2500=new Turbine("Nordex N60/1300",60,1300,250,3,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N54_1000=new Array(0,0,0,14,51,105,179,297,427,548,697,794,885,999,1082,1090,1086,1033,1025,1021,1011,1000,990,980,970,0,0,0,0,0);
# hNordex_N54_1000=new Array(50,60,70);
# Nordex_N54_1000=new Turbine("Nordex N54/1000",54,1000,200,4,25,hNordex_N54_1000,pNordex_N54_1000, iota30);
#
# pNordex_N80_2500=new Array(0,0,0,23,57,90,165,257,359,470,572,668,747,805,838,842,840,827,808,785,757,728,743,742,745,0,0,0,0,0);
# hNordex_N80_2500=new Array(46,50,70);
# Nordex_N80_2500=new Turbine("Nordex N50/800",50,800,200,3,25,hNordex_N80_2500,pNordex_N80_2500, iota30);
#
# pNordex_N43_600=new Array(0,0,2,17,45,72,124,196,277,364,444,533,584,618,619,618,619,620,610,594,592,590,580,575,570,0,0,0,0,0);
# hNordex_N43_600=new Array(40,46,50,60);
# Nordex_N43_600=new Turbine("Nordex N43/600",43,600,125,3,25,hNordex_N43_600,pNordex_N43_600, iota30);
#
# pNordex_N29_250=new Array(0,0,2,12,24,35,58,95,128,161,190,213,225,234,245,254,261,265,271,267,263,259,253,248,245,0,0,0,0,0);
# hNordex_N29_250=new Array(30,40,50);
# Nordex_N29_250=new Turbine("Nordex N29/250",29,250,45,4,25,hNordex_N29_250,pNordex_N29_250, iota30);
#
# pNordex_N27_150=new Array(0,0,0,8,19,31,55,83,110,136,160,170,176,180,175,172,164,155,150,145,145,140,135,130,130,0,0,0,0,0);
# hNordex_N27_150=new Array(30,40,50);
# Nordex_N27_150=new Turbine("Nordex N27/150",27,150,30,3,25,hNordex_N27_150,pNordex_N27_150, iota30);
#
# pVestas_2000_80=new Array(0,0,0,44.1,135,261,437,669,957,1279,1590,1823,1945,1988,1998,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,0,0,0,0,0);
# hVestas_2000_80=new Array(80,80);
# Vestas_2000_80=new Turbine("Vestas V80 2000/80 onshore",80,2000,0,4,25,hVestas_2000_80,pVestas_2000_80,iota30);
#
# pVestas_2000_66=new Array(0,0,0,33.4,94.3,178,294,451,655,901,1169,1433,1667,1843,1943,1985,1997,2000,2000,2000,2000,2000,2000,2000,2000,0,0,0,0,0);
# hVestas_2000_66=new Array(66,66);
# Vestas_2000_66=new Turbine("Vestas V66 2000/66 offshore",66,2000,0,4,25,hVestas_2000_66,pVestas_2000_66,iota30);
#
# pVestas_1750_66=new Array(0,0,0,33.3,93.9,178,294,452,655,900,1167,1418,1603,1702,1739,1748,1750,1750,1750,1750,1750,1750,1750,1750,1750,0,0,0,0,0);
# hVestas_1750_66=new Array(66,66);
# Vestas_1750_66=new Turbine("Vestas V66 1750/66",66,1750,0,4,25,hVestas_1750_66,pVestas_1750_66,iota30);
#
# pVestas_1650_66=new Array(0,0,0,15.2,79.3,167,286,445,640,854,1064,1258,1425,1549,1616,1641,1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650,0,0,0,0,0);
# hVestas_1650_66=new Array(60,67,80);
# lVestas_1650_66=new Array(0,0,0,15.2,79.3,167,286,445,640,854,1064,1258,1425,1549,1616,1641,1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650,0,0,0,0,0); // NB NOT UPDATED!!!
# Vestas_1650_66=new Turbine("Vestas V66 1650/66",66,1650,300,4.5,25,hVestas_1650_66,pVestas_1650_66,iota30, lVestas_1650_66);
#
# pVestas_850_52=new Array(0,0,0,25.5,67.4,125,203,304,425,554,671,759,811,836,846,849,850,850,850,850,850,850,850,850,850,0,0,0,0,0);
# hVestas_850_52=new Array(44,49,55,60,65);
# Vestas_850_52=new Turbine("Vestas V52 850/52",52,850,0,4,25,hVestas_850_52,pVestas_850_52,iota30);
#
# pVestas_660_200_47=new Array(0,0,0,5.3,44.9,95.4,161,242,334,426,511,577,620,644,654,658,660,660,660,660,660,660,660,660,660,0,0,0,0,0);
# hVestas_660_200_47=new Array(40,45,50,55,60,65);
# lVestas_660_200_47=new Array(0,0,0,0.8,35.2,79,136,206,285,366,446,519,578,619,642,653,658,659,660,660,660,660,660,660,660,0,0,0,0,0);
# Vestas_660_200_47=new Turbine("Vestas V47 660-200/47",47,660,200,3.5,25,hVestas_660_200_47,pVestas_660_200_47, iota30, lVestas_660_200_47);
#
# pVestas_660_47=new Array(0,0,0,2.9,43.8,96.7,166,252,350,450,538,600,635,651,657,659,660,660,660,660,660,660,660,660,660,0,0,0,0,0);
# hVestas_660_47=new Array(40,45,50,55);
# lVestas_660_47=new Array(0,0,0,0.6,36.2,81.8,141,215,300,392,480,554,607,637,652,657,659,660,660,660,660,660,660,600,660,0,0,0,0,0);
# Vestas_660_47=new Turbine("Vestas V47 660/47",47,660,0,4,25,hVestas_660_47,pVestas_660_47, iota30, lVestas_660_47);
#
# pVestas_600_44=new Array(0,0,0,0,30.4,77.3,135,206,287,371,450,514,558,582,594,598,600,600,600,600,0,0,0,0,0,0,0,0,0,0);
# hVestas_600_44=new Array(35,40,45,50,55);
# lVestas_600_44=new Array(0,0,0,0,24.7,65.2,115,176,246,320,393,461,517,557,581,593,598,599,600,600,0,0,0,0,0,0,0,0,0,0);
# Vestas_600_44=new Turbine("Vestas V44 600/44",44,600,0,4,20,hVestas_600_44,pVestas_600_44, iota30, lVestas_600_44);
#
# pVestas_600_42=new Array(0,0,0,0,21.5,65.2,120,188,268,356,440,510,556,582,594,598,600,600,600,600,600,600,600,600,600,0,0,0,0,0);
# hVestas_600_42=new Array(35,40,45,50,55);
# lVestas_600_42=new Array(0,0,0,0,17,54.7,102,160,230,308,386,460,519,560,583,594,598,599,600,600,600,600,600,600,600,0,0,0,0,0);
# Vestas_600_42=new Turbine("Vestas V42 600/42",42,600,0,4,25,hVestas_600_42,pVestas_600_42, iota30, lVestas_600_42);
#
# pVestas_600_39=new Array(0,0,0,0,18.9,57.4,106,166,239,320,402,476,532,568,587,595,599,600,600,600,600,600,600,600,600,600,600,600,600,600);
# hVestas_600_39=new Array(35,40,45,50,55);
# lVestas_600_39= new Array(0,0,0,0,14.8,48,89.4,141,204,274,348,418,481,531,565,584,594,598,600,600,600,600,600,600,600,600,600,600,600,600); // density 1.06 kg/m3
# Vestas_600_39=new Turbine("Vestas V39 600/39",39,600,0,4,30,hVestas_600_39,pVestas_600_39, iota30, lVestas_600_39);
#
# pVestas_225_29=new Array(0,0,2.1,7.1,20.5,38.3,61.9,92.2,127.9,164.9,196.4,215.5,222.9,225,225,225,225,225,225,225,225,225,225,225,225,0,0,0,0,0);
# mVestas_225=new Array(1,2,3.5,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30);
# hVestas_225_29=new Array(0); hVestas_225_29[0]=31.5;
# lVestas_225_29=new Array(0,0,1,5.6,17.2,32.7,53.2,79.3,110,142,174,200,216,223,225,225,225,225,225,225,225,225,225,225,225, 0,0,0,0,0);
# Vestas_225_29=new Turbine("Vestas V29 225/29",29,225,50,3.5,25,hVestas_225_29,pVestas_225_29, mVestas_225, lVestas_225_29);
#
# pVestas_225_27=new Array(0,0,1.5,4.5,16.6,31.8,52.5,82.4,114.5,148.3,181,205,217.6,225,225,225,225,225,225,225,225,225,225,225,225,0,0,0,0,0);
# hVestas_225_27=new Array(1); hVestas_225_27[0]=31.5;
# Vestas_225_27=new Turbine("Vestas V27 225/27",27,225,50,3.5,25,hVestas_225_27,pVestas_225_27, mVestas_225);
#
# pWindWorld_750_52=new Array("no","data",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
# hWindWorld_750_52=new Array(50,65);
# WindWorld_750_52=new Turbine("Wind World 750/52",52,750,0,2.5,25,hWindWorld_750_52,pWindWorld_750_52, iota30);
#
# pWindWorld_750_48=new Array(0,0,0,16.93,46.36,90.75,152.93,235.59,340.63,458.44,568.09,651.11,711.95,747.09,764.42,769,762.12,750.22,736.06,721.53,708.14,697.49,691.63,690.67,692.79,0,0,0,0,0);
# hWindWorld_750_48=new Array(50,65);
# WindWorld_750_48=new Turbine("Wind World 750/48",48,750,0,2.5,25,hWindWorld_750_48,pWindWorld_750_48, iota30);
#
# pWindWorld_600=new Array(0,0,0,0,11.9,56.9,114.6,186.1,268.5,342.3,429.3,510.9,572,597.5,601,592.8,578.5,567.4,570.4,577.8,0,0,0,0,0,0,0,0,0,0);
# hWindWorld_600=new Array(40,43.5,48,62.5);
# WindWorld_600=new Turbine("Wind World 600/42",42,600,0,2.5,20,hWindWorld_600,pWindWorld_600, iota30);
#
# pWindWorld_550=new Array(0,0,0,0,17.4,50.3,92.4,144.4,205,273.2,346.1,415.7,476.1,517.6,542.3,550.7,541.9,517.9,484.5,468.6,462.2,464.3,470.3,483.1,0,0,0,0,0,0);
# hWindWorld_550=new Array(35,40);
# WindWorld_550=new Turbine("Wind World 550/37.3",37.3,550,0,4.5,23,hWindWorld_550,pWindWorld_550, iota30);
#
# pWindWorld_250=new Array(0,0,0,0,12.05,32.91,59.87,91.95,123.94,152.81,180.41,204.9,224.24,238.04,247.11,253.41,258.18,260.29,259.37,255.58,249.71,243.02,236.27,230.09,224.41,0,0,0,0,0);
# hWindWorld_250=new Array(31.5,41.5);
# WindWorld_250=new Turbine("Wind World 250/29.2",29.2,250,0,3.5,25,hWindWorld_250,pWindWorld_250, iota30);
#
# pWindWorld_170=new Array(0,0,0,0,2.33,8.33,15.55,25.03,35.2,50.51,69,87,100.94,113.91,128,138.78,146.55,152.13,156,161,164,169,173,177.73,179.1,177,172.8,166.77,162.4,161);
# mWindWorld_170=new Array(1,2,3,4,4.75,5.24,5.7,6.28,6.74,7.29,8.29,8.78,9.24,9.76,10.72,11.24,11.71,12.23,12.72,13.22,13.73,14.1,14.75,15.23,15.73,16.74,17.24,17.65,19,25);
# hWindWorld_170=new Array(31.5,41.5);
# WindWorld_170=new Turbine("Wind World 170/27",27,170,0,4,25,hWindWorld_170,pWindWorld_170, mWindWorld_170);
#
# pNordtank_55=new Array(0,0,0,1.93,4.95,8.05,16.85,24.91,30.72,36.64,44.16,48.2,51.91,53.93,55.86,58.04,58.14,60.16,60.24,61.23,61.85,62.88,63.69,63.69,0,0,0,0,0,0);
# mNordtank_55=new Array(1,2,3,4.01,4.98,5.99,7,8.01,8.96,9.99,10.98,12,12.97,14,14.94,16.04,17.01,18.1,19,19.98,20.97,22.03,23.04,25,26,27,28,29,30,31);
# hNordtank_55=new Array(0); hNordtank_55[0]=22;
# Nordtank_55=new Turbine("(1980: Nordtank 55/10)",15,55,11,3,25,hNordtank_55,pNordtank_55,mNordtank_55);
#
# pNordtank_30=new Array(0,0,0,0.11,0.9,2.83,5.44,9.52,14.53,18.41,23.42,26.80,29.81,30.31,30.68,27.18,30.18,31.19,31.19,0,0,0,0,0,0,0,0,0,0,0);
# mNordtank_30=new Array(1,2,2.63,3.93,4.95,5.98,7.03,8.03,9.24,10.23,11.21,12.29,13.47,14.55,15.63,16.71, 17.79,19.08,25,26,27,28,29,30,31,32,33,34,35,36);
# hNordtank_30=new Array(0); hNordtank_30[0]=20.5;
# Nordtank_30=new Turbine("(1980: Nordtank 30/7.5)",11,30,7.5,3,25,hNordtank_30,pNordtank_30,mNordtank_30);
#
# pNordtank_22=new Array(0,0,0,0.09,0.72,2.26,4.34,7.6,11.6,14.7,18.7,21.4,23.8,24.2,24.5,21.7,24.1,24.9,24.9,0,0,0,0,0,0,0,0,0,0,0);
# mNordtank_22=new Array(1,2,2.44,3.65,4.59,5.55,6.52,7.45,8.57,9.49,10.4,11.4,12.5,13.5,14.5,15.5, 16.5,17.7,25,26,27,28,29,30,31,32,33,34,35,36);
# hNordtank_22=new Array(0); hNordtank_22[0]=20.5;
# Nordtank_22=new Turbine("(1980: Nordtank 22/7.5)",11,22,7.5,3,25,hNordtank_22,pNordtank_22,mNordtank_22);
#
# pVestas_55=new Array(0,0,0,0.38,2.15,6.2,12.8,20,27.9,35.8,43.8,49.9,53.8,58.2,61.7,63.8,63.8,0,0,0,0,0,0,0,0,0,0,0,0,0); // Coronet blades
# mVestas_55=new Array(1,2,2.32,3.51,4.52,5.56,6.52,7.53,8.49,9.5,10.5,11.5,12.6,13.6,14.4,15.4,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39);
# hVestas_55=new Array(0); hVestas_55[0]=18;
# Vestas_55=new Turbine("(1980: Vestas 55/7.5)",15,55,7.5,3,25,hVestas_55,pVestas_55,mVestas_55);
#
# pKuriant_15=new Array(0,0,0,0.04,0.62,1.66,3.74,6.17,8.76,11.01,12.49,13.75,15.01,16.03,16.6,17.35,17.6,18.6,19,19.7,20.3,20.8,21.4,22.4,22.4,22.4,0,0,0,0);
# mKuriant_15=new Array(1,2,2.6,3.5,4.6,5.5,6.5,7.5,8.5,9.4,10.5,11.5,12.4,13.5,14.4,15,16,17.4,18.4,19.4,20.3,21.2,22.4,23.2,24,25,27,28,29,30);
# hKuriant_15=new Array(0); hKuriant_15[0]=18;
# Kuriant_15=new Turbine("(1980: Kuriant 15/4)",10.9,15,4,3,25,hKuriant_15,pKuriant_15,mKuriant_15);
#
# temp=new Box("temperature",15,-35,50," degrees Celsius is an unreasonably low temperature."," degrees Celsius is an unreasonably high temperature.");
# altitude=new Box("altitude",0,0,3000," metres is a very low altitude. Are you thinking about water mills?"," metres is an extremely high altitude, how are you going to get a turbine up there?");
# rough = new Box("rough",0.055,0.0002,1.6," m as roughness length is below roughness class zero."," m as roughness length is above roughness class 4.");
# pressure=new Box("pressure",p0,70,135," is an unreasonably low air pressure."," is an unreasonably high air pressure.");
# density=new Box("density",1.225,0.6,1.8," is an unreasonably low air density."," is an unreasonably high air density.");
# shape=new Box("shape",2,1,3," is an invalid shape parameter. The parameter must be beween 1 and 3."," is an invalid shape parameter. The parameter must be beween 1 and 3.");
# mean=new Box("mean",7,2,14," m/s is so low a wind speed that wind energy is insignificant."," m/s is an extremely high mean wind speed. If you are serious, send us an e-mail about where we find it - else...");
# scale=new Box("scale",7.9,1,13.432," is an invalid scale parameter. The parameter must be beween 2 and 10."," is an invalid scale parameter. The parameter must be beween 2 and 10.");
# mHeight=new Box("mHeight",50.0,3,200, "m is a very low measurement height. Disturbances from nearby obstacles are likely to give you very unreliable mesurements. ","m is a very high measurement height. We are talking about the distance from the ground of your anemometer, not the altitude above sea level. ");
# kWrated=new Box("kWrated",600,0,Number.MAX_VALUE," kW rated power does not make sense. ","");
# cutin=new Box("cutin",5,0,Number.MAX_VALUE," m/s as a cut in wind speed is not sensible. The cut in speed must be at least zero.","");
# cutout=new Box("cutout",25,0,35," m/s as a cut out wind speed is not sensible. The cut out speed must be at least zero."," m/s is a very high cut out wind speed. You may be running too large risks.");
# diam=new Box("diam",43,0.01,200," m as a rotor diameter does not make sense"," m rotor diameter is enormous! The largest wind turbine ever made had 100 metre rotor diameter.");
# hubHeight= new Box("hubHeight",50,18,150," m hub height is very low. There should be room for the rotor, we have to avoid ground turbulence, and we get more energy with a taller tower."," m towers are not really available at any reasonable cost on the market today.");
# powers = new BoxArray("kW", 30, 0, 0, 0, " kW is wrong. The turbine must have zero or a positive power output."," kW is far too large for the laws of physics");
# speeds = new BoxArray("ms", 30, 0, 0, 30, " m/s is too low. The wind speed must be a positive number."," m/s is too high a wind speed for safety. The turbine would have to be stopped at that speed.");
# init();
#
# function Turbine(name, diam, kW, kWalt, cutin ,cutout, towerHeights, powerCurve,aSpeeds,pitchPc) {
# 	this.name=name;
# 	this.diam=diam;
# 	this.kW=kW;
# 	this.kWalt=kWalt;
# 	this.cutin=cutin;
# 	this.cutout=cutout;
# 	this.towerHeights=towerHeights;
# 	this.powers=powerCurve;
# 	this.pitch=pitchPc;
# 	this.speeds=aSpeeds;
# 	turbines.Append(this); // Registers automatically in the turbines array
# }
# function Sites(aSelectListName) {
# 	this.name=aSelectListName;
# 	this.list=new Array(0);
# 	this.current=null;
# 	this.Select=SelectSite;
# 	this.Append=Append;
# }
# function SelectSite() {	// Set method for Sites
# 	var index=iiForm[this.name].selectedIndex; // index in menu
# 	if (index==0) { this.current=null; return;}
# 	var ndx=parseInt(iiForm[this.name].options[index].value);
# 	this.current=this.list[ndx];
# 	mHeight.Set(this.current.height);
# 	CheckClass();
# }
# function Turbines(aSelectListName) {	// List of turbines available
# 	this.name=aSelectListName;
# 	this.list=new Array(0);
# 	this.current=null;		// current turbine object
# 	this.Select=Select;
# 	this.Append=Append;
# 	this.Reset=Reset;
# }
# function Select() {	// Set method for Turbines
# 	var index=iiForm[this.name].selectedIndex; // index in menu
# 	var ndx=parseInt(iiForm[this.name].options[index].value); // index in Turbines.list
# 	this.current=this.list[ndx];
# 	kWrated.Set(this.current.kW);
# 	cutin.Set(this.current.cutin);
# 	cutout.Set(this.current.cutout);
# 	diam.Set(this.current.diam);
# 	hubHeight.Set(this.current.towerHeights[0]);
# 	// Update std. tower heights
# 	for (var i=1;iiForm["stdHeight"].options.length>i; i++)
# 	{
# 		if (this.current.towerHeights.length>=i)
# 		{
# 			iiForm["stdHeight"].options[i].text = this.current.towerHeights[i-1]+" m";
# 			iiForm["stdHeight"].options[i].value = this.current.towerHeights[i-1];
# 		}
# 		else
# 		{
# 			iiForm["stdHeight"].options[i].text = "";
# 			iiForm["stdHeight"].options[i].value = -1;
# 		}
# 	}
# 	iiForm["stdHeight"].selectedIndex=0;
# 	var temp=weighPc(this.current.powers, this.current.pitch,density.val());
# 	for (i=0;i<30;i++) {
# 		powers.Set(i,temp[i]);
# 		speeds.Set(i,this.current.speeds[i]);
# 	}
# }
# function weighPc(a,b,rho) {
# 	var r=new Array(0);
# 	if (b==null) b=a;
# 	for (var i=0;i<a.length;i++) {
# 		 r[i]=b[i]+(rho-1.06)*(a[i]-b[i])/( 1.2256527394654197-1.06);
# 	}
# 	return(r);
# }
# function Append(aTurbine) {	// Append method for Turbines
# 	this.list[this.list.length]=aTurbine; // Expands array automatically
# 	iiForm[this.name].options[this.list.length]=new Option(aTurbine.name, this.list.length-1);
# }
# function Reset() {	// Reset method for turbines (resets select menu to base option)
# 	iiForm[this.name].selectedIndex=1;
# }
# function CheckTurbine() {
# 	turbines.Select(); plot();
# }
# function init() {
# 	density.Set(1000*pressure.val()/(R*(temp.val() + T0)));
# 	turbines.Select();
# }
# function BoxArray(startName, no, def, min, max, mintxt, maxtxt) {
# 	this.name=startName;
# 	this.def=def;
# 	this.min=min;
# 	this.max=max;
# 	this.mintxt=mintxt;
# 	this.maxtxt=maxtxt;
# 	this.Set=SetBA;
# }
# function SetBA(n, val) {	// Set method for BoxArray
# 	iiForm[(this.name+(n+1))].value=val;
# }
# function Box(no, def, min, max, mintxt, maxtxt) {
# 	this.no=no;
# 	this.def=def;
# 	this.min=min;
# 	this.max=max;
# 	this.mintxt=mintxt;
# 	this.maxtxt=maxtxt;
# 	this.oldvalue=0;
# 	this.Set=Set;
# 	this.val=val;
# 	iiForm[this.no].value=this.def;
# }
# function val() {
# 	return(parseFloat(iiForm[this.no].value));
# }
# function Set(val) {
# 	var err=0;
# 	var newVal=0;
# 	if (Set.arguments.length==0) { newVal=parseFloat2(iiForm[this.no].value); }
# 	else { newVal=val; }
# 	if (this.min>newVal) err=1;
# 	if (newVal>this.max) err=2;
# 	if (err!=0)
# 	{
# 		if (err==1) alert(newVal+this.mintxt+" Please try again.");
# 		if (err==2) alert(newVal+this.maxtxt+" Please try again.");
# 		iiForm[this.no].value=this.def;
# 		return(false);
# 	}
# 	iiForm[this.no].value=newVal;
# 	this.oldvalue=newVal;
# 	return(true);
# }
# function CheckP(n) {
# 	// n indicates box number
# 	var power=parseFloat2(iiForm["kW"+n].value);
# 	var ms=parseFloat(iiForm["ms"+n].value);
# 	var yield=1000*power/(3.14159265*diam.val()*diam.val()*0.25); // power per square metre in Watts
# 	var betz=0.59*0.5*ms*ms*ms*1000*pressure.val()/(R*(15+T0)); // line 261
# 	if (yield>betz) {alert(power+powers.maxtxt+" at a wind speed of "+ms+" m/s."); iiForm["kW"+n].value = 0;}
# 	if (yield<powers.min) {alert(power+powers.mintxt); iiForm["kW"+n].value = 0}
# }
# function Ms(n) {
# 	var ms=parseFloat2(iiForm["ms"+n].value);
# 	if (ms<=0) {alert(ms+speeds.mintxt); iiForm["ms"+n].value = 0;}
# 	if (ms>speeds.max) {alert(ms+speeds.maxtxt); iiForm["ms"+n].value = 0;}
#
# }
# function CheckT() {
# 	if (temp.Set())
# 	{
# 		pressure.Set(Pressure(altitude.val(),temp.val()-altitude.val()*beta+T0));
# 		density.Set(1000*pressure.val()/(R*(temp.val() + T0))); 		plot();
# 	}
# }
# function CheckAlt() {
# 	var changed="decreased";
# 	var change="increase";
# 	var old=altitude.oldvalue;
# 	if (altitude.Set())
# 	{
# 		if (altitude.val()!= old)
# 		{
# 			var x=altitude.val()-old;
# 			var umpteen=-x*beta;
# 			var blabla=Pressure(altitude.val(), temp.val()+umpteen+altitude.val()*beta+T0)-pressure.val();
# 			if (x>0)
# 			{
# 				changed="increased";
# 				change="decrease";
# 			}
# 			alert("You have just "+changed+" the altitude by "+x+" metres. Normally, this would imply a temperature "+change+" of "+(0.01*Math.round(100*Math.abs(umpteen)))+" degrees, and a pressure "+change+" of "+(0.01*Math.round(100*Math.abs(blabla)))+" kPa. These corrections are made automatically. You may change the temperature afterwards, if you wish.");
# 			temp.Set(temp.val()+umpteen);
# 			pressure.Set(pressure.val()+blabla);
# 		}
# 		density.Set(1000*pressure.val()/(R*(temp.val() + T0))); 		plot();
# 	}
# }
# function CheckPressure() {
# 	var old=pressure.val();
# 	if (pressure.Set())
# 	{
# 		if (pressure.val() != old)
# 		{
# 			var ch=confirm("Warning: You have changed the standard air pressure. This field is normally set automatically by the programme. Do you really wish to go ahead with the change?");
# 			if (!ch)
# 			{
# 				iiForm[pressure.no].value=pressure.val();
# 			}
# 		}
# 	density.Set(1000*pressure.val()/(R*(temp.val() + T0)));
# 	plot();
# 	}
# }
# function CheckDensity() {
# 	var t=0;
# 	if (density.Set())
# 	{
# 		altitude.Set(0);
# 		t=(1000*pressure.val())/(density.val()*R)-T0;
# 		if (t>temp.max)
# 		{
# 			altitude.Set(altitude.max);
# 			t=(1000*pressure.val())/(density.val()*R)-T0;
# 		}
# 		temp.Set(t);
# 		plot();
# 	}
# }
# function CheckMean() {
# 	if (mean.Set()){ scale.Set(mean.val()/gamma(1+1/shape.val())); plot(); }
# }
# function CheckScale() {
# 	if (scale.Set()){ mean.Set(scale.val()*gamma(1+1/shape.val())); plot(); }
# }
# function CheckmHeight() {
# 	if (mHeight.Set()){ plot(); }
# }
# function CheckShape() {
# 	if (shape.Set()){ mean.Set(scale.val()*gamma(1+1/shape.val())); plot(); }
# }
# function CheckkW() {
# 	alert("WARNING: If you change the rated power of the main generator, you must also specify a new power curve yourself. Otherwise your results will be meaningless. If you want a standard machine with a different generator size, just use the pop up menu to select it.");
# 	if (kWrated.Set()){ turbines.Reset(); plot(); }
# }
# function CheckCutin() {
# 	if (cutin.Set()){ turbines.Reset(); plot(); }
# }
# function CheckCutout() {
# 	if (cutout.Set()){ turbines.Reset(); plot(); }
# }
# function CheckDiam() {
# 	alert("WARNING: If you change the rotor diameter, you must also specify a new power curve yourself. Otherwise your results will be meaningless. If you want a standard machine with a different rotor diameter, just use the pop up menu to select it.");
# 	if (diam.Set()){ turbines.Reset(); plot(); }
# }
# function CheckTowerHeight() {
# 	if (hubHeight.Set())
# 	{
# 		var towerExists=false;
# 		for (var i=0; turbines.current.towerHeights.length>i; i++)
# 		{ if (turbines.current.towerHeights[i]==hubHeight.val()) towerExists=true; }
# 		if (towerExists==false) turbines.Reset();
# 		plot();
# 	}
# }
# function CheckStdHeight() {
# 	var index=iiForm["stdHeight"].selectedIndex;
# 	var val=parseInt(iiForm["stdHeight"].options[index].value);
# 	if (val!=-1) { if(hubHeight.Set(val)) plot();}
# }
# function Pressure(alt, Ta) // Ta is abs temperature at sea level
# {
# 	return(p0*Math.pow(1-(beta*alt)/Ta,g/(R*beta)));
# }
# function plot()
# {
# 	iiForm.remark.value="";
# 	plotpowdensi(scale.val(),shape.val(),density.val(),cutin.val(),cutout.val(),diam.val());
# }
# function plotpowdensi(c,k,d,cuti,cuto,diam) // c is the scale parameter, k is the shape parameter
# {				// d is air density in kg/m3
# 	var pcu = MakePowerCurve();
# 	if (pcu==null) return;
# 	document.forms[0].comment.value = "";
# 	if (hubHeight.val() != mHeight.val()) document.forms[0].comment.value = "Note: Hub height differs from wind measurement height";
# 	var factor = WSpeed(hubHeight.val(), rough.val(), mHeight.val(), 1, rough.val());
# 	c*=factor;
# 	var m = c*gamma(1+1/k); // m is the mean wind speed value
# 	var fi=0;
# 	var u=0;
# 	var uc=0;
# 	var ucik=0;
# 	var kc=k/c;
# 	var max=0;
# 	var cMax=0;
# 	var uMax=0;
# 	var pow=0;
# 	var hd=0.5*d;
# 	var area=3.14159265*0.25*diam*diam; // Rotor area in m2
# 	var we=0; // Weibull data
# 	var akkW=0; // Total power at this site
# 	var akkWT=0; // Total power captured by turbine minus cutin cutout
# 	var prod=0; // Power produced by turbine
# 	var akkWP=0; // Total power produced by turbine
# 	iiForm.hhms.value=edit(m,1);
# 	for (var i=0;i<pcu.length;i++)
# 	{
# 		u=i*0.10;
# 		uc=u/c;
# 		ucik=Math.pow(uc,k-1);
# 		we=kc*ucik*Math.exp(-ucik*uc); // Weibull value
# 		pow=hd*u*u*u;
# 		fi=pow*we; // Power value in W/m2 times probability
# 		if (gPowden!=null) gPowden[i]=fi;
# 		akkW+=fi; // Accumulated power total
# 		if (fi>max) {max=fi; uMax=u}
# 		prod= we*1000*(d/1.225)*pcu[i] /area;
# 		if (gProd!=null) gProd[i]=prod;
# 		akkWT+=fi; // Power input on site
# 		if (cuti<=u && u<=cuto) akkWP+=prod; // Power output
# 	}
# 	cMax=0.01*Math.round(cMax*100);
# 	uMax=0.1*Math.round(uMax*10);
# 	akkW=Math.round(0.1*akkW);
# 	akkWT=Math.round(0.1*akkWT);
# 	akkWP=Math.round(0.1*akkWP);
# 	var totYr=Math.round(akkWP*area*24*365.25*0.001);
# 	iiForm.maxp.value = edit(uMax,1);
# 	iiForm.totp.value = akkWT;
# 	iiForm.turbp.value = akkWP;
# 	iiForm.turbe.value = Math.round(akkWP*365.25*24/1000);
# 	iiForm.turby.value = Math.round(totYr);
# 	iiForm.capfactor.value = Math.round(100*totYr /(365.25*24*kWrated.val()));
# 	if (gEcon!=null) {
# 		gEcon.document.forms[0].kWh.value=totYr;
# 		gEcon. CkWh();
# 	}
# }
# function parseFloat2(str)
# {
# 	for (var i=0;str.length>i;i++)
# 	{
# 		var c=str.charAt(i);
# 		if (c>"9" || "0">c)
# 		{
# 			if (c!="." && c!="+" && c!="-" && c!="e" && c!="E" && c!=" ")
# 			{
# 				alert("You have just entered an invalid character for numeric data. Please check that the number shown on the screen is what you intended.");
# 			}
# 		}
# 	}
# 	return(parseFloat(str));
# }
# function MakePowerCurve() {
# 	var ms = new Array(30+1);
# 	var pow = new Array(30+1);
# 	ms[0]=0;
# 	pow[0]=0;
# 	for (var i=0;i<30;i++) {
# 		ms[i+1] = parseFloat(iiForm[("ms"+(i+1))].value);
# 		pow[i+1] = parseFloat(iiForm[("kW"+(i+1))].value);
# 		if(ms[i+1]<=ms[i]) {alert("Wind speeds in power curve table must be in ascending (increasing) order."); return(null);}
# 	}
# 	var res = new Array(401); // an element for each 0.1 m/s
# 	var lower=0;
# 	var upper=ms[1];
# 	res[0]=0;
# 	var j=1;
# 	var theMs=0;
# 	for (var i=0;i<res.length;i++){
# 		theMs=0.1*i;
# 		while (theMs>upper) {
# 			j++;
# 			if (j>=ms.length){
# 				return(res);
# 			}
# 			else {
# 				lower=upper;
# 				upper=ms[j];
# 			}
# 		}
# 		res[i]=pow[j-1]+((theMs-lower)/(upper-lower))*(pow[j]-pow[j-1]);
# 		if ((pow[j-1]==0 && theMs!=upper) || (pow[j] ==0 && theMs!= lower)) res[i]=0;
# 	}
# 	return(res);
# }
# function WSpeed(height, roughness, refHeight, refSpeed, refRoughness)
# {
# 	return(refSpeed*Math.log(height/roughness)/Math.log(refHeight/refRoughness));
# }
# function CheckRough() {
# 	var max = iiForm.cls.options.length;
# 	if (rough.Set()) plot();
# 	iiForm.cls.selectedIndex = max-1;
# 	for (var i=0;i<max;i++) {
# 		if (rough.val() == iiForm.cls.options[i].value) iiForm.cls.selectedIndex = i;
# 	}
# }
# function CheckClass() {
# 	var i = iiForm.cls.selectedIndex;
# 	if (i == iiForm.cls.options.length) return;
# 	iiForm.rough.value = iiForm.cls.options[i].value;
# 	if (sites.current!=null) {
# 		var theText= iiForm.cls.options[i].text;
# 		if (theText=="other") {alert("You have not selected a roughness class for the "+sites.current.name+" site. The wind data is left unchanged."); plot(); return;}
# 		var cl=parseFloat(theText);
# 		if (cl>3) { alert("Sorry, we have no data for roughness classes above 3 for the "+sites.current.name+" site. The roughness class is set to 3.0"); cl=3.0;}
# 		var floor=Math.floor(cl);
# 		var ceiling=Math.ceil(cl);
# 		var fraction=cl-floor;
# 		var theA=sites.current.A[floor]*(1-fraction)+ sites.current.A[ceiling]*( fraction);
# 		var thek= sites.current.k[floor]*(1-cl)+ sites.current.k[ceiling]*( cl);
# 		iiForm.scale.value= theA;
# 		iiForm.shape.value= thek;
# 		CheckShape();
# 	}
# 	else {
# 		plot();
# 	}
# }
# function Powden() {
# 	gPowden=new Array(351);
# 	gProd=new Array(351);
# 	plot();
# 	gWindow = window.open("","Power_Density_Curve_for_Site","status=yes,width=420,height=350");
# 	graph(gPowden,1,gProd);
# 	gPowden=null;
# 	gProd=null;
# }
# function Powcu() {
# 	var pc = MakePowerCurve();
# 	gWindow = window.open("","Power_Curve","status=yes,width=420,height=350");
# 	graph(pc,1,null);
# }
# function Powco(){
# 	gWindow = window.open("","Power_Coefficient","status=yes,width=450,height=350");
# 	var pcu = MakePowerCurve();
# 	var radius = 0.5*parseFloat(document.forms[0].diam.value);
# 	var rotorArea = radius*radius*3.1415926535;
# 	var v = 0;
# 	for (var i=0;i<pcu.length;i++) {
# 		v = 0.1 * i;
# 		pcu[i]/=0.5*v*v*v*1.225*0.001*rotorArea;
# 	}
# 	graph(pcu,1,null);
# }
# function Sorry() {
# 	alert("Sorry, you cannot change a result. You will have to change the input data instead.");
# 	plot();
# }
# function graph(y,xStep,y2)
# {
# 	var noPoints=1+xStep*(y.length-1);
# 	var oldval=-1;
# 	var val=0;
# 	var val2=0;
# 	var step=1;
# 	var trueMax=Number.NEGATIVE_INFINITY;
# 	for (var i=0; y.length>i; i++) {
# 		if (y[i]>trueMax) trueMax=y[i];
# 	}
# 	var unit = 0.1*Math.pow(10,Math.ceil(Math.log(trueMax)/Math.log(10)));
# 	var n = Math.ceil(trueMax/unit);
# 	if (5>n) {unit = unit*0.2; n = Math.ceil(trueMax/unit);}
# 	var max=n*unit;
# 	var pixPerUnit = Math.floor(256/n); // 256 is max height
# 	var totalHeight=pixPerUnit*n;
# 	var scale=totalHeight/max;
# 	var slack= Math.round(scale*(max-trueMax))-7;
# 	if (slack<0) slack+=pixPerUnit;
# 	gWindow.document.clear();
# 	gWindow.document.write("<HTML><HEAD><TITLE>"+turbines.current.name+"</TITLE></HEAD>");
# 	gWindow.document.write("<BODY BGCOLOR='#ffffff' BACKGROUND='../../../../res/grwh"+pixPerUnit+".gif' ><P><IMG SRC='../../../r/t.gif' WIDTH="+noPoints+" HEIGHT="+slack+"><BR>");
# 	gWindow.document.write("<TABLE BORDER='0' CELLSPACING='0' CELLPADDING='0'><TR>");
# 	var maxTxt=trueMax.toString();
# 	maxTxt=maxTxt.substring(0,3)
# 	if (maxTxt.indexOf(".",1)==3) maxTxt = maxTxt.substring(0,2);
# 	gWindow.document.write("<TD VALIGN='TOP' ROWSPAN='2' ><FONT SIZE=2 FACE='gillsans, frutiger, arial, helvetica, geneva'>"+maxTxt);
# 	gWindow.document.write("</TD");
# 	for (var i=0; noPoints>i; i++) {
# 		val= Math.round(scale*y[i]);
# 		gWindow.document.write("<TD WIDTH='1' VALIGN='BOTTOM' >");
# 		step= Math.abs(val-oldval);
# 		if (step<1) step=1;
# 		if (y2!=null) {
# 			val2= Math.round(scale*y2[i]);
# 			betz= Math.round(val*16/27);
# 			step=val-betz;
# 			gWindow.document.write("<IMG SRC='../../../../res/grpix.gif' WIDTH=1 HEIGHT="+step+"><BR>");
# 		}
# 		else
# 		{
# 			gWindow.document.write("<IMG SRC='../../../../res/bluepix.gif' WIDTH=1 HEIGHT="+step+"><BR>");
# 		}
# 		var ww = val;
# 		if (val-oldval<0) ww=oldval;
# 		if (y2!=null) {
# 			ww=val2
# 			gWindow.document.write("<IMG SRC='../../../../res/bluepix.gif' WIDTH=1 HEIGHT="+(betz-ww)+"><BR>");
# 			gWindow.document.write("<IMG SRC='../../../../res/redpix.gif' WIDTH=1 HEIGHT="+ww+"></TD>");
# 		}
# 		else
# 		{
# 			gWindow.document.write("<IMG SRC='../../../r/t.gif' WIDTH=1 HEIGHT="+(ww-step)+"></TD>");
# 		}
# 		oldval=val;
# 	}
# 	gWindow.document.write("</TR><TD>&nbsp;</TD><TD COLSPAN='"+noPoints+"'>");
# 	var ticks = Math.floor(y.length/10) - 1;
# 	var h = 3;
# 	for (var i=0;i<ticks;i++) {
# 		h=3; if (i%5==0) h=5;
# 		gWindow.document.write("<IMG SRC='../../../../res/blpix.gif' WIDTH=1  HEIGHT="+h+" ALIGN='TOP'>");
# 		gWindow.document.write("<IMG SRC='../../../r/t.gif' WIDTH=9  HEIGHT=1 ALIGN='TOP'>");
# 	}
# 	gWindow.document.write("</TD></TR><TR><TD>&nbsp; ");
# 	for (var i=0;i<8;i++) {
# 		var x=i*5;
# 		if (i==7) x="m/s"
# 		gWindow.document.write("</TD><TD COLSPAN='50' ALIGN='LEFT'><FONT SIZE=2 FACE='gillsans, frutiger, arial, helvetica, geneva'>"+x);
# 	}
# 	gWindow.document.write("</TD><TD></TD></TR><TR><TD COLSPAN='"+(1+noPoints)+"'>");
#
# if (y2!=null) gWindow.document.write("<FONT SIZE=2 FACE='gillsans, frutiger, arial, helvetica, geneva'><IMG SRC='../../../../res/grpix.gif' WIDTH='8' HEIGHT='8'>&nbsp;= Total power input; <IMG SRC='../../../../res/bluepix.gif' WIDTH='8' HEIGHT='8'>&nbsp;= Usable power input (Betz' law); <IMG SRC='../../../../res/redpix.gif' WIDTH='8' HEIGHT='8'>&nbsp;= Turbine power output</FONT><BR>");
#
# gWindow.document.write("<FONT COLOR='#0066CC' SIZE=1 FACE='gillsans, frutiger, arial, helvetica, geneva'>Windspeed Graphics System Copyright &copy; 1997 DWIA</FONT>");
# 	gWindow.document.write("</TD></TR></TABLE></P></BODY></HTML>");
# 	gWindow.document.close();
# 	}
# function CheckSite() {
# 	sites.Select(); plot();
# }
# function Site(aName, aHeight, A0, k0, A1, k1, A2, k2, A3, k3) {
# this.name=aName;
# this.height=aHeight;
# this.A= new Array(A0,A1,A2,A3);
# this.k= new Array(k0,k1,k2,k3);
# sites.Append(this);
# }
# // Copyright 1998 Søren Krohn & DWIA
#
