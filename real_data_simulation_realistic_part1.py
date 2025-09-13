import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import os
import requests
import json
from datetime import datetime
import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Configuration des graphiques en français
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

@dataclass
class RealPilot:
    """Profil d'un pilote MotoGP basé sur des données réelles"""
    name: str
    team: str
    number: int
    nationality: str
    
    # Statistiques de performance (normalisées entre 0 et 1)
    qualifying_pace: float    # Performance en qualification
    race_pace: float          # Performance en course
    start_performance: float  # Performance au départ
    overtaking: float         # Capacité à dépasser
    defending: float          # Capacité à défendre sa position
    wet_performance: float    # Performance sur piste mouillée
    consistency: float        # Régularité
    
    # Statistiques de carrière
    career_wins: int
    career_podiums: int
    career_poles: int
    championship_points: int
    
    # Données brutes pour l'analyse
    raw_data: Dict = None

@dataclass
class RealCircuit:
    """Circuit réel avec ses caractéristiques"""
    name: str
    country: str
    length: float  # en mètres
    corners: int
    left_corners: int
    right_corners: int
    longest_straight: float  # en mètres
    circuit_record: Optional[str] = None  # en secondes (format chaîne)
    record_holder: Optional[str] = None
    layout: List[Tuple[str, float, float]] = None  # (type, longueur, difficulté)

class MotoGPRealDataSimulator:
    def __init__(self):
        """Initialise le simulateur avec des données réelles"""
        self.data_dir = "simulations/real_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Chargement ou création des données
        self.pilots = self._load_or_create_pilots()
        self.circuits = self._load_or_create_circuits()
        self.historical_results = self._load_or_create_historical_results()
        
        # Facteurs d'influence pour la simulation
        self.weather_influence = 0.15  # Influence de la météo
        self.qualifying_influence = 0.25  # Influence de la position de départ
        self.random_factor = 0.05  # Facteur aléatoire (incidents, chance)
    
    def _load_or_create_pilots(self) -> List[RealPilot]:
        """Charge ou crée les données des pilotes"""
        pilots_file = f"{self.data_dir}/pilots.json"
        
        if os.path.exists(pilots_file):
            with open(pilots_file, 'r', encoding='utf-8') as f:
                pilots_data = json.load(f)
                pilots = [RealPilot(**p) for p in pilots_data]
                print(f"Données de {len(pilots)} pilotes chargées depuis {pilots_file}")
                return pilots
        
        # Création de données réalistes pour les pilotes 2024-2025
        pilots = [
            # Ducati Factory
            RealPilot(
                name="Francesco Bagnaia", team="Ducati Lenovo Team", number=1, nationality="ITA",
                qualifying_pace=0.98, race_pace=0.97, start_performance=0.92, 
                overtaking=0.94, defending=0.95, wet_performance=0.90, consistency=0.96,
                career_wins=25, career_podiums=58, career_poles=18, championship_points=1267,
                raw_data={"avg_position": 2.1, "dnf_rate": 0.15}  # Augmenté
            ),
            RealPilot(
                name="Enea Bastianini", team="Ducati Lenovo Team", number=23, nationality="ITA",
                qualifying_pace=0.89, race_pace=0.94, start_performance=0.85, 
                overtaking=0.96, defending=0.88, wet_performance=0.87, consistency=0.88,
                career_wins=7, career_podiums=18, career_poles=2, championship_points=684,
                raw_data={"avg_position": 4.3, "dnf_rate": 0.18}  # Augmenté
            ),
            
            # Pramac Ducati
            RealPilot(
                name="Jorge Martin", team="Prima Pramac Racing", number=89, nationality="ESP",
                qualifying_pace=0.99, race_pace=0.96, start_performance=0.96, 
                overtaking=0.92, defending=0.93, wet_performance=0.89, consistency=0.92,
                career_wins=12, career_podiums=36, career_poles=23, championship_points=1052,
                raw_data={"avg_position": 2.5, "dnf_rate": 0.17}  # Augmenté
            ),
            RealPilot(
                name="Franco Morbidelli", team="Prima Pramac Racing", number=21, nationality="ITA",
                qualifying_pace=0.85, race_pace=0.87, start_performance=0.84, 
                overtaking=0.86, defending=0.85, wet_performance=0.88, consistency=0.89,
                career_wins=3, career_podiums=12, career_poles=4, championship_points=458,
                raw_data={"avg_position": 9.2, "dnf_rate": 0.20}  # Augmenté
            ),
            
            # Gresini Ducati
            RealPilot(
                name="Marc Marquez", team="Gresini Racing MotoGP", number=93, nationality="ESP",
                qualifying_pace=0.95, race_pace=0.98, start_performance=0.94, 
                overtaking=0.99, defending=0.97, wet_performance=0.98, consistency=0.91,
                career_wins=85, career_podiums=140, career_poles=92, championship_points=3351,
                raw_data={"avg_position": 3.8, "dnf_rate": 0.25}  # Augmenté
            ),
            RealPilot(
                name="Alex Marquez", team="Gresini Racing MotoGP", number=73, nationality="ESP",
                qualifying_pace=0.84, race_pace=0.86, start_performance=0.83, 
                overtaking=0.85, defending=0.84, wet_performance=0.82, consistency=0.87,
                career_wins=0, career_podiums=5, career_poles=0, championship_points=298,
                raw_data={"avg_position": 10.1, "dnf_rate": 0.19}  # Augmenté
            ),
            
            # VR46 Ducati
            RealPilot(
                name="Marco Bezzecchi", team="VR46 Racing Team", number=72, nationality="ITA",
                qualifying_pace=0.88, race_pace=0.89, start_performance=0.86, 
                overtaking=0.90, defending=0.87, wet_performance=0.85, consistency=0.85,
                career_wins=3, career_podiums=10, career_poles=3, championship_points=367,
                raw_data={"avg_position": 7.6, "dnf_rate": 0.22}  # Augmenté
            ),
            RealPilot(
                name="Fabio Di Giannantonio", team="VR46 Racing Team", number=49, nationality="ITA",
                qualifying_pace=0.86, race_pace=0.87, start_performance=0.82, 
                overtaking=0.84, defending=0.83, wet_performance=0.81, consistency=0.86,
                career_wins=1, career_podiums=3, career_poles=0, championship_points=214,
                raw_data={"avg_position": 9.8, "dnf_rate": 0.18}  # Augmenté
            ),
            
            # Yamaha Factory
            RealPilot(
                name="Fabio Quartararo", team="Monster Energy Yamaha", number=20, nationality="FRA",
                qualifying_pace=0.89, race_pace=0.90, start_performance=0.88, 
                overtaking=0.91, defending=0.92, wet_performance=0.83, consistency=0.93,
                career_wins=11, career_podiums=33, career_poles=18, championship_points=1067,
                raw_data={"avg_position": 8.3, "dnf_rate": 0.14}  # Augmenté
            ),
            RealPilot(
                name="Alex Rins", team="Monster Energy Yamaha", number=42, nationality="ESP",
                qualifying_pace=0.84, race_pace=0.86, start_performance=0.83, 
                overtaking=0.87, defending=0.85, wet_performance=0.84, consistency=0.82,
                career_wins=5, career_podiums=17, career_poles=4, championship_points=521,
                raw_data={"avg_position": 9.7, "dnf_rate": 0.21}  # Augmenté
            ),
            
            # KTM Factory
            RealPilot(
                name="Brad Binder", team="Red Bull KTM Factory Racing", number=33, nationality="RSA",
                qualifying_pace=0.86, race_pace=0.92, start_performance=0.93, 
                overtaking=0.94, defending=0.90, wet_performance=0.86, consistency=0.89,
                career_wins=3, career_podiums=11, career_poles=0, championship_points=548,
                raw_data={"avg_position": 6.8, "dnf_rate": 0.16}  # Augmenté
            ),
            RealPilot(
                name="Jack Miller", team="Red Bull KTM Factory Racing", number=43, nationality="AUS",
                qualifying_pace=0.87, race_pace=0.85, start_performance=0.90, 
                overtaking=0.89, defending=0.86, wet_performance=0.92, consistency=0.81,
                career_wins=4, career_podiums=22, career_poles=1, championship_points=627,
                raw_data={"avg_position": 10.2, "dnf_rate": 0.22}  # Augmenté
            ),
            
            # Tech3 KTM
            RealPilot(
                name="Pedro Acosta", team="Red Bull GASGAS Tech3", number=31, nationality="ESP",
                qualifying_pace=0.90, race_pace=0.91, start_performance=0.87, 
                overtaking=0.93, defending=0.88, wet_performance=0.85, consistency=0.84,
                career_wins=1, career_podiums=3, career_poles=1, championship_points=192,
                raw_data={"avg_position": 7.4, "dnf_rate": 0.26}  # Augmenté
            ),
            RealPilot(
                name="Augusto Fernandez", team="Red Bull GASGAS Tech3", number=37, nationality="ESP",
                qualifying_pace=0.81, race_pace=0.82, start_performance=0.80, 
                overtaking=0.81, defending=0.80, wet_performance=0.79, consistency=0.83,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=71,
                raw_data={"avg_position": 14.6, "dnf_rate": 0.19}  # Augmenté
            ),
            
            # Aprilia Factory
            RealPilot(
                name="Aleix Espargaro", team="Aprilia Racing", number=41, nationality="ESP",
                qualifying_pace=0.91, race_pace=0.88, start_performance=0.85, 
                overtaking=0.86, defending=0.89, wet_performance=0.84, consistency=0.90,
                career_wins=3, career_podiums=11, career_poles=3, championship_points=712,
                raw_data={"avg_position": 8.1, "dnf_rate": 0.17}  # Augmenté
            ),
            RealPilot(
                name="Maverick Vinales", team="Aprilia Racing", number=12, nationality="ESP",
                qualifying_pace=0.92, race_pace=0.89, start_performance=0.84, 
                overtaking=0.88, defending=0.87, wet_performance=0.86, consistency=0.85,
                career_wins=9, career_podiums=28, career_poles=13, championship_points=895,
                raw_data={"avg_position": 7.9, "dnf_rate": 0.20}  # Augmenté
            ),
            
            # Trackhouse Aprilia
            RealPilot(
                name="Miguel Oliveira", team="Trackhouse Racing", number=88, nationality="POR",
                qualifying_pace=0.85, race_pace=0.87, start_performance=0.84, 
                overtaking=0.87, defending=0.85, wet_performance=0.89, consistency=0.84,
                career_wins=5, career_podiums=7, career_poles=0, championship_points=428,
                raw_data={"avg_position": 10.3, "dnf_rate": 0.19}  # Augmenté
            ),
            RealPilot(
                name="Raul Fernandez", team="Trackhouse Racing", number=25, nationality="ESP",
                qualifying_pace=0.82, race_pace=0.83, start_performance=0.81, 
                overtaking=0.82, defending=0.81, wet_performance=0.80, consistency=0.82,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=65,
                raw_data={"avg_position": 13.8, "dnf_rate": 0.21}  # Augmenté
            ),
            
            # Honda Factory
            RealPilot(
                name="Joan Mir", team="Repsol Honda Team", number=36, nationality="ESP",
                qualifying_pace=0.83, race_pace=0.85, start_performance=0.82, 
                overtaking=0.84, defending=0.86, wet_performance=0.88, consistency=0.87,
                career_wins=1, career_podiums=13, career_poles=2, championship_points=462,
                raw_data={"avg_position": 13.2, "dnf_rate": 0.23}  # Augmenté
            ),
            RealPilot(
                name="Luca Marini", team="Repsol Honda Team", number=10, nationality="ITA",
                qualifying_pace=0.81, race_pace=0.80, start_performance=0.79, 
                overtaking=0.80, defending=0.81, wet_performance=0.78, consistency=0.83,
                career_wins=0, career_podiums=1, career_poles=0, championship_points=158,
                raw_data={"avg_position": 15.1, "dnf_rate": 0.20}  # Augmenté
            ),
            
            # LCR Honda
            RealPilot(
                name="Johann Zarco", team="LCR Honda", number=5, nationality="FRA",
                qualifying_pace=0.84, race_pace=0.83, start_performance=0.85, 
                overtaking=0.83, defending=0.84, wet_performance=0.87, consistency=0.86,
                career_wins=0, career_podiums=15, career_poles=7, championship_points=532,
                raw_data={"avg_position": 12.7, "dnf_rate": 0.18}  # Augmenté
            ),
            RealPilot(
                name="Takaaki Nakagami", team="LCR Honda", number=30, nationality="JPN",
                qualifying_pace=0.80, race_pace=0.81, start_performance=0.78, 
                overtaking=0.79, defending=0.80, wet_performance=0.77, consistency=0.82,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=223,
                raw_data={"avg_position": 15.8, "dnf_rate": 0.19}  # Augmenté
            ),
        ]
        
        # Sauvegarde des données
        with open(pilots_file, 'w', encoding='utf-8') as f:
            json.dump([p.__dict__ for p in pilots], f, ensure_ascii=False, indent=2)
            print(f"Données de {len(pilots)} pilotes sauvegardées dans {pilots_file}")
        
        return pilots