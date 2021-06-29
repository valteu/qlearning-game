import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

INTERVALL_SIZE = 1.5
database = pd.read_excel(r'C:\Users\vtt\Desktop\stellerator_database.xlsx', sheet_name="ishcdb_26", nrows=0)

database_columns = database.columns.ravel()

stelleratorlist = np.array(np.unique(database['STELL']))

# database_w7 = database.loc[(database['STELL'] == "W7-AS") & (database["NEBAR"] > 5e19)]

# intervall:
'''
def intervall(column):
    intervall = []
    status = ""
    if np.min(column) < 0:
        min_ = np.min(column)
        status = "smaller 0"
    else:
        min_ = np.min(column[column>0])
        status = "greater 0"
    while min_ * INTERVALL_SIZE < np.max(column):
        if status == "smaller 0":
            if min_ < -0.5:
                intervall.append([min_, min_ / INTERVALL_SIZE])
                min_ /= INTERVALL_SIZE
            elif -0.5 < min_ < 0:
                intervall.append([min_, min_ / -INTERVALL_SIZE])
                min_ /= -INTERVALL_SIZE
            elif min_ > 0:
                intervall.append([min_, min_ * INTERVALL_SIZE])
                min_ *= INTERVALL_SIZE     
        else:
            intervall.append([min_, min_ * INTERVALL_SIZE])
            min_ *= INTERVALL_SIZE
            
    intervall.append([0.9 * np.max(column), np.max(column)])
    return(intervall)
'''
def intervall(column):
    intervall = []
    if np.min(column) < 0:
        if np.absolute(np.min(column)) < np.min(column[column>0]):
            min_ = np.absolute(np.min(column))
        else:
            min_ = np.min(column[column>0])
    else:
        min_ = np.min(column[column>0])
    while min_ * 1.5 < np.max(column):

        intervall.append([min_, min_ * 1.5])
        min_ *= 1.5
    intervall.append([0.9 * np.max(column), np.max(column)])
    return(intervall)

testi=0
for stell_ in stelleratorlist:
    if stell_ == "W7-X" :
        continue
    database_stell = database.loc[(database["STELL"] == stell_)]
    ptot_intervall = intervall(database_stell["PTOT"])
    bt_intervall = intervall(database_stell["BT"])
        
    iota23_intervall = intervall(database_stell["IOTA23"])
    iota0_intervall = intervall(database_stell["IOTA0"])
    rgeo_intervall = intervall(database_stell["RGEO"])
    aeff_intervall = intervall(database_stell["AEFF"])
    print("STELLERATOR: ", stell_)
    for ptot_ in ptot_intervall:
        for bt_ in bt_intervall:
            for iota0_ in iota0_intervall:
                for rgeo_ in rgeo_intervall:
                    for aeff_ in aeff_intervall:
                        database_i = database_stell.loc[(database_stell["PTOT"] >= ptot_[0])  & (database_stell["PTOT"] <= ptot_[1]) & (database_stell["BT"] >= bt_[0]) & (database_stell["BT"] <= bt_[1]) &
                        (database_stell["IOTA0"] >= iota0_[0]) & (database_stell["IOTA0"] <= iota0_[1]) & 
                        (database_stell["RGEO"] >= rgeo_[0]) & (database_stell["RGEO"] <= rgeo_[1]) & (database_stell["AEFF"] >= aeff_[0]) 
                        & (database_stell["AEFF"] <= aeff_[1])]
                        '''
                        database_c = database_i.loc[(database_i["PABSNBI"] > 0) & (database_i["PABSECH"] > 0)]
                        if len(database_c) > 0 :
                            print("c:",len(database_c))
                            
                        for a in range(len(database_i)):
                            if np.isnan(database_i["PABSECH"].iat[a]) == False & np.isnan(database_i["PABSNBI"].iat[a]) == False:
                                if database_i["PABSECH"].iat[a] > 0:
                                    if database_i["PABSNBI"].iat[a] > 0:
                                        print(database_i["PABSECH"].iat[a])                            
                                        print(database_i["PABSNBI"].iat[a])
                        '''
                        # if database_i.empty == False: 
                        '''
                        for i in range(len(database_i)):
                            if database_i["NEBAR"].iat[i] == database_i["NEBAR"].iat[i] and database_i["TAUEDIA"].iat[i] == database_i["TAUEDIA"].iat[i] and database_i["ISS04"].iat[i] == database_i["ISS04"].iat[i] and database_i["AEFF"].iat[i] == database_i["AEFF"].iat[i] and database_i["BT"].iat[i] == database_i["BT"].iat[i] and database_i["RGEO"].iat[i] == database_i["RGEO"].iat[i] and database_i["IOTA23"].iat[i] == database_i["IOTA23"].iat[i] and database_i["PTOT"].iat[i] == database_i["PTOT"].iat[i]:
                                database_n = database_i
                                # nebar_list.append(database_i["NEBAR"])
                                # tauedia_list.append(database_i["TAUEDIA"])
                                # iss04_list.append(10 ** database_i["LOG_TAUE_ISS04"])
                                a = 10 ** database_i["LOG_TAUE_ISS04"].iat[i]
                                b = (0.134 * database_i["AEFF"].iat[i] ** 2.28) * (database_i["RGEO"].iat[i] ** 0.64) * ((database_i["PTOT"].iat[i] / 1e6) ** (-0.61)) * ((database_i["NEBAR"].iat[i] / 1e19) ** 0.54) * (database_i["BT"].iat[i] ** 0.84) * (database_i["IOTA0"].iat[i] ** 0.41)
                                print("ISS04 = ", a)
                                print("      = ", b)
                        '''
                        if len(database_i) > 5:
                            fig, axs_ = plt.subplots(3, 1)
                            fig.set_figheight(15)
                            fig.set_figwidth(15)
                            fig.suptitle("Stellerator: " + stell_ + " ; Ptot Mittelwert: " + str(0.5 * (ptot_[0] + ptot_[1])), y=0.98, size=30)
                            database_a = database_i.loc[(database_i["PABSECH"] > 0) & (database_i["PABSNBI"] == 0) & (database_i["PABSICH"] == 0)]
                            database_b = database_i.loc[(database_i["PABSNBI"] > 0) & (database_i["PABSECH"] == 0) & (database_i["PABSICH"] == 0)]
                            database_c = database_i.loc[(database_i["PABSNBI"] > 0) & (database_i["PABSECH"] > 0)]
                            axs_[0].plot(database_a["NEBAR"], database_a["TAUEDIA"] / (10 ** database_a["LOG_TAUE_ISS04"]), "o")
                            axs_[0].set_title("PABSECH")
                            axs_[0].set_xlabel("$\\bar{n}_e$")
                            axs_[0].set_ylim([0, 1.5])
                            axs_[0].set_ylabel("$\\tau_\\mathrm{E,ECRH}$")
                            axs_[1].plot(database_b["NEBAR"], database_b["TAUEDIA"] / (10 ** database_b["LOG_TAUE_ISS04"]), "o")
                            axs_[1].set_xlabel("$\\bar{n}_e$")
                            axs_[1].set_ylabel("$\\tau_\\mathrm{E,NBI}$")
                            axs_[1].set_ylim([0, 1.5])
                            axs_[2].plot(database_c["NEBAR"], database_c["TAUEDIA"] / (10 ** database_c["LOG_TAUE_ISS04"]), "o")
                            # axs_[1, 1].plot(database_c["PABSECH"], database_c["NEBAR"], "o")
                            axs_[2].set_xlabel("$\\bar{n}_e$")
                            axs_[2].set_ylabel("$\\tau_\\mathrm{E,ECRH+NBI}$")
                            axs_[2].set_ylim([0, 1.5])
                            
                            testi+=1
                            '''
                            axs_[2, 0].plot(database_i["NEBAR"], database_i["TAUEDIA"], "o")
                            axs_[2, 0].set_xlabel("$\\bar{n}_e$")
                            axs_[2, 0].set_title("a=%.3f,R=%.3f,Bt=%.2f,iota=%.2f,P=%.3f"%(aeff_[0], rgeo_[0], bt_[0], iota23_[0], ptot_[0] / 1e6))
                            axs_[2, 1].plot(database_i["NEBAR"], database_i["TAUEDIA"] / (10 ** database_i["LOG_TAUE_ISS04"]), "o")
                            axs_[2, 1].set_xlabel("$\\bar{n}_e$")
                            '''
                            plt.tight_layout()
                            plt.subplots_adjust(top=0.9)
                            plt.savefig("test%0.4d.png" %testi)
                            plt.close("all")
                                    # plt.close("all")
'''
# plt.plot(nebar_, tauedia_, "o")
# plt.xlabel("$\\bar{n}_e$")
# plt.ylabel("$\\tau_\\mathrm{E}$")
# plt.ylim([0, 0.1])
# plt.show
for i in range(len(nebar_list)):
    axs[0].plot(nebar_list[i], tauedia_list[i], "o")
# plt.xlabel("$\\bar{n}_e$")
# plt.ylabel("$\\tau_\\mathrm{E}$")
# axs[0].ylim([0, 0.02])
for i in range(len(iss04_list)):
    axs[1].plot(nebar_list[i], iss04_list[i], "o")
plt.show
'''
