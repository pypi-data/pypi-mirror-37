
#   MNUBO DATA SCIENCE LIBRARY

'mnubo Data Science Library' objective is to centralize and standardize data science and data analysis functions used for pre-sales or POCs at mnubo.

it can contain:
   - our utilisation usage of some "common" libraries and the manipulation/presentation of results
   - some helper/frequently used functions...

##  IMPORTANT NOTES
  - Upon successful (automatic) build on Jenkins build server, this library is PUSHED to a PYPI servers.

  - obviously, MNUBO IP/code or CUSTOMER specific algos MUST NOT be included here!


#  HOW TO MODIFY THE MNUBO DATA SCIENCE LIBRARY
-----------------------------------------------------

##  setup your DEV environment to access and modify the data-science-library :

  1. LOGIN as yourself in Gitlab (http://git-lab1.mtl.mnubo.com/) and FORK data-science-library project

  2. ADD 'central/mnubo' branch :
    *  ```git clone gitlab@git-lab1.mtl.mnubo.com:smartobjects/data-science-library.git```
    *  ```cd data-science-library```
    *  ```git remote rename origin central```

  3. You can now add your fork to your working directory

    NOTE: REPLACE 'YOURNAME' below with your USERNAME: ex: jcbeaudin

    From your dev 'workplace'/directory, execute:

    ```git remote add origin gitlab@git-lab1.mtl.mnubo.com:```YOURNAME```/data-science-library.git```

##  in order to create new version of data-science-library :

  0. Make sure your dev environment is setup as described above.

  1. GET the latest version:
    *  ```git fetch central```
    *  ```git rebase central/master```

  2. ### create/modify/fix library!!! using your favorive editor.

  3. PUSH/publish your work:
    *  ```git add .```
    *  ```git commit -m "enter a relevant comment or description of your work here. a JIRA nb somewhere is great"```
    *  ```git fetch central```
    *  ```git rebase central/master```
    *  ```git push origin master```
    *  on GITLAB, create a Merge Request to “mnubo master” (central master)

  4. CREATION of a NEW LIB on Pypi server:

     nothing to do, Jenkins will build the latest version when MR will be accepted.

     build/jenkins server is at:  http://jenkins.mtl.mnubo.com/


#  List of ideas for the next functions :

    *  Scoring Function
    *  TTT
    *  Churn Prediction
    *  Interpolation
    *  Linear Regression
    *  Time Series Forecast
    *  Time Series Smoothing
    *  FFT
    *  Anomaly Detection (8 different functions)
    *  Entropy
    *  PCA
    *  Remove Outliers
    *  Percentile
    *  SAX - symbolic representation for time series
    *  TSNE for data visualization
    *  Test for Statistical significance difference


