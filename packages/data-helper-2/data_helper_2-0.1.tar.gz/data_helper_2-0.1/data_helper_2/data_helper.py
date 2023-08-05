class completeanalysis():
    
    """The class takes a dataframe, methods are written for \
     plotting and other analysis"""
     
    def __init__(self,df,classification=True,split_ratio=0.25,nsplit=5,random_state=0):
        self.df = df
        self.split_ratio = split_ratio
        self.df_X = df.iloc[:,:-1]
        self.df_y = df.iloc[:,-1]
        self.all_columns = list(self.df.columns)
        self.y = df.iloc[:,-1].values
        self.X = df.iloc[:,:-1].values
        self.objCol = list(self.df.select_dtypes(include = ['object']).columns)
        self.numCol = list(self.df.select_dtypes(include = ['float64','int64']).columns)
        self.numCol_x = list(self.df_X.select_dtypes(include = ['float64','int64']).columns)
        self.objCol_x = list(self.df_X.select_dtypes(include = ['object']).columns)
        self.predict_col = df.columns[-1]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = self.split_ratio, random_state = random_state)
        #self.class_models = [('LR', LogisticRegression()),('LDA', LinearDiscriminantAnalysis()),
        #                     ('KNN', KNeighborsClassifier()),('CART', DecisionTreeClassifier()),
        #                     ('NB', GaussianNB()),('SVM', SVC())]
        self.class_models = [('LR', LogisticRegression(multi_class ='ovr')),('SVC', SVC(kernel = 'linear', random_state = random_state))]
        self.class_scoring = 'roc_auc'
        self.kfold = KFold(n_splits=nsplit, random_state=random_state)
        
    def delete_column(self,name_of_col):
        for i in name_of_col:
            try:
                self.df = self.df.drop(name_of_col,axis=1)
                self.df_x = self.df_x.drop(name_of_col,axis=1)
                self.y = df.iloc[:,-1].values
                self.X = df.iloc[:,:-1].values
                self.objCol = list(self.df.select_dtypes(include = ['object']).columns)
                self.numCol = list(self.df.select_dtypes(include = ['float64','int64']).columns)
                self.numCol_x = list(self.df_x.select_dtypes(include = ['float64','int64']).columns)
                self.objCol_x = list(self.df_x.select_dtypes(include = ['object']).columns)
                self.all_columns = self.df.columns
            except:
                continue
         
    def col_meta_data(self):
        objCol = list(self.df.select_dtypes(include = ['object']).columns)
        numCol = list(self.df.select_dtypes(include = ['float64','int64']).columns)
        columndetails = []
        for i in objCol:
            columndetails.append({'Column Name':i,'Type' : 'Object' ,'Number of NULL values': float(self.df[i].isna().sum()),'Number of Unique Values':len(self.df[i].unique())})
        for i in numCol:
            columndetails.append({'Column Name':i,'Type' : 'Numeric' ,'Number of NULL values': float(self.df[i].isna().sum()),'Number of Unique Values':len(self.df[i].unique())})
        return(pd.DataFrame(columndetails))
    
    def distribution_plots(self):
        fig,axes = plt.subplots(nrows=(round(len(self.all_columns)/3)),ncols=3,figsize =(18,12))
        for i, ax in enumerate(fig.axes):
            if i < len(self.all_columns):
                #ax.axis([0, max(df[num_column[i]]), 0, 5])
                ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
                sns.distplot(df[self.all_columns[i]], ax=ax)
        fig.tight_layout()
        plt.show()
    
    def numerical_plots(self):
        fig,axes = plt.subplots(nrows=(round(len(self.numCol_x)/3)),ncols=3,figsize =(18,12))
        for i, ax in enumerate(fig.axes):
            if i < len(self.numCol_x):
                ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
                plt.title(i)
                sns.regplot(x=self.df_X[self.numCol_x[i]], y=self.y,ax=ax)
        fig.tight_layout()
        plt.show()
        
    def response_distribution(self):
        fig,ax = plt.subplots(1,1)  
        ax.axis([0, 5, 0, 5000])
        for i in self.df[self.predict_col].unique():
            ax.text(i-1,len(self.df[self.df[self.predict_col]==i]), str(len(self.df[self.df[self.predict_col]==i])), transform=ax.transData)
        sns.countplot(x=self.df[self.predict_col], alpha=0.7, data=self.df)
        
    def pairplot(self):
        sns.pairplot(self.df,diag_kind='kde',vars=self.numCol,hue=self.predict_col)

    def correlation_plot(self,low = 0,high = 0):
        df_corr = self.df_x.corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(df_corr[(df_corr >= high) | (df_corr <= low)],
         cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
         annot=True, annot_kws={"size": 8}, square=True);
                            
    def boxplots(self):
        fig,axes = plt.subplots(nrows=(round(len(self.numCol)/3)),ncols=3,figsize =(18,12))
        for i, ax in enumerate(fig.axes):
            if i < len(self.numCol):
                ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
                plt.title(i)
                sns.boxplot(y=df[self.numCol[i]], x=df[self.predict_col],ax=ax)
        fig.tight_layout()
        plt.show()
        
    def binning(self,col,valueList,labelNames):
        self.df[col] = pd.cut(self.df[col],valueList,labels = labelNames)
        self.df[col] = self.df[col].astype('object')
        return self.df
        
    def vif(self):
        #gather features
        features = "+".join(self.numCol_x)
        # get y and X dataframes based on this regression:
        y, X = dmatrices(self.predict_col+ '~' + features, self.df, return_type='dataframe')
        # For each X, calculate VIF and save in dataframe
        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif["features"] = X.columns
        return vif.round(1)
    
    def compare_algo(self):
        results = []
        names = []
        for name, model in self.class_models:
            cv_results = cross_val_score(model, self.X, self.y, cv=self.kfold, scoring=self.class_scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)
        fig = plt.figure()
        fig.suptitle('Algorithm Comparison')
        ax = fig.add_subplot(111)
        plt.boxplot(results)
        ax.set_xticklabels(names)
        plt.show()
        
    def dummy_data(self,columns=None):
        self.df_x_dummy = pd.get_dummies(self.df_x,drop_first=True,columns=columns)
        self.final_col_x = self.df_x_dummy.columns
        return self.df_x_dummy
    
    def cor_selector(self):
        cor_list = []
        # calculate the correlation with y for each feature
        for i in list(self.df_X.columns):
            cor = np.corrcoef(self.df_X[i], self.df_y)[0, 1]
            cor_list.append(cor)
        # replace NaN with 0
        cor_list = [0 if np.isnan(i) else i for i in cor_list]
        # feature name
        self.cor_feature = self.df_X.iloc[:,np.argsort(np.abs(cor_list))[-100:]].columns.tolist()
        # feature selection? 0 for not select, 1 for select
        self.cor_support = [True if i in self.cor_feature else False for i in list(self.df_X.columns)]
        return pd.DataFrame(self.cor_support, self.cor_feature)
    
    def chi_selector(self):
        X_norm = MinMaxScaler().fit_transform(self.df_X)
        chi_selector = SelectKBest(chi2, k=10)
        chi_selector.fit(X_norm, self.y)
        self.chi_support = chi_selector.get_support()
        self.chi_feature = list(self.df_X.loc[:,self.chi_support].columns)
        return pd.DataFrame(self.chi_support, self.chi_feature)
    
    def RFE(self):
        X_norm = MinMaxScaler().fit_transform(self.df_X)
        rfe_selector = RFE(estimator=LogisticRegression(), n_features_to_select=10, step=10, verbose=5)
        rfe_selector.fit(X_norm, self.y)
        self.rfe_support = rfe_selector.get_support()
        self.rfe_feature = list(self.df_X.loc[:,self.rfe_support].columns)
        return pd.DataFrame(self.rfe_support, self.rfe_feature)
    
    def embed_lr(self):
        X_norm = MinMaxScaler().fit_transform(self.df_X)
        embeded_lr_selector = SelectFromModel(LogisticRegression(penalty="l1"), '1.25*median')
        embeded_lr_selector.fit(X_norm, self.y)
        self.embeded_lr_support = embeded_lr_selector.get_support()
        self.embeded_lr_feature = self.df_X.loc[:,self.embeded_lr_support].columns.tolist()
        return pd.DataFrame(self.embeded_lr_support,self.embeded_lr_feature)
    
    def embed_rf(self):
        embeded_rf_selector = SelectFromModel(RandomForestClassifier(n_estimators=10), threshold='1.25*median')
        embeded_rf_selector.fit(self.X, self.y)
        self.embeded_rf_support = embeded_rf_selector.get_support()
        self.embeded_rf_feature = list(self.df_X.loc[:,self.embeded_rf_support].columns)
        return pd.DataFrame(self.embeded_rf_support,self.embeded_rf_feature)
    
    def embed_LGBM(self):
        lgbc=LGBMClassifier(n_estimators=10, learning_rate=0.05, num_leaves=32, colsample_bytree=0.2,
                    reg_alpha=3, reg_lambda=1, min_split_gain=0.01, min_child_weight=40)
        embeded_lgb_selector = SelectFromModel(lgbc, threshold='1.25*median')
        embeded_lgb_selector.fit(self.df_X, self.y)
        self.embeded_lgb_support = embeded_lgb_selector.get_support()
        self.embeded_lgb_feature = list(self.df_X.loc[:,self.embeded_lgb_support].columns)
        return pd.DataFrame(self.embeded_lgb_support,self.embeded_lgb_feature)
    
    def feature_support(self):
        _ = self.cor_selector()
        _ = self.chi_selector()
        _ = self.RFE()
        self.feature_selection_df = pd.DataFrame({'Feature':list(self.df_X.columns), 'Pearson':self.cor_support, 'Chi-2':self.chi_support, 'RFE':self.rfe_support})
        # count the selected times for each feature
        self.feature_selection_df['Total'] = np.sum(self.feature_selection_df, axis=1)
        # display the top 100
        self.feature_selection_df = self.feature_selection_df.sort_values(['Total','Feature'] , ascending=False)
        self.feature_selection_df.index = range(1, len(self.feature_selection_df)+1)
        return self.feature_selection_df