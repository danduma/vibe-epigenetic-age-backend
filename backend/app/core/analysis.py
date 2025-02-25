import pandas as pd
import numpy as np
from ..schemas.sample import ClockType


from biolearn.model_gallery import ModelGallery
from biolearn.data_library import GeoData

def get_all_clocks():
    """Get all available clock models"""
    gallery = ModelGallery()
    clocks = {
        ClockType.HORVATH: gallery.get("Horvathv1"),
        ClockType.HANNUM: gallery.get("Hannum"),
        ClockType.PHENOAGE: gallery.get("PhenoAge"),
    }
    return clocks

def process_methylation_data(
    file_path: str,
    imputation_strategy: str = "mean",
    normalize_data: bool = True
) -> dict:
    """Process methylation data using all available clocks"""
    try:
        # Load methylation data using GeoData
        data = GeoData.from_methylation_matrix(file_path)
        
        # Get all clock models
        clocks = get_all_clocks()
        
        # Store results for each clock
        results = {}
        
        # Run each clock
        for clock_type, clock_model in clocks.items():
            try:
                # Run the clock (imputation is handled automatically by the model)
                predictions = clock_model.predict(data)
                
                # Calculate statistics
                age_predictions = predictions['Predicted']
                mean_age = float(np.mean(age_predictions))
                std_age = float(np.std(age_predictions)) if len(age_predictions) > 1 else 0.0
                
                # Store results for this clock
                results[clock_type] = {
                    "predicted_age": mean_age,
                    "std_predicted_age": std_age,
                    "num_samples": len(age_predictions),
                    "individual_predictions": age_predictions.tolist(),
                }
            except Exception as clock_error:
                # If one clock fails, store the error but continue with others
                results[clock_type] = {
                    "error": str(clock_error)
                }
        
        # Return combined results
        return {
            "clocks": results,
            "total_sites_used": len(data.dnam.index),
            "config": {
                "imputation_strategy": imputation_strategy,
                "normalize_data": normalize_data
            }
        }

    except Exception as e:
        raise ValueError(f"Error processing methylation data: {str(e)}") 