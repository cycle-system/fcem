"""
Module that condense all the components of the EMS tested above
"""

# General Imports

import numpy as np
import skfuzzy as fuzz

# Sklearn imports

from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted
import inspect

"""
FCEM - v.0.1. 
"""

class threeLevelFCEM(BaseEstimator):
    
    """ 
    Fuzzy Comprehensive Evaluation Methodology implementation available to any configuration with
    3 levels (Goals | Category | KPI).
    
    Parameters
    ----------
    kpiParameters : array (# KPIs) of matrices (5 labels x 4 points membership function), default='None' - KPI configurations
    kpiStep : array (# KPIs), default='None' - Mapping to the step size for each KPI
    categoryMapping : array (# KPIs), default='None' - Mapping from Category to KPI matrix using the array index
    weightVectorCategories : array (# Categories) of arrays (# KPIs), default='None' - Weighting for Categories
    weightVectorGoals : array (# Goals) of arrays (# Categories), default='None' - Weighting for Goals
    """  
    
    def __init__(self,kpiParameters = None,kpiStep = None,categoryMapping = None,weightVectorCategories = None,weightVectorGoals = None):
        
        # Gather all the passed parameters
        args, _, _,values = inspect.getargvalues(inspect.currentframe())
        
        # Remove parameter 'self' 
        values.pop("self")

        # Init the attributes of the class
        for arg, val in values.items():
            setattr(self, arg, val)

    def fit(self, X, y = None):
        
        """ 
        Configure all the Membership Functions of the FCEM
        
        Features per row
        ----------
        X -> Not used
        
        Outputs
        ----------
        y -> Not used
             
        """
        
        # Define the functions
        
        self.xAxis = [];
        self.membership = [];
        
        # Configure the time vector for each KPI membership function
        
        index = 0;
        
        for kpi in self.kpiParameters:
        
            rangeMin = min(kpi[0]);
            rangeMax = max(kpi[len(kpi) - 1]);
            
            self.xAxis.append(np.arange(rangeMin, rangeMax, self.kpiStep[index]))
            
            index += 1;
            
        # Create membership function array for each KPI
            
        index = 0;
            
        for kpi in self.kpiParameters:
        
            arrayOfMembership = [];
        
            for label in kpi:
                
                arrayOfMembership.append(fuzz.trapmf(self.xAxis[index],label));
            
            self.membership.append(arrayOfMembership);
            
            index += 1;
            
        
        
        
        # Check input and target vectors correctness
        # ToDo
        
        # Initial value for initialization flag
        
        self.isInitialized_ = False;
        
        
        # Configure parameters when fitted
        
        self.isFitted_ = True;
        
        # `fit` should always return `self`
        return self

    def predict(self, X, y = None):
        
        """ 
        Fuzzy Comprehensive Evaluation Methodology implementation available to any configuration with
        3 levels (Goals | Category | KPI).
        
        Features per row
        ----------
        X -> List (# Desired measures) of lists (# KPIs) with processed data KPIs  
        
        Outputs
        ----------
        y[0] -> Evaluation for KPIs
        y[1] -> Evaluation for Categories 
        y[2] -> Evaluation for Goals 

        """
        
        # Define the Output vector
        
        y = [];
        
        # Verification before prediction
        
        check_is_fitted(self, 'isFitted_')
        
        # Perform the prediction over the input array
        
        for x in X :
            
            result = [];
            
            kpiEvaluations = [];
        
            index = 0;
        
            # Evaluate all the processed data KPIs with the membership functions
            
            for processedKpi in x:
                
                evaluation = [];
                
                for function in self.membership[index]:
                    
                    evaluation.append(fuzz.interp_membership(self.xAxis[index],function,processedKpi));
                    
                kpiEvaluations.append(evaluation)
                
                index += 1;
            
            result.append(kpiEvaluations)
            
            # Create lists for Category evaluation
            
            categoryEvaluation = [];
            
            for vector in self.weightVectorCategories:
                
                categoryEvaluation.append([]);
            
            # Fill the matrices of Category Evaluation
            
            index = 0;
            
            for kpi in kpiEvaluations:
            
                categoryEvaluation[categoryMapping[index]].append(kpi);
                
                index += 1;

            # Compute the Category scores
            
            computedCategoryEvaluation = [];
            
            index = 0;
            
            for matrix in categoryEvaluation:
                
                category = np.array([self.weightVectorCategories[index]]);
                kpis = np.array(matrix);
                
                computedCategoryEvaluation.append(np.dot(category,kpis)[0]);
                
                index += 1;
            
            result.append(computedCategoryEvaluation)
            
            # Compute the Goal Evaluation
            
            goal = np.array(weightVectorGoals);
            categories = computedCategoryEvaluation;
            
            goalEvaluation = np.dot(goal,categories);
            
            result.append(goalEvaluation);
        
            y.append(result);
        
        # Return the vector of outputs
        
        return y;
    
    """
    --------------------------------------------------------------------------------------------------
    Definition of specific EMS methods - NOT NEEDED FOR NOW
    --------------------------------------------------------------------------------------------------
    """
