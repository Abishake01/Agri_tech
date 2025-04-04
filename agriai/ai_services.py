# ai_services.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import json
import os
from datetime import datetime

class CropRecommender:
    def __init__(self):
        # Initialize with sample crop data (in production, this would come from a database)
        self.crop_data = self._load_crop_data()
        self._prepare_data()
        
    def _load_crop_data(self):
        """Load or create crop dataset with agricultural parameters"""
        crops = [
            # Format: crop_name, temperature, rainfall, humidity, soil_type, water_requirement, yield_potential, market_demand
            ('Wheat', 20, 500, 60, 'loamy', 2500, 'High', 'High'),
            ('Rice', 25, 1200, 80, 'clay', 5000, 'High', 'High'),
            ('Maize', 25, 600, 65, 'loamy', 3000, 'Medium', 'Medium'),
            ('Sorghum', 30, 400, 50, 'sandy', 2000, 'Medium', 'Medium'),
            ('Millet', 28, 350, 45, 'sandy', 1800, 'Medium', 'Low'),
            ('Barley', 15, 450, 55, 'loamy', 2200, 'Medium', 'Medium'),
            ('Soybean', 22, 600, 70, 'loamy', 2800, 'High', 'High'),
            ('Cotton', 27, 550, 60, 'loamy', 3200, 'High', 'Medium'),
            ('Potato', 18, 500, 70, 'loamy', 2500, 'High', 'High'),
            ('Tomato', 24, 600, 65, 'loamy', 3500, 'High', 'High')
        ]
        
        return pd.DataFrame(crops, columns=[
            'crop_name', 'temperature', 'rainfall', 'humidity', 
            'soil_type', 'water_requirement', 'yield_potential', 'market_demand'
        ])
    
    def _prepare_data(self):
        """Prepare data for recommendation algorithm"""
        # Encode categorical features
        self.le_soil = LabelEncoder()
        self.le_crop = LabelEncoder()
        
        self.crop_data['soil_encoded'] = self.le_soil.fit_transform(self.crop_data['soil_type'])
        self.crop_data['crop_encoded'] = self.le_crop.fit_transform(self.crop_data['crop_name'])
        
        # Convert water requirement to efficiency score (1-100)
        max_water = self.crop_data['water_requirement'].max()
        self.crop_data['water_efficiency'] = 100 - (
            (self.crop_data['water_requirement'] / max_water) * 100
        ).astype(int)
        
        # Train KNN model
        self.knn = NearestNeighbors(n_neighbors=5)
        features = self.crop_data[[
            'temperature', 'rainfall', 'humidity', 
            'soil_encoded', 'water_requirement'
        ]]
        self.knn.fit(features)
    
    def recommend_crops(self, temperature, rainfall, humidity, soil_type, water_availability):
        """
        Recommend crops based on environmental conditions and water availability
        
        Args:
            temperature: Average temperature in °C
            rainfall: Annual rainfall in mm
            humidity: Average humidity percentage
            soil_type: String (clay, sandy, loamy, silty)
            water_availability: Scale of 1-5 (1=low, 5=high)
            
        Returns:
            List of recommended crops with details
        """
        try:
            soil_encoded = self.le_soil.transform([soil_type])[0]
        except ValueError:
            # Default to loamy if unknown soil type
            soil_encoded = self.le_soil.transform(['loamy'])[0]
            
        # Adjust water requirement based on availability (1-5 scale)
        water_adjusted = (6 - water_availability) * 1000  # Convert scale to approximate liters
            
        query_point = np.array([[
            temperature, rainfall, humidity, 
            soil_encoded, water_adjusted
        ]])
        
        distances, indices = self.knn.kneighbors(query_point)
        
        recommended = self.crop_data.iloc[indices[0]].copy()
        
        # Add additional calculated fields
        recommended['suitability_score'] = 100 - (distances[0] * 10).astype(int)
        recommended['water_efficiency'] = recommended['water_efficiency'].astype(str) + '%'
        
        return recommended.to_dict('records')


class WaterAdvisor:
    def __init__(self):
        self.water_requirements = self._load_water_data()
        
    def _load_water_data(self):
        """Load water requirements for different crops"""
        return {
            'Wheat': {'water_per_acre': 2500, 'frequency_days': 7, 'best_time': 'morning'},
            'Rice': {'water_per_acre': 5000, 'frequency_days': 3, 'best_time': 'any'},
            'Maize': {'water_per_acre': 3000, 'frequency_days': 5, 'best_time': 'morning'},
            'Sorghum': {'water_per_acre': 2000, 'frequency_days': 10, 'best_time': 'evening'},
            'Millet': {'water_per_acre': 1800, 'frequency_days': 12, 'best_time': 'evening'},
            'Barley': {'water_per_acre': 2200, 'frequency_days': 8, 'best_time': 'morning'},
            'Soybean': {'water_per_acre': 2800, 'frequency_days': 6, 'best_time': 'morning'},
            'Cotton': {'water_per_acre': 3200, 'frequency_days': 4, 'best_time': 'morning'},
            'Potato': {'water_per_acre': 2500, 'frequency_days': 5, 'best_time': 'morning'},
            'Tomato': {'water_per_acre': 3500, 'frequency_days': 3, 'best_time': 'morning'}
        }
    
    def calculate_water_drain_time(self, diameter, depth, current_level, pump_rate):
        """
        Calculate time to drain a well completely
        
        Args:
            diameter: Well diameter in meters
            depth: Well depth in meters
            current_level: Current water level in meters
            pump_rate: Pump rate in liters/second
            
        Returns:
            Hours to drain (rounded to 2 decimal places)
        """
        if pump_rate <= 0:
            return 0
            
        # Calculate well volume (cylinder volume formula)
        radius = diameter / 2
        volume_m3 = 3.14159 * (radius ** 2) * current_level
        
        # Convert to liters (1 m³ = 1000 liters)
        volume_liters = volume_m3 * 1000
        
        # Calculate time in seconds, then convert to hours
        seconds_to_drain = volume_liters / pump_rate
        hours_to_drain = seconds_to_drain / 3600
        
        return round(hours_to_drain, 2)
    
    def get_crop_water_advice(self, crop_name, soil_type, area):
        """
        Get water advice for specific crop
        
        Args:
            crop_name: Name of the crop
            soil_type: Type of soil (clay, sandy, loamy, silty)
            area: Area in acres
            
        Returns:
            Dictionary with water advice
        """
        crop_info = self.water_requirements.get(crop_name)
        if not crop_info:
            return None
            
        # Adjust based on soil type
        soil_factors = {
            'sandy': 1.2,  # Sandy soil needs more water
            'loamy': 1.0,
            'clay': 0.8,   # Clay retains water better
            'silty': 0.9
        }
        soil_factor = soil_factors.get(soil_type.lower(), 1.0)
        
        # Calculate water needed
        water_needed = crop_info['water_per_acre'] * area * soil_factor
        frequency = crop_info['frequency_days']
        best_time = crop_info['best_time']
        
        return {
            'water_needed': round(water_needed, 2),
            'frequency': frequency,
            'best_time': best_time,
            'soil_adjustment': f"{soil_factor}x ({soil_type})"
        }