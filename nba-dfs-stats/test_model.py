from pandas import * 
import pandasql
import numpy as np
import MySQLdb as mdb
import sys
import string
import pdb
import datetime
from os import listdir
from DKLineupOptimizer import LineupOptimizer
from decimal import *
import csv

DB_HOST = '173.194.110.63'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = 'Jermann1'
DB_NAME = 'nbastats'
STRATEGY_DIR = 'dkstrategies' 

COEFFICIENTS = {'TwoGameDoubleDigitBlocks': -9.56025,
'PrevGameDoubleDigitBlocks': -7.771493,
'Intercept': -3.664901,
'OffensiveReboundRatio': -2.364374,
'TwoGameDoubleDigitAssists': -2.185807,
'FiveGameThreesPct': -1.662997,
'FourGameTwentyPoints': -1.030766,
'PrevGameDoubleDouble': -0.4630055,
'ThreeGameTripleDouble': -0.3853141,
'FiveGameDoubleDigitRebounds': -0.2278286,
'TwoGameDoubleDigitCategories': -0.1848764,
'FourGameTurnovers': -0.1527424,
'FiveGameDoubleDigitCategories': -0.1389445,
'PrevGameShotsMade': -0.1361692,
'TwoGameOffensiveRebounds': -0.1128141,
'TwoGameShotsMade': -0.110561,
'PrevGameShotPct': -0.106594,
'TwoGameDoubleDigitPoints': -0.1011248,
'TwoGameBlocks': -0.09267557,
'FourGameThreesPct': -0.08766461,
'FourGameShotsMade': -0.07531323,
'PrevGameRebounds': -0.05707361,
'PrevGameDefensiveRebounds': -0.05298008,
'FourGameThreesAttempted': -0.05172004,
'ThreeGameAssists': -0.04980597,
'FiveGameThreesAttempted': -0.04288179,
'FiveGameDoubleDouble': -0.03415103,
'FourGameAssists': -0.0315696,
'FiveGameBlocks': -0.02653542,
'FourGameThreesMade': -0.02222501,
'DefensiveReboundRatio': -0.02164218,
'TwoGameSteals': -0.02057845,
'TeamSpread': -0.01840445,
'OverUnder': -0.01100133,
'FiveGamePlusMinus': -0.008114935,
'FiveGameThreesMade': -0.001621689,
'OppBlocks5Game': -0.001609458,
'ThreeGamePlusMinus': -0.0007546913,
'OppReboundsAgainst': -0.00002610623,
'MissedShotsDefensiveRebounds': -0.00000433048,
'ExpectedPointTotal': -0.000001031249,
'OppPointsAllowed': 0.00005058215,
'OppPointsAgainst': 0.0004272669,
'ExpectedPlayerPoints': 0.0004868425,
'PrevGameDollars': 0.0006904209,
'ExpectedPlayerAssists': 0.000930458,
'FourGameOffensiveRebounds': 0.001960343,
'Dollars': 0.003178865,
'PrevGamePoints': 0.003293061,
'TwoGameMinutes': 0.003744827,
'ThreeGameDoubleDigitCategories': 0.004211604,
'OppStealsAgainst': 0.005531516,
'ThreeGameShotsAttempted': 0.006132074,
'OppTurnovers': 0.007474682,
'FourGameDefensiveRebounds': 0.009772518,
'ReboundRatio5Game': 0.009773343,
'FiveGameDefensiveRebounds': 0.01269573,
'FourGameShotsAttempted': 0.01334379,
'PrevGameMinutes': 0.01554758,
'FiveGameShotsAttempted': 0.01837291,
'TwoGameDoubleDouble': 0.0208891,
'FiveGameSteals': 0.02199413,
'ThreeGameMinutes': 0.03096645,
'FiveGameRebounds': 0.03662519,
'TwoGameShotsAttempted': 0.03940698,
'FourGameBlocks': 0.04101381,
'FourGameRebounds': 0.04252047,
'PrevGameSteals': 0.04589061,
'FiveGameOffensiveRebounds': 0.0473671,
'FourGameSteals': 0.05251558,
'TwoGameThreesMade': 0.05294575,
'TwoGameAssists': 0.06103976,
'PrevGameShotsAttempted': 0.09894348,
'TwoGameThreesAttempted': 0.1052462,
'FiveGameShotPct': 0.1096529,
'ThreeGameDoubleDigitPoints': 0.1135925,
'PrevGameTurnovers': 0.1174146,
'FiveGameTurnovers': 0.160572,
'ThreeGameDoubleDouble': 0.2731635,
'HomeTeam': 0.2752021,
'PrevGameDoubleDigitCategories': 0.4096536,
'PrevGameDoubleDigitPoints': 0.4128788,
'ThreeGameDoubleDigitRebounds': 0.4217104,
'TwoGameThreesPct': 0.4560937,
'FourGameDoubleDigitAssists': 0.573267,
'PrevGameTwentyPoints': 0.5871701,
'ThreeGameShotPct': 0.7129182,
'TwoGameTwentyPoints': 0.9992815,
'PrevGameDoubleDigitAssists': 1.493954,
'PrevGameTripleDouble': 2.42925,
'ThreeGameDoubleDigitBlocks': 3.741796,
'FourGameDoubleDigitBlocks': 6.286302,
'PrevGameDKPointsPerDollar': 265.8833,
'PrevGameThreesAttempted': 0,
'PrevGameThreesMade': 0,
'PrevGameThreesPct': 0,
'PrevGameAssists': 0,
'PrevGameBlocks': 0,
'PrevGameOffensiveRebounds': 0,
'PrevGamePlusMinus': 0,
'PrevGameDoubleDigitRebounds': 0,
'PrevGameDoubleDigitSteals': 0,
'TwoGamePoints': 0,
'TwoGameShotPct': 0,
'TwoGameRebounds': 0,
'TwoGameDefensiveRebounds': 0,
'TwoGameTurnovers': 0,
'TwoGamePlusMinus': 0,
'TwoGameDoubleDigitRebounds': 0,
'TwoGameDoubleDigitSteals': 0,
'ThreeGamePoints': 0,
'ThreeGameShotsMade': 0,
'ThreeGameThreesAttempted': 0,
'ThreeGameThreesMade': 0,
'ThreeGameThreesPct': 0,
'ThreeGameBlocks': 0,
'ThreeGameSteals': 0,
'ThreeGameRebounds': 0,
'ThreeGameOffensiveRebounds': 0,
'ThreeGameDefensiveRebounds': 0,
'ThreeGameTurnovers': 0,
'ThreeGameTwentyPoints': 0,
'ThreeGameDoubleDigitAssists': 0,
'ThreeGameDoubleDigitSteals': 0,
'FourGamePoints': 0,
'FourGameShotPct': 0,
'FourGamePlusMinus': 0,
'FourGameMinutes': 0,
'FourGameDoubleDigitPoints': 0,
'FourGameDoubleDigitRebounds': 0,
'FourGameDoubleDigitSteals': 0,
'FourGameDoubleDigitCategories': 0,
'FiveGamePoints': 0,
'FiveGameShotsMade': 0,
'FiveGameAssists': 0,
'FiveGameMinutes': 0,
'FiveGameDoubleDigitPoints': 0,
'FiveGameTwentyPoints': 0,
'FiveGameDoubleDigitAssists': 0,
'FiveGameDoubleDigitBlocks': 0,
'FiveGameDoubleDigitSteals': 0,
'ExpectedTeamPoints': 0,
'ExpectedPlayerRebounds': 0,
'PrevGameDraftkingsPoints': 0,
'TwoGameTripleDouble': 0,
'TwoGameDraftkingsPoints': 0,
'ThreeGameDraftkingsPoints': 0,
'FourGameDoubleDouble': 0,
'FourGameTripleDouble': 0,
'FourGameDraftkingsPoints': 0,
'FiveGameTripleDouble': 0,
'FiveGameDraftkingsPoints': 0,
'OppShotsMade': 0,
'OppShotsPct': 0,
#'TeamPoints': 0,
'OppAssistsAgainst': 0}


OLD_COEFFICIENTS = {'PrevGameDKPointsPerDollar': -151.2919,
'PrevGameDoubleDigitBlocks': -5.851714,
'ThreeGameDoubleDigitBlocks': -5.297644,
'Intercept': -3.981755,
'OppShotsPct': -2.200426,
'FourGameShotPct': -1.64808,
'TwoGameDoubleDigitBlocks': -1.314744,
'PrevGameDoubleDouble': -1.119297,
'FiveGameThreesPct': -0.9131851,
'ThreeGameDoubleDigitAssists': -0.8543261,
'PrevGameTripleDouble': -0.7915997,
'TwoGameShotPct': -0.7440065,
'PrevGameThreesPct': -0.6783799,
'OffensiveReboundRatio': -0.5991616,
'ThreeGameTripleDouble': -0.4806218,
'PrevGameDoubleDigitRebounds': -0.4478054,
'ExpectedPlayerRebounds': -0.4380068,
'TwoGameTripleDouble': -0.3998839,
'FourGameThreesPct': -0.3462124,
'FiveGameDoubleDouble': -0.345002,
'ThreeGameTwentyPoints': -0.3309854,
'FourGameTwentyPoints': -0.2823506,
'ReboundRatio5Game': -0.2727222,
'FourGameTripleDouble': -0.1790415,
'TwoGameDoubleDigitPoints': -0.152931,
'TwoGameOffensiveRebounds': -0.1331745,
'PrevGameShotsMade': -0.1298245,
'FiveGameDoubleDigitRebounds': -0.09429359,
'FourGameTurnovers': -0.08916336,
'PrevGameTurnovers': -0.08462481,
'FourGameDoubleDigitPoints': -0.07779055,
'ThreeGameDoubleDigitRebounds': -0.07390523,
'PrevGameThreesAttempted': -0.06591732,
'TwoGameShotsMade': -0.0620188,
'FourGameThreesMade': -0.05742276,
'ThreeGameAssists': -0.04054103,
'FourGameShotsMade': -0.03893626,
'FiveGameThreesMade': -0.03616569,
'FiveGameBlocks': -0.03061873,
'FiveGameTripleDouble': -0.02945377,
'TwoGameDoubleDigitCategories': -0.02718237,
'TwoGameSteals': -0.02357794,
'TeamSpread': -0.02051567,
'TwoGameRebounds': -0.02032677,
'ThreeGameShotsMade': -0.01980433,
'FourGameThreesAttempted': -0.01953298,
'ThreeGameDoubleDigitCategories': -0.01925737,
'FourGameAssists': -0.01812997,
'ThreeGameOffensiveRebounds': -0.01574735,
'PrevGamePlusMinus': -0.01173011,
'FourGameBlocks': -0.01026861,
'FiveGamePlusMinus': -0.009786462,
'FiveGameThreesAttempted': -0.006554596,
'ThreeGameThreesMade': -0.005717853,
'FourGamePoints': -0.003684615,
'OppBlocks5Game': -0.002420494,
'OverUnder': -0.001857012,
'FourGameDraftkingsPoints': -0.001724721,
'ThreeGamePlusMinus': -0.001629364,
'TwoGamePoints': -0.001253327,
'ThreeGameThreesAttempted': -0.0009760322,
'MissedShotsDefensiveRebounds': 0.00004794037,
'TwoGameDraftkingsPoints': 0.0002091796,
'ExpectedPlayerPoints': 0.0002271869,
'ExpectedPlayerAssists': 0.0004817401,
'ThreeGameDraftkingsPoints': 0.0006858974,
'PrevGameDollars': 0.001198277,
'Dollars': 0.001381086,
'FourGameDoubleDigitCategories': 0.002972818,
'FiveGameDraftkingsPoints': 0.003136708,
'TwoGameDefensiveRebounds': 0.003483754,
'FiveGameShotsMade': 0.003541717,
'FiveGameMinutes': 0.003707908,
'TwoGamePlusMinus': 0.004084476,
'OppShotsMade': 0.004217763,
'FourGameMinutes': 0.004597733,
'FourGamePlusMinus': 0.00688391,
'ThreeGamePoints': 0.007520384,
'ExpectedTeamPoints': 0.008175279,
'FiveGamePoints': 0.008208711,
'TwoGameMinutes': 0.008608732,
'ThreeGameRebounds': 0.009968553,
'ThreeGameMinutes': 0.01348732,
'FourGameSteals': 0.01475441,
'PrevGameDraftkingsPoints': 0.01528755,
'FourGameDefensiveRebounds': 0.01601664,
'FourGameRebounds': 0.01607153,
'ThreeGameSteals': 0.01774695,
'FiveGameAssists': 0.01887522,
'DefensiveReboundRatio': 0.01911875,
'PrevGameDefensiveRebounds': 0.01927158,
'FiveGameDoubleDigitCategories': 0.02025848,
'FourGameShotsAttempted': 0.02077491,
'ThreeGameDefensiveRebounds': 0.02193035,
'OppTurnovers': 0.02210771,
'FiveGameRebounds': 0.02346145,
'FiveGameDoubleDigitPoints': 0.02434725,
'ThreeGameShotsAttempted': 0.02605883,
'PrevGameMinutes': 0.02710032,
'PrevGamePoints': 0.02714334,
'FiveGameShotsAttempted': 0.02808421,
'FiveGameOffensiveRebounds': 0.0289918,
'ThreeGameDoubleDigitPoints': 0.03016656,
'TwoGameBlocks': 0.03064474,
'TwoGameThreesMade': 0.0316405,
'FiveGameDefensiveRebounds': 0.0354942,
'ThreeGameTurnovers': 0.03816281,
'PrevGameRebounds': 0.03844153,
'PrevGameAssists': 0.03934343,
'FourGameOffensiveRebounds': 0.04790744,
'TwoGameShotsAttempted': 0.04907767,
'HomeTeam': 0.05548406,
'PrevGameShotsAttempted': 0.06123623,
'TwoGameDoubleDigitAssists': 0.0629853,
'TwoGameThreesAttempted': 0.06301015,
'FiveGameSteals': 0.08241128,
'ThreeGameBlocks': 0.09056195,
'FourGameDoubleDouble': 0.1006142,
'TwoGameAssists': 0.1087956,
'TwoGameTurnovers': 0.1099756,
'FourGameDoubleDigitRebounds': 0.1144684,
'FiveGameTurnovers': 0.1353239,
'ThreeGameDoubleDouble': 0.1522239,
'FiveGameTwentyPoints': 0.1569286,
'PrevGameThreesMade': 0.1613115,
'PrevGameOffensiveRebounds': 0.1651026,
'PrevGameSteals': 0.1810288,
'PrevGameBlocks': 0.216972,
'TwoGameTwentyPoints': 0.2805507,
'TwoGameThreesPct': 0.3244406,
'FiveGameDoubleDigitBlocks': 0.3259691,
'TwoGameDoubleDigitRebounds': 0.3714425,
'PrevGameDoubleDigitCategories': 0.3716601,
'TwoGameDoubleDouble': 0.3753681,
'FiveGameShotPct': 0.4222492,
'ThreeGameThreesPct': 0.4370634,
'PrevGameTwentyPoints': 0.4846816,
'FiveGameDoubleDigitAssists': 0.4929093,
'PrevGameDoubleDigitPoints': 0.7429853,
'FourGameDoubleDigitAssists': 0.7720767,
'PrevGameDoubleDigitAssists': 0.8482994,
'PrevGameShotPct': 0.8494402,
'ThreeGameShotPct': 2.392946,
'FourGameDoubleDigitBlocks': 6.116571,
'PrevGameDoubleDigitSteals': 0,
'TwoGameDoubleDigitSteals': 0,
'ThreeGameDoubleDigitSteals': 0,
'FourGameDoubleDigitSteals': 0,
'FiveGameDoubleDigitSteals': 0}


def update_database(con, input_dataframe, table, drop=True, index=False):
    try:
        cur = con.cursor()
        if drop:
            drop_query = 'DROP TABLE IF EXISTS ' + table
            cur.execute(drop_query)
            con.commit()
            if not index:
                input_dataframe.insert(0, 'ID', input_dataframe.index.tolist())
        input_dataframe.to_sql(table, con, 'mysql', if_exists='append', index=False)

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

def get_index(con, query):
    try:
        cur = con.cursor()
        cur.execute(query)

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

def mult_coefficients(df, coefficients):
    ret_val = df['FiveGameAssists']*0 + coefficients['Intercept']
    ret_val.astype(float)
    for coefficient in coefficients:
        if coefficient != 'Intercept':
	    ret_val += float(coefficients[coefficient])*df[coefficient].astype(float)
    return ret_val

def main():
    con = mdb.connect(host=DB_HOST,
                      port=DB_PORT,
                      user=DB_USER,
                      passwd=DB_PWD,
                      db=DB_NAME)

    cur = con.cursor()
    cur.execute("SELECT * FROM TodayTrainingDataWithTeams")
    training = cur.fetchall()
    field_names = [i[0] for i in cur.description]
    training = list(training)
    training_df = DataFrame(training, columns=field_names)
    training_df['Points'] = mult_coefficients(training_df, COEFFICIENTS)
    model = training_df[['PlayerID','Points']]

    update_database(con, model, 'Model', drop=True, index=True)

    training_df['Points'] = mult_coefficients(training_df, OLD_COEFFICIENTS)
    model = training_df[['PlayerID','Points']]

    update_database(con, model, 'Old_Model', drop=True, index=True)

    con.close()

if __name__ == "__main__":
    main()
