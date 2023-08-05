# -*- coding: utf-8 -*-

import scipy.stats as stat
import numpy as np
import itertools as it


###################################################################################### pairwise/nodewise stats ###########################################################################################################


def return_signif_code(p_values, uncor_alpha=0.05, fdr_alpha=0.05, bon_alpha=0.05):

    N = p_values.shape[0]

    ################# by default, code = 1 (cor at 0.05)
    signif_code = np.ones(shape=N)

    ################ uncor #############################
    # code = 0 for all correlation below uncor_alpha
    signif_code[p_values >= uncor_alpha] = 0

    ################ FPcor #############################
    if 1.0/N < uncor_alpha:

        signif_code[p_values < 1.0/N] = 2

    ################ fdr ###############################
    seq = np.arange(N, 0, -1)

    seq_fdr_p_values = fdr_alpha/seq

    order = p_values.argsort()

    signif_sorted = p_values[order] < seq_fdr_p_values

    signif_code[order[signif_sorted]] = 3

    ################# bonferroni #######################

    signif_code[p_values < bon_alpha/N] = 4

    return signif_code


def return_signif_code_Z(Z_values, uncor_alpha=0.05, fdr_alpha = 0.05, bon_alpha = 0.05):

    N = Z_values.shape[0]

    ###################### by default, code = 1 (cor at 0.05)
    signif_code = np.ones(shape=N)

    ################ uncor #############################
    
    Z_uncor = stat.norm.ppf(1-uncor_alpha/2)

    signif_code[Z_values < Z_uncor] = 0

    print (signif_code)
    ################ FPcor #############################

    Z_FPcor = stat.norm.ppf(1-(1.0/(2*N)))

    signif_code[Z_values > Z_FPcor] = 2

    print (signif_code)
    
    ################ fdr ###############################

    seq = np.arange(N, 0, -1)

    seq_fdr_p_values = fdr_alpha/seq

    seq_Z_val = stat.norm.ppf(1-seq_fdr_p_values/2)

    order = (-Z_values).argsort() ### classé dans l'ordre inverse

    sorted_Z_values = Z_values[order] ### classé dans l'ordre inverse

    signif_sorted = sorted_Z_values > seq_Z_val

    signif_code[order[signif_sorted]] = 3

    ################# bonferroni #######################

    Z_bon = stat.norm.ppf(1-bon_alpha/(2*N))

    signif_code[Z_values > Z_bon] = 4

    return signif_code

################################################ pairwise stats ##########################################

def compute_pairwise_ttest_fdr(X, Y, cor_alpha, uncor_alpha, paired=True, old_order=True, keep_intracon=False):

    ### old order was n_nodes, n_nodes, sample_size
    ### new order is sample_size, n_nodes, n_nodes,
    
    # number of nodes
    if old_order:
        X = np.moveaxis(X,2,0)
        Y = np.moveaxis(Y,2,0)
    
    # test squared matrices
    assert X.shape[1] == X.shape[2] and Y.shape[1] == Y.shape[2], "Error, X {} {} and/or Y {} {} are not squared".format(
        X.shape[1], X.shape[2], Y.shape[1], Y.shape[2])

    # test same number of nodes between X and Y
    assert X.shape[1] == Y.shape[1] , "Error, X {} and Y {}do not have the same number of nodes".format(
        X.shape[1], Y.shape[1])

    # test if same number of sample (paired t-test only)
    if paired:
        assert X.shape[0] == Y.shape[0], "Error, X and Y are paired but do not have the same number od samples{}{}".format(
            X.shape[0], Y.shape[0])

    ### info nodes
    N = X.shape[1]

    ### test are also done on the diagonal of the matrix
    if keep_intracon:
        iter_indexes = it.combinations_with_replacement(list(range(N)), 2)
    else:
        iter_indexes = it.combinations(list(range(N)), 2)

    ### computing signif t-tests for each relevant pair 
    list_diff = []

    for i, j in iter_indexes:

        print (X[:,i,j])
        
        ### removing the nan
        X_nonan = X[np.logical_not(np.isnan(X[:, i, j])), i, j]
        Y_nonan = Y[np.logical_not(np.isnan(Y[:, i, j])), i, j]

        print (X_nonan)
        
        if len(X_nonan) < 2 or len(Y_nonan) < 2:
            print ("Not enough values for sample {} {}, len = {} and {}, skipping".format(i,j,len(X_nonan),len(Y_nonan)))
            continue

        if paired == True:
            t_stat, p_val = stat.ttest_rel(X_nonan, Y_nonan)
            if np.isnan(p_val):
                print("Warning, unable to compute T-test: ")

            # pas encore present (version scipy 0.18)
            #t_stat,p_val = stat.ttest_rel(X[i,j,:],Y[i,j,:],nan_policy = 'omit')

        else:
            t_stat, p_val = stat.ttest_ind(X_nonan, Y_nonan)

        list_diff.append([i, j, p_val, np.sign(
            np.mean(X_nonan)-np.mean(Y_nonan)), t_stat])

    assert len(list_diff) != 0, "Error, list_diff is empty"

    np_list_diff = np.array(list_diff)

    signif_code = return_signif_code(
        np_list_diff[:, 2], uncor_alpha=uncor_alpha, fdr_alpha=cor_alpha, bon_alpha=cor_alpha)

    np_list_diff[:, 3] *=  signif_code

    #### formatting signif_mat, p_val_mat and T_stat_mat
    signif_mat = np.zeros((N, N), dtype='int')
    p_val_mat = np.zeros((N, N), dtype='float')
    T_stat_mat = np.zeros((N, N), dtype='float')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_mat[signif_i, signif_j] = signif_mat[signif_j,signif_i] = np_list_diff[:, 3].astype(int)
    p_val_mat[signif_i, signif_j] = p_val_mat[signif_j,signif_i] = np_list_diff[:, 2]
    T_stat_mat[signif_i, signif_j] = T_stat_mat[signif_j,signif_i] = np_list_diff[:, 4]

    return signif_mat, p_val_mat, T_stat_mat


def compute_pairwise_oneway_ttest_fdr(X, cor_alpha, uncor_alpha, old_order=True):

    if old_order:
        X = np.moveaxis(X,2,0)

    # number of nodes
    assert X.shape[1] == X.shape[2],  "Error, X {}{} and/or Y {}{} are not squared".format(
        X.shape[1], X.shape[2])

    N = X.shape[1]

    list_diff = []

    for i, j in it.combinations(list(range(N)), 2):

        X_nonan = X[np.logical_not(np.isnan(X[:, i, j])), i, j]

        if len(X_nonan) < 2:
            print ("Not enough values for sample {} {}, len = {}, skipping".format(i,j,len(X_nonan)) )   
            continue

        t_stat, p_val = stat.ttest_1samp(X_nonan, 0.0) ## 0.0 ?

        if np.isnan(p_val):

            print("Warning, unable to compute T-test: ")
            print(t_stat, p_val, X_nonan, end=' ')

        list_diff.append([i, j, p_val, np.sign(np.mean(X_nonan)), t_stat])

    print(list_diff)

    assert len(list_diff) != 0, "Error, list_diff is empty"

    np_list_diff = np.array(list_diff)

    print(np_list_diff)

    signif_code = return_signif_code(
        np_list_diff[:, 2], uncor_alpha, fdr_alpha=cor_alpha, bon_alpha=cor_alpha)

    np_list_diff[:, 3] *= signif_code

    signif_mat = np.zeros((N, N), dtype='int')
    p_val_mat = np.zeros((N, N), dtype='float')
    T_stat_mat = np.zeros((N, N), dtype='float')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_mat[signif_i, signif_j] = signif_mat[signif_j,signif_i] = np_list_diff[:, 3].astype(int)
    p_val_mat[signif_i, signif_j] = p_val_mat[signif_j,signif_i] = np_list_diff[:, 2]
    T_stat_mat[signif_i, signif_j] = T_stat_mat[signif_j,signif_i] = np_list_diff[:, 4]

    print(T_stat_mat)

    return signif_mat, p_val_mat, T_stat_mat


def compute_pairwise_mannwhitney_fdr(X, Y, fdr_alpha, uncor_alpha=0.01, old_order = True):
    ### modified to be compatible with old_order = True (was only developed for old order) + assert
    ### TODO : test if OK with moveaxis and 'new order'? 
    ### TODO : return parameter of mannwhitneyu (i.e. "U" values)?
    
    if old_order:
        X = np.moveaxis(X,2,0)
        Y = np.moveaxis(Y,2,0)

    #### Assert
    
    # test squared matrices
    assert X.shape[1] == X.shape[2] and Y.shape[1] == Y.shape[2], "Error, X {} {} and/or Y {} {} are not squared".format(
        X.shape[1], X.shape[2], Y.shape[1], Y.shape[2])

    # test same number of nodes between X and Y
    assert X.shape[1] == Y.shape[1] , "Error, X {} and Y {}do not have the same number of nodes".format(
        X.shape[1], Y.shape[1])

    # number of nodes
    N = X.shape[1]

    #### compute
    list_diff = []

    for i, j in it.combinations(list(range(N)), 2):

        #### TODO: handles nan correctly??
        u_stat, p_val = stat.mannwhitneyu(X[:, i, j], Y[:, i, j], use_continuity=False)

        sign_diff = np.sign(np.mean(X[: , i, j])-np.mean(Y[:, i, j])
        list_diff.append([i, j, p_val, sign_diff)])

    np_list_diff = np.array(list_diff)

    signif_code = return_signif_code(np_list_diff[:, 2], uncor_alpha=uncor_alpha, fdr_alpha=fdr_alpha, bon_alpha=0.05)

    np_list_diff[:, 3] = np_list_diff[:, 3] * signif_code

    signif_signed_adj_mat = np.zeros((N, N), dtype='int')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)
    signif_sign = np.array(np_list_diff[:, 3], dtype=int)

    signif_mat[signif_i,signif_j] = signif_mat[signif_j, signif_i] = signif_sign

    return signif_mat


#### private function for compute_pairwise_binom_fdr
def _info_CI(X, Y):
    """ Compute binomial comparaison"""
    nX = len(X) * 1.
    nY = len(Y) * 1.

    pX = np.sum(X == 1)/nX

    pY = np.sum(Y == 1)/nY

    SE = np.sqrt(pX * (1-pX)/nX + pY * (1-pY)/nY)

    return np.absolute(pX-pY), SE, np.sign(pX-pY)

def compute_pairwise_binom_fdr(X, Y, conf_interval_binom_fdr, old_order = True):
    ### modified to be compatible with old_order = True (was only developed for old order) + assert
    ### TODO : test if OK with moveaxis and 'new order'? 
    
    if old_order:
        X = np.moveaxis(X,2,0)
        Y = np.moveaxis(Y,2,0)

    #### Assert
    
    # test squared matrices
    assert X.shape[1] == X.shape[2] and Y.shape[1] == Y.shape[2], "Error, X {} {} and/or Y {} {} are not squared".format(
        X.shape[1], X.shape[2], Y.shape[1], Y.shape[2])

    # test same number of nodes between X and Y
    assert X.shape[1] == Y.shape[1] , "Error, X {} and Y {}do not have the same number of nodes".format(
        X.shape[1], Y.shape[1])

    # number of nodes
    N = X.shape[1]


    # Perform binomial test at each edge
    list_diff = []

    for i, j in it.combinations(list(range(N)), 2):

        abs_diff, SE, sign_diff = _info_CI(X[: i, j], Y[:, i, j])

        list_diff.append([i, j, abs_diff/SE, sign_diff])

    print(list_diff)

    np_list_diff = np.array(list_diff)

    signif_code = return_signif_code_Z(np_list_diff[:, 2], conf_interval_binom_fdr)

    np_list_diff[:, 3] = np_list_diff[:, 3] * signif_code

    signif_signed_adj_mat = np.zeros((N, N), dtype='int')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_sign = np.array(np_list_diff[:, 3], dtype=int)

    signif_mat[signif_i,signif_j] = signif_mat[signif_j, signif_i] = signif_sign

    return signif_mat

### TODO : warning, this is very different than previous functions, needs to be checked where it is called
# OneWay Anova (F-test)
def compute_oneway_anova_fwe(list_of_list_matrices, cor_alpha=0.05, uncor_alpha=0.001, keep_intracon=False):

    assert False, "Warning, very old function, check your call and report it to developer"
    
    for group_mat in list_of_list_matrices:
        assert group_mat.shape[1] == group_mat.shape[2], "warning, matrices are not squared {} {}".format(
            group_mat.shape[1], group_mat.shape[2])

    N = group_mat.shape[2]

    list_diff = []

    if keep_intracon:
        iter_indexes = it.combinations_with_replacement(list(range(N)), 2)

    else:
        iter_indexes = it.combinations(list(range(N)), 2)

    for i, j in iter_indexes:

        list_val = [group_mat[:, i, j].tolist()
                    for group_mat in list_of_list_matrices]

        F_stat, p_val = stat.f_oneway(*list_val)

        list_diff.append([i, j, p_val, F_stat])

    ############### computing significance code ################

    np_list_diff = np.array(list_diff)

    print(np_list_diff)

    signif_code = return_signif_code(
        np_list_diff[:, 2], uncor_alpha=uncor_alpha, fdr_alpha=cor_alpha, bon_alpha=cor_alpha)

    signif_code[np.isnan(np_list_diff[:, 2])] = 0

    print(np.sum(signif_code == 0.0), np.sum(signif_code == 1.0), np.sum(
        signif_code == 2.0), np.sum(signif_code == 3.0), np.sum(signif_code == 4.0))

    # converting to matrix

    signif_adj_mat = np.zeros((N, N), dtype='int')
    p_val_mat = np.zeros((N, N), dtype='float')
    F_stat_mat = np.zeros((N, N), dtype='float')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_adj_mat[signif_i, signif_j] = signif_adj_mat[signif_j,
                                                        signif_i] = signif_code
    p_val_mat[signif_i, signif_j] = p_val_mat[signif_i,
                                              signif_j] = np_list_diff[:, 2]
    F_stat_mat[signif_i, signif_j] = F_stat_mat[signif_i,
                                                signif_j] = np_list_diff[:, 3]

    # print signif_adj_mat
    # print p_val_mat
    # print F_stat_mat

    return signif_adj_mat, p_val_mat, F_stat_mat


def compute_correl_behav(X, reg_interest, uncor_alpha=0.001, cor_alpha=0.05, old_order=False, keep_intracon=False):

    import numpy as np
    import itertools as it

    import scipy.stats as stat

    from graphpype.utils_stats import return_signif_code
    
    if old_order:
       X = X.moveaxis(X, 0,2)
       
    N = X.shape[1]

    print(reg_interest)
    print(reg_interest.dtype)

    if keep_intracon:
        iter_indexes = it.combinations_with_replacement(list(range(N)), 2)
    else:
        iter_indexes = it.combinations(list(range(N)), 2)

    # number of nodes
    assert X.shape[1] == X.shape[2] and "Error, X {}{} is not squared".format(
        X.shape[1], X.shape[2])

    assert X.shape[0] == reg_interest.shape[0], "Incompatible number of fields in dataframe and nb matrices"

    list_diff = []

    for i, j in iter_indexes:

        keep_val = (~np.isnan(X[:, i, j])) & (~np.isnan(reg_interest))
        print(keep_val)
        
        X_nonan = X[keep_val,i,j]
        reg_nonan = reg_interest[keep_val]

        r_stat, p_val = stat.pearsonr(X_nonan, reg_nonan)

        print(r_stat, p_val)

        if np.isnan(p_val):

            print("Warning, unable to compute T-test: ")
            print(r_stat, p_val, X_nonan, Y_nonan)

            # pas encore present (version scipy 0.18)
            #t_stat,p_val = stat.ttest_rel(X[i,j,:],Y[i,j,:],nan_policy = 'omit')

        list_diff.append([i, j, p_val, np.sign(r_stat), r_stat])

    print(list_diff)

    assert len(list_diff) != 0, "Error, list_diff is empty"

    np_list_diff = np.array(list_diff)

    print(np_list_diff)

    signif_code = return_signif_code(
        np_list_diff[:, 2], uncor_alpha=uncor_alpha, fdr_alpha=cor_alpha, bon_alpha=cor_alpha)

    print(np.sum(signif_code == 0.0), np.sum(signif_code == 1.0), np.sum(
        signif_code == 2.0), np.sum(signif_code == 3.0), np.sum(signif_code == 4.0))

    np_list_diff[:, 3] = np_list_diff[:, 3] * signif_code

    print(np.sum(np_list_diff[:, 3] == 0.0))
    print(np.sum(np_list_diff[:, 3] == 1.0), np.sum(np_list_diff[:, 3] == 2.0), np.sum(
        np_list_diff[:, 3] == 3.0), np.sum(np_list_diff[:, 3] == 4.0))
    print(np.sum(np_list_diff[:, 3] == -1.0), np.sum(np_list_diff[:, 3] == -2.0),
          np.sum(np_list_diff[:, 3] == -3.0), np.sum(np_list_diff[:, 3] == -4.0))

    signif_signed_adj_mat = np.zeros((N, N), dtype='int')
    p_val_mat = np.zeros((N, N), dtype='float')
    r_stat_mat = np.zeros((N, N), dtype='float')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_signed_adj_mat[signif_i, signif_j] = signif_signed_adj_mat[signif_j,
                                                                      signif_i] = np.array(np_list_diff[:, 3], dtype=int)

    p_val_mat[signif_i, signif_j] = p_val_mat[signif_j,
                                              signif_i] = np_list_diff[:, 2]
    r_stat_mat[signif_i, signif_j] = r_stat_mat[signif_j,
                                                signif_i] = np_list_diff[:, 4]

    print(r_stat_mat)

    return signif_signed_adj_mat, p_val_mat, r_stat_mat


############### nodewise stats #########################
def compute_nodewise_t_test_vect(d_stacked, nx, ny):

    print(d_stacked.shape)

    assert d_stacked.shape[1] == nx + ny

    t1 = time.time()

    t_val_vect = compute_nodewise_t_values(
        d_stacked[:, :nx], d_stacked[:, nx:nx+ny])

    t2 = time.time()

    print("computation took %f" % (t2-t1))

    return t_val_vect

######################## correl ######################################


def compute_pairwise_correl_fdr(X, behav_score, correl_thresh_fdr):

    from scipy.stats.stats import pearsonr

    # number of nodes
    N = X.shape[0]

    list_diff = []

    for i, j in it.combinations(list(range(N)), 2):

        #t_stat_zalewski = ttest2(X[i,j,:],Y[i,j,:])

        r_stat, p_val = pearsonr(X[i, j, :], behav_score)

        # print i,j,p_val,r_stat

        list_diff.append([i, j, p_val, np.sign(r_stat)])

    # print list_diff

    np_list_diff = np.array(list_diff)

    np_list_diff = np.array(list_diff)

    signif_code = return_signif_code(
        np_list_diff[:, 2], uncor_alpha=0.001, fdr_alpha=correl_thresh_fdr, bon_alpha=0.05)

    print(np.sum(signif_code == 0.0), np.sum(signif_code == 1.0), np.sum(
        signif_code == 2.0), np.sum(signif_code == 3.0), np.sum(signif_code == 4.0))

    np_list_diff[:, 3] = np_list_diff[:, 3] * signif_code

    print(np.sum(np_list_diff[:, 3] == 0.0))
    print(np.sum(np_list_diff[:, 3] == 1.0), np.sum(np_list_diff[:, 3] == 2.0), np.sum(
        np_list_diff[:, 3] == 3.0), np.sum(np_list_diff[:, 3] == 4.0))
    print(np.sum(np_list_diff[:, 3] == -1.0), np.sum(np_list_diff[:, 3] == -2.0),
          np.sum(np_list_diff[:, 3] == -3.0), np.sum(np_list_diff[:, 3] == -4.0))

    signif_signed_adj_mat = np.zeros((N, N), dtype='int')

    signif_i = np.array(np_list_diff[:, 0], dtype=int)
    signif_j = np.array(np_list_diff[:, 1], dtype=int)

    signif_sign = np.array(np_list_diff[:, 3], dtype=int)

    print(signif_i, signif_j)

    print(signif_signed_adj_mat[signif_i, signif_j])

    # print signif_sign

    signif_signed_adj_mat[signif_i,
                          signif_j] = signif_signed_adj_mat[signif_j, signif_i] = signif_sign

    print(signif_signed_adj_mat)

    return signif_signed_adj_mat
