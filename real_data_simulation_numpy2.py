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
                raw_data={"avg_position": 2.1, "dnf_rate": 0.08}
            ),
            RealPilot(
                name="Enea Bastianini", team="Ducati Lenovo Team", number=23, nationality="ITA",
                qualifying_pace=0.89, race_pace=0.94, start_performance=0.85, 
                overtaking=0.96, defending=0.88, wet_performance=0.87, consistency=0.88,
                career_wins=7, career_podiums=18, career_poles=2, championship_points=684,
                raw_data={"avg_position": 4.3, "dnf_rate": 0.12}
            ),
            
            # Pramac Ducati
            RealPilot(
                name="Jorge Martin", team="Prima Pramac Racing", number=89, nationality="ESP",
                qualifying_pace=0.99, race_pace=0.96, start_performance=0.96, 
                overtaking=0.92, defending=0.93, wet_performance=0.89, consistency=0.92,
                career_wins=12, career_podiums=36, career_poles=23, championship_points=1052,
                raw_data={"avg_position": 2.5, "dnf_rate": 0.10}
            ),
            RealPilot(
                name="Franco Morbidelli", team="Prima Pramac Racing", number=21, nationality="ITA",
                qualifying_pace=0.85, race_pace=0.87, start_performance=0.84, 
                overtaking=0.86, defending=0.85, wet_performance=0.88, consistency=0.89,
                career_wins=3, career_podiums=12, career_poles=4, championship_points=458,
                raw_data={"avg_position": 9.2, "dnf_rate": 0.15}
            ),
            
            # Gresini Ducati
            RealPilot(
                name="Marc Marquez", team="Gresini Racing MotoGP", number=93, nationality="ESP",
                qualifying_pace=0.95, race_pace=0.98, start_performance=0.94, 
                overtaking=0.99, defending=0.97, wet_performance=0.98, consistency=0.91,
                career_wins=85, career_podiums=140, career_poles=92, championship_points=3351,
                raw_data={"avg_position": 3.8, "dnf_rate": 0.18}
            ),
            RealPilot(
                name="Alex Marquez", team="Gresini Racing MotoGP", number=73, nationality="ESP",
                qualifying_pace=0.84, race_pace=0.86, start_performance=0.83, 
                overtaking=0.85, defending=0.84, wet_performance=0.82, consistency=0.87,
                career_wins=0, career_podiums=5, career_poles=0, championship_points=298,
                raw_data={"avg_position": 10.1, "dnf_rate": 0.14}
            ),
            
            # VR46 Ducati
            RealPilot(
                name="Marco Bezzecchi", team="VR46 Racing Team", number=72, nationality="ITA",
                qualifying_pace=0.88, race_pace=0.89, start_performance=0.86, 
                overtaking=0.90, defending=0.87, wet_performance=0.85, consistency=0.85,
                career_wins=3, career_podiums=10, career_poles=3, championship_points=367,
                raw_data={"avg_position": 7.6, "dnf_rate": 0.16}
            ),
            RealPilot(
                name="Fabio Di Giannantonio", team="VR46 Racing Team", number=49, nationality="ITA",
                qualifying_pace=0.86, race_pace=0.87, start_performance=0.82, 
                overtaking=0.84, defending=0.83, wet_performance=0.81, consistency=0.86,
                career_wins=1, career_podiums=3, career_poles=0, championship_points=214,
                raw_data={"avg_position": 9.8, "dnf_rate": 0.13}
            ),
            
            # Yamaha Factory
            RealPilot(
                name="Fabio Quartararo", team="Monster Energy Yamaha", number=20, nationality="FRA",
                qualifying_pace=0.89, race_pace=0.90, start_performance=0.88, 
                overtaking=0.91, defending=0.92, wet_performance=0.83, consistency=0.93,
                career_wins=11, career_podiums=33, career_poles=18, championship_points=1067,
                raw_data={"avg_position": 8.3, "dnf_rate": 0.07}
            ),
            RealPilot(
                name="Alex Rins", team="Monster Energy Yamaha", number=42, nationality="ESP",
                qualifying_pace=0.84, race_pace=0.86, start_performance=0.83, 
                overtaking=0.87, defending=0.85, wet_performance=0.84, consistency=0.82,
                career_wins=5, career_podiums=17, career_poles=4, championship_points=521,
                raw_data={"avg_position": 9.7, "dnf_rate": 0.16}
            ),
            
            # KTM Factory
            RealPilot(
                name="Brad Binder", team="Red Bull KTM Factory Racing", number=33, nationality="RSA",
                qualifying_pace=0.86, race_pace=0.92, start_performance=0.93, 
                overtaking=0.94, defending=0.90, wet_performance=0.86, consistency=0.89,
                career_wins=3, career_podiums=11, career_poles=0, championship_points=548,
                raw_data={"avg_position": 6.8, "dnf_rate": 0.09}
            ),
            RealPilot(
                name="Jack Miller", team="Red Bull KTM Factory Racing", number=43, nationality="AUS",
                qualifying_pace=0.87, race_pace=0.85, start_performance=0.90, 
                overtaking=0.89, defending=0.86, wet_performance=0.92, consistency=0.81,
                career_wins=4, career_podiums=22, career_poles=1, championship_points=627,
                raw_data={"avg_position": 10.2, "dnf_rate": 0.15}
            ),
            
            # Tech3 KTM
            RealPilot(
                name="Pedro Acosta", team="Red Bull GASGAS Tech3", number=31, nationality="ESP",
                qualifying_pace=0.90, race_pace=0.91, start_performance=0.87, 
                overtaking=0.93, defending=0.88, wet_performance=0.85, consistency=0.84,
                career_wins=1, career_podiums=3, career_poles=1, championship_points=192,
                raw_data={"avg_position": 7.4, "dnf_rate": 0.19}
            ),
            RealPilot(
                name="Augusto Fernandez", team="Red Bull GASGAS Tech3", number=37, nationality="ESP",
                qualifying_pace=0.81, race_pace=0.82, start_performance=0.80, 
                overtaking=0.81, defending=0.80, wet_performance=0.79, consistency=0.83,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=71,
                raw_data={"avg_position": 14.6, "dnf_rate": 0.12}
            ),
            
            # Aprilia Factory
            RealPilot(
                name="Aleix Espargaro", team="Aprilia Racing", number=41, nationality="ESP",
                qualifying_pace=0.91, race_pace=0.88, start_performance=0.85, 
                overtaking=0.86, defending=0.89, wet_performance=0.84, consistency=0.90,
                career_wins=3, career_podiums=11, career_poles=3, championship_points=712,
                raw_data={"avg_position": 8.1, "dnf_rate": 0.11}
            ),
            RealPilot(
                name="Maverick Vinales", team="Aprilia Racing", number=12, nationality="ESP",
                qualifying_pace=0.92, race_pace=0.89, start_performance=0.84, 
                overtaking=0.88, defending=0.87, wet_performance=0.86, consistency=0.85,
                career_wins=9, career_podiums=28, career_poles=13, championship_points=895,
                raw_data={"avg_position": 7.9, "dnf_rate": 0.13}
            ),
            
            # Trackhouse Aprilia
            RealPilot(
                name="Miguel Oliveira", team="Trackhouse Racing", number=88, nationality="POR",
                qualifying_pace=0.85, race_pace=0.87, start_performance=0.84, 
                overtaking=0.87, defending=0.85, wet_performance=0.89, consistency=0.84,
                career_wins=5, career_podiums=7, career_poles=0, championship_points=428,
                raw_data={"avg_position": 10.3, "dnf_rate": 0.14}
            ),
            RealPilot(
                name="Raul Fernandez", team="Trackhouse Racing", number=25, nationality="ESP",
                qualifying_pace=0.82, race_pace=0.83, start_performance=0.81, 
                overtaking=0.82, defending=0.81, wet_performance=0.80, consistency=0.82,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=65,
                raw_data={"avg_position": 13.8, "dnf_rate": 0.15}
            ),
            
            # Honda Factory
            RealPilot(
                name="Joan Mir", team="Repsol Honda Team", number=36, nationality="ESP",
                qualifying_pace=0.83, race_pace=0.85, start_performance=0.82, 
                overtaking=0.84, defending=0.86, wet_performance=0.88, consistency=0.87,
                career_wins=1, career_podiums=13, career_poles=2, championship_points=462,
                raw_data={"avg_position": 13.2, "dnf_rate": 0.17}
            ),
            RealPilot(
                name="Luca Marini", team="Repsol Honda Team", number=10, nationality="ITA",
                qualifying_pace=0.81, race_pace=0.80, start_performance=0.79, 
                overtaking=0.80, defending=0.81, wet_performance=0.78, consistency=0.83,
                career_wins=0, career_podiums=1, career_poles=0, championship_points=158,
                raw_data={"avg_position": 15.1, "dnf_rate": 0.13}
            ),
            
            # LCR Honda
            RealPilot(
                name="Johann Zarco", team="LCR Honda", number=5, nationality="FRA",
                qualifying_pace=0.84, race_pace=0.83, start_performance=0.85, 
                overtaking=0.83, defending=0.84, wet_performance=0.87, consistency=0.86,
                career_wins=0, career_podiums=15, career_poles=7, championship_points=532,
                raw_data={"avg_position": 12.7, "dnf_rate": 0.11}
            ),
            RealPilot(
                name="Takaaki Nakagami", team="LCR Honda", number=30, nationality="JPN",
                qualifying_pace=0.80, race_pace=0.81, start_performance=0.78, 
                overtaking=0.79, defending=0.80, wet_performance=0.77, consistency=0.82,
                career_wins=0, career_podiums=0, career_poles=0, championship_points=223,
                raw_data={"avg_position": 15.8, "dnf_rate": 0.12}
            ),
        ]
        
        # Sauvegarde des données
        with open(pilots_file, 'w', encoding='utf-8') as f:
            json.dump([p.__dict__ for p in pilots], f, ensure_ascii=False, indent=2)
            print(f"Données de {len(pilots)} pilotes sauvegardées dans {pilots_file}")
        
        return pilots
    
    def _load_or_create_circuits(self) -> List[RealCircuit]:
        """Charge ou crée les données des circuits"""
        circuits_file = f"{self.data_dir}/circuits.json"
        
        if os.path.exists(circuits_file):
            with open(circuits_file, 'r', encoding='utf-8') as f:
                circuits_data = json.load(f)
                circuits = [RealCircuit(**c) for c in circuits_data]
                print(f"Données de {len(circuits)} circuits chargées depuis {circuits_file}")
                return circuits
        
        # Création de données réelles pour les circuits MotoGP
        circuits = [
            RealCircuit(
                name="Losail International Circuit",
                country="Qatar",
                length=5380,
                corners=16,
                left_corners=6,
                right_corners=10,
                longest_straight=1068,
                circuit_record="1:52.772",
                record_holder="Francesco Bagnaia",
                layout=[
                    ("straight", 1068, 0.3),
                    ("corner", 250, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 180, 0.6),
                    ("straight", 500, 0.3),
                    ("corner", 200, 0.8),
                    ("straight", 400, 0.2),
                    ("corner", 150, 0.7),
                    ("straight", 600, 0.3),
                    ("corner", 220, 0.6),
                    ("straight", 350, 0.2),
                    ("corner", 180, 0.7),
                    ("straight", 400, 0.3),
                    ("corner", 150, 0.5),
                    ("straight", 300, 0.2),
                    ("corner", 130, 0.6)
                ]
            ),
            RealCircuit(
                name="Autódromo Internacional do Algarve",
                country="Portugal",
                length=4592,
                corners=15,
                left_corners=9,
                right_corners=6,
                longest_straight=969,
                circuit_record="1:38.725",
                record_holder="Francesco Bagnaia",
                layout=[
                    ("straight", 969, 0.3),
                    ("corner", 200, 0.8),
                    ("straight", 300, 0.2),
                    ("corner", 180, 0.7),
                    ("straight", 400, 0.3),
                    ("corner", 220, 0.9),
                    ("straight", 350, 0.2),
                    ("corner", 150, 0.6),
                    ("straight", 300, 0.3),
                    ("corner", 170, 0.7),
                    ("straight", 400, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 300, 0.2)
                ]
            ),
            RealCircuit(
                name="Circuit of the Americas",
                country="USA",
                length=5513,
                corners=20,
                left_corners=11,
                right_corners=9,
                longest_straight=1200,
                circuit_record="2:03.575",
                record_holder="Jorge Martin",
                layout=[
                    ("straight", 1200, 0.3),
                    ("corner", 180, 0.8),
                    ("straight", 250, 0.2),
                    ("corner", 150, 0.7),
                    ("straight", 300, 0.3),
                    ("corner", 200, 0.6),
                    ("straight", 350, 0.2),
                    ("corner", 170, 0.7),
                    ("straight", 400, 0.3),
                    ("corner", 220, 0.8),
                    ("straight", 300, 0.2),
                    ("corner", 150, 0.6),
                    ("straight", 250, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 350, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 300, 0.3),
                    ("corner", 150, 0.6),
                    ("straight", 250, 0.2),
                    ("corner", 180, 0.7)
                ]
            ),
            RealCircuit(
                name="Circuito de Jerez - Ángel Nieto",
                country="Spain",
                length=4423,
                corners=13,
                left_corners=8,
                right_corners=5,
                longest_straight=607,
                circuit_record="1:36.170",
                record_holder="Maverick Viñales",
                layout=[
                    ("straight", 607, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 150, 0.6),
                    ("straight", 400, 0.2),
                    ("corner", 220, 0.7),
                    ("straight", 300, 0.3),
                    ("corner", 170, 0.8),
                    ("straight", 350, 0.2),
                    ("corner", 180, 0.6),
                    ("straight", 400, 0.3)
                ]
            ),
            RealCircuit(
                name="Le Mans",
                country="France",
                length=4185,
                corners=14,
                left_corners=5,
                right_corners=9,
                longest_straight=674,
                circuit_record="1:31.778",
                record_holder="Johann Zarco",
                layout=[
                    ("straight", 674, 0.3),
                    ("corner", 150, 0.7),
                    ("straight", 250, 0.2),
                    ("corner", 180, 0.8),
                    ("straight", 300, 0.3),
                    ("corner", 200, 0.6),
                    ("straight", 350, 0.2),
                    ("corner", 170, 0.7),
                    ("straight", 400, 0.3),
                    ("corner", 220, 0.8),
                    ("straight", 300, 0.2),
                    ("corner", 150, 0.6),
                    ("straight", 250, 0.3),
                    ("corner", 180, 0.7)
                ]
            ),
            RealCircuit(
                name="Circuit de Barcelona-Catalunya",
                country="Spain",
                length=4655,
                corners=14,
                left_corners=8,
                right_corners=6,
                longest_straight=1047,
                circuit_record="1:39.027",
                record_holder="Aleix Espargaro",
                layout=[
                    ("straight", 1047, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 150, 0.6),
                    ("straight", 400, 0.2),
                    ("corner", 220, 0.7),
                    ("straight", 300, 0.3),
                    ("corner", 170, 0.8),
                    ("straight", 350, 0.2),
                    ("corner", 180, 0.6),
                    ("straight", 400, 0.3),
                    ("corner", 150, 0.7)
                ]
            ),
            RealCircuit(
                name="Mugello Circuit",
                country="Italy",
                length=5245,
                corners=15,
                left_corners=6,
                right_corners=9,
                longest_straight=1141,
                circuit_record="1:45.187",
                record_holder="Francesco Bagnaia",
                layout=[
                    ("straight", 1141, 0.3),
                    ("corner", 180, 0.8),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.7),
                    ("straight", 350, 0.3),
                    ("corner", 150, 0.6),
                    ("straight", 400, 0.2),
                    ("corner", 220, 0.8),
                    ("straight", 300, 0.3),
                    ("corner", 170, 0.7),
                    ("straight", 350, 0.2),
                    ("corner", 180, 0.6),
                    ("straight", 400, 0.3),
                    ("corner", 150, 0.8),
                    ("straight", 300, 0.2)
                ]
            ),
            RealCircuit(
                name="TT Circuit Assen",
                country="Netherlands",
                length=4542,
                corners=18,
                left_corners=6,
                right_corners=12,
                longest_straight=487,
                circuit_record="1:31.778",
                record_holder="Maverick Viñales",
                layout=[
                    ("straight", 487, 0.3),
                    ("corner", 150, 0.7),
                    ("straight", 250, 0.2),
                    ("corner", 180, 0.8),
                    ("straight", 300, 0.3),
                    ("corner", 200, 0.6),
                    ("straight", 350, 0.2),
                    ("corner", 170, 0.7),
                    ("straight", 250, 0.3),
                    ("corner", 220, 0.8),
                    ("straight", 300, 0.2),
                    ("corner", 150, 0.6),
                    ("straight", 250, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 170, 0.6)
                ]
            ),
            RealCircuit(
                name="Sachsenring",
                country="Germany",
                length=3671,
                corners=13,
                left_corners=10,
                right_corners=3,
                longest_straight=700,
                circuit_record="1:20.195",
                record_holder="Marc Marquez",
                layout=[
                    ("straight", 700, 0.3),
                    ("corner", 180, 0.8),
                    ("straight", 250, 0.2),
                    ("corner", 150, 0.7),
                    ("straight", 300, 0.3),
                    ("corner", 200, 0.6),
                    ("straight", 350, 0.2),
                    ("corner", 170, 0.8),
                    ("straight", 250, 0.3),
                    ("corner", 220, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 150, 0.6),
                    ("straight", 250, 0.3)
                ]
            ),
            RealCircuit(
                name="Silverstone Circuit",
                country="Great Britain",
                length=5900,
                corners=18,
                left_corners=8,
                right_corners=10,
                longest_straight=770,
                circuit_record="1:58.372",
                record_holder="Jorge Martin",
                layout=[
                    ("straight", 770, 0.3),
                    ("corner", 180, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 150, 0.6),
                    ("straight", 400, 0.2),
                    ("corner", 220, 0.7),
                    ("straight", 300, 0.3),
                    ("corner", 170, 0.8),
                    ("straight", 350, 0.2),
                    ("corner", 180, 0.6),
                    ("straight", 400, 0.3),
                    ("corner", 150, 0.7),
                    ("straight", 300, 0.2),
                    ("corner", 200, 0.8),
                    ("straight", 350, 0.3),
                    ("corner", 170, 0.6)
                ]
            ),
        ]
        
        # Sauvegarde des données
        with open(circuits_file, 'w', encoding='utf-8') as f:
            json.dump([c.__dict__ for c in circuits], f, ensure_ascii=False, indent=2)
            print(f"Données de {len(circuits)} circuits sauvegardées dans {circuits_file}")
        
        return circuits
    
    def _load_or_create_historical_results(self) -> Dict:
        """Charge ou crée les données historiques de résultats"""
        results_file = f"{self.data_dir}/historical_results.json"
        
        if os.path.exists(results_file):
            with open(results_file, 'r', encoding='utf-8') as f:
                historical_results = json.load(f)
                print(f"Données historiques chargées depuis {results_file}")
                return historical_results
        
        # Création de données historiques simulées
        historical_results = {
            "2024": {
                "Qatar": self._generate_race_result("Losail International Circuit"),
                "Portugal": self._generate_race_result("Autódromo Internacional do Algarve"),
                "Americas": self._generate_race_result("Circuit of the Americas"),
                "Spain": self._generate_race_result("Circuito de Jerez - Ángel Nieto"),
                "France": self._generate_race_result("Le Mans"),
                "Catalunya": self._generate_race_result("Circuit de Barcelona-Catalunya"),
                "Italy": self._generate_race_result("Mugello Circuit"),
                "Netherlands": self._generate_race_result("TT Circuit Assen"),
                "Germany": self._generate_race_result("Sachsenring"),
                "Great Britain": self._generate_race_result("Silverstone Circuit")
            }
        }
        
        # Sauvegarde des données
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(historical_results, f, ensure_ascii=False, indent=2)
            print(f"Données historiques sauvegardées dans {results_file}")
        
        return historical_results
    
    def _generate_race_result(self, circuit_name: str) -> List[Dict]:
        """Génère un résultat de course simulé pour un circuit donné"""
        # Trouver le circuit
        circuit = next((c for c in self.circuits if c.name == circuit_name), None)
        if not circuit:
            return []
        
        # Simuler les qualifications
        qualifying_results = sorted(
            [(p, p.qualifying_pace + random.uniform(-0.05, 0.05)) for p in self.pilots],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Simuler la course
        race_results = []
        dnf_pilots = []
        
        # Déterminer les abandons (DNF)
        for pilot, _ in qualifying_results:
            dnf_chance = pilot.raw_data.get("dnf_rate", 0.1)
            if random.random() < dnf_chance:
                dnf_pilots.append(pilot.name)
        
        # Calculer les temps de course pour les pilotes qui terminent
        for position, (pilot, quali_pace) in enumerate(qualifying_results, 1):
            if pilot.name in dnf_pilots:
                race_results.append({
                    "position": "DNF",
                    "name": pilot.name,
                    "team": pilot.team,
                    "number": pilot.number,
                    "nationality": pilot.nationality,
                    "grid": position,
                    "status": "Accident" if random.random() < 0.7 else "Technical",
                    "points": 0
                })
                continue
            
            # Calculer le temps total basé sur les performances
            base_time = 100  # Temps de base en secondes
            
            # Facteurs de performance
            performance_factor = (
                0.5 * pilot.race_pace +
                0.2 * pilot.consistency +
                0.1 * pilot.overtaking +
                0.1 * pilot.defending +
                0.1 * (1 - abs(position - 10) / 20)  # Bonus pour les positions médianes
            )
            
            # Calculer le temps final
            race_time = base_time * (2 - performance_factor) * (1 + random.uniform(-0.02, 0.02))
            
            # Points selon la position
            points_map = {1: 25, 2: 20, 3: 16, 4: 13, 5: 11, 6: 10, 7: 9, 8: 8, 9: 7, 10: 6,
                         11: 5, 12: 4, 13: 3, 14: 2, 15: 1}
            
            race_results.append({
                "position": position,
                "name": pilot.name,
                "team": pilot.team,
                "number": pilot.number,
                "nationality": pilot.nationality,
                "grid": position,
                "time": race_time,
                "gap": race_time - base_time if position > 1 else 0,
                "points": points_map.get(position, 0),
                "fastest_lap": position == 1 or random.random() < 0.1
            })
        
        # Trier par position (DNF à la fin)
        finished_results = [r for r in race_results if r["position"] != "DNF"]
        dnf_results = [r for r in race_results if r["position"] == "DNF"]
        
        finished_results.sort(key=lambda x: x["position"])
        
        return finished_results + dnf_results
    
    def simulate_qualifying(self, circuit_name: str, weather_condition: str = "dry") -> pd.DataFrame:
        """Simule une séance de qualification sur un circuit donné"""
        # Trouver le circuit
        circuit = next((c for c in self.circuits if c.name == circuit_name), None)
        if not circuit:
            raise ValueError(f"Circuit {circuit_name} non trouvé")
        
        # Facteurs météo
        weather_factor = 1.0
        if weather_condition == "wet":
            weather_factor = 0.9  # Piste mouillée = plus lent
        elif weather_condition == "mixed":
            weather_factor = 0.95  # Conditions mixtes
        
        # Simuler Q1
        all_pilots = self.pilots.copy()
        q1_results = []
        
        for pilot in all_pilots:
            # Performance de base
            base_performance = pilot.qualifying_pace
            
            # Ajustement météo
            if weather_condition == "wet":
                performance = base_performance * 0.7 + pilot.wet_performance * 0.3
            else:
                performance = base_performance
            
            # Variabilité
            variability = random.uniform(-0.03, 0.03)
            
            # Temps au tour
            lap_time = (100 - performance * 20) * (1 + variability) * weather_factor
            
            q1_results.append({
                "name": pilot.name,
                "team": pilot.team,
                "number": pilot.number,
                "nationality": pilot.nationality,
                "lap_time": lap_time
            })
        
        # Trier par temps au tour
        q1_results.sort(key=lambda x: x["lap_time"])
        
        # Ajouter les positions
        for i, result in enumerate(q1_results):
            result["position"] = i + 1
        
        # Convertir en DataFrame
        qualifying_df = pd.DataFrame(q1_results)
        
        return qualifying_df
    
    def simulate_race(self, circuit_name: str, qualifying_results: pd.DataFrame, 
                     weather_condition: str = "dry", race_laps: int = 20) -> pd.DataFrame:
        """Simule une course complète basée sur les résultats des qualifications"""
        # Trouver le circuit
        circuit = next((c for c in self.circuits if c.name == circuit_name), None)
        if not circuit:
            raise ValueError(f"Circuit {circuit_name} non trouvé")
        
        # Facteurs météo
        weather_factor = 1.0
        if weather_condition == "wet":
            weather_factor = 0.9  # Piste mouillée = plus lent
        elif weather_condition == "mixed":
            weather_factor = 0.95  # Conditions mixtes
        
        # Préparer les données de course
        race_data = []
        
        # Grille de départ basée sur les qualifications
        grid = qualifying_results.sort_values("position").copy()
        
        # Déterminer les abandons (DNF)
        dnf_pilots = []
        dnf_laps = {}
        
        for _, row in grid.iterrows():
            pilot = next((p for p in self.pilots if p.name == row["name"]), None)
            if pilot:
                dnf_chance = pilot.raw_data.get("dnf_rate", 0.1)
                if random.random() < dnf_chance:
                    dnf_pilots.append(pilot.name)
                    # Déterminer le tour d'abandon
                    dnf_laps[pilot.name] = random.randint(1, race_laps - 1)
        
        # Simuler chaque tour
        positions = {row["name"]: idx + 1 for idx, row in grid.iterrows()}
        
        for lap in range(1, race_laps + 1):
            # Calculer les temps au tour pour chaque pilote
            lap_times = {}
            
            for _, row in grid.iterrows():
                pilot_name = row["name"]
                
                # Vérifier si le pilote a abandonné avant ce tour
                if pilot_name in dnf_pilots and dnf_laps[pilot_name] < lap:
                    continue
                
                pilot = next((p for p in self.pilots if p.name == pilot_name), None)
                if not pilot:
                    continue
                
                # Position actuelle
                current_position = positions[pilot_name]
                
                # Performance de base
                base_performance = pilot.race_pace
                
                # Ajustements
                if weather_condition == "wet":
                    performance = base_performance * 0.7 + pilot.wet_performance * 0.3
                else:
                    performance = base_performance
                
                # Facteur de position (plus difficile de remonter depuis l'arrière)
                position_factor = 1 - (current_position - 1) * 0.005
                
                # Usure des pneus
                tire_wear = lap / race_laps * 0.1
                tire_factor = 1 - tire_wear * (1 - pilot.consistency * 0.5)
                
                # Variabilité
                variability = random.uniform(-0.02, 0.02)
                
                # Temps au tour
                lap_time = (100 - performance * 20) * position_factor * tire_factor * (1 + variability) * weather_factor
                
                # Enregistrer le temps au tour
                lap_times[pilot_name] = lap_time
                
                # Ajouter aux données de course
                race_data.append({
                    "lap": lap,
                    "name": pilot_name,
                    "team": pilot.team,
                    "position": current_position,
                    "lap_time": lap_time,
                    "status": "Running"
                })
            
            # Mettre à jour les positions pour le prochain tour (sauf au dernier tour)
            if lap < race_laps:
                # Trier les pilotes par temps cumulé
                active_pilots = [p for p in positions.keys() if p not in dnf_pilots or dnf_laps[p] >= lap]
                active_pilots.sort(key=lambda p: lap_times.get(p, float('inf')))
                
                # Mettre à jour les positions
                for pos, pilot_name in enumerate(active_pilots, 1):
                    positions[pilot_name] = pos
            
            # Ajouter les DNF pour ce tour
            for pilot_name in dnf_pilots:
                if dnf_laps[pilot_name] == lap:
                    pilot = next((p for p in self.pilots if p.name == pilot_name), None)
                    if pilot:
                        race_data.append({
                            "lap": lap,
                            "name": pilot_name,
                            "team": pilot.team,
                            "position": None,
                            "lap_time": None,
                            "status": "DNF - Accident" if random.random() < 0.7 else "DNF - Technical"
                        })
        
        # Convertir en DataFrame
        race_df = pd.DataFrame(race_data)
        
        # Calculer les temps cumulés
        race_df["cumulative_time"] = race_df.groupby("name")["lap_time"].cumsum()
        
        return race_df
    
    def analyze_race_results(self, race_df: pd.DataFrame, qualifying_df: pd.DataFrame) -> Dict:
        """Analyse les résultats d'une course"""
        # Extraire le dernier tour pour chaque pilote
        final_lap = race_df.groupby("name")["lap"].max().reset_index()
        final_results = []
        
        for _, row in final_lap.iterrows():
            pilot_name = row["name"]
            max_lap = row["lap"]
            
            # Données du dernier tour du pilote
            last_lap_data = race_df[(race_df["name"] == pilot_name) & (race_df["lap"] == max_lap)].iloc[0]
            
            # Position de qualification
            quali_position = qualifying_df[qualifying_df["name"] == pilot_name]["position"].values[0]
            
            # Statut final
            status = last_lap_data["status"]
            
            # Points selon la position
            points_map = {1: 25, 2: 20, 3: 16, 4: 13, 5: 11, 6: 10, 7: 9, 8: 8, 9: 7, 10: 6,
                         11: 5, 12: 4, 13: 3, 14: 2, 15: 1}
            
            position = last_lap_data["position"]
            points = points_map.get(position, 0) if position and status == "Running" else 0
            
            final_results.append({
                "name": pilot_name,
                "team": last_lap_data["team"],
                "final_position": int(position) if position and not pd.isna(position) else None,
                "qualifying_position": int(quali_position) if not pd.isna(quali_position) else None,
                "status": status,
                "points": int(points) if not pd.isna(points) else 0,
                "laps_completed": int(max_lap) if not pd.isna(max_lap) else 0
            })
        
        # Trier par position finale (DNF à la fin)
        running_results = [r for r in final_results if r["status"] == "Running"]
        dnf_results = [r for r in final_results if r["status"] != "Running"]
        
        running_results.sort(key=lambda x: x["final_position"] if x["final_position"] is not None else float('inf'))
        
        final_classification = running_results + dnf_results
        
        # Trouver le meilleur tour
        valid_laps = race_df[race_df["status"] == "Running"].copy()
        if not valid_laps.empty:
            best_lap_idx = valid_laps["lap_time"].idxmin()
            best_lap = valid_laps.loc[best_lap_idx]
            
            best_lap_info = {
                "name": best_lap["name"],
                "team": best_lap["team"],
                "lap": int(best_lap["lap"]),  # Convertir en int standard
                "time": float(best_lap["lap_time"])  # Convertir en float standard
            }
        else:
            best_lap_info = None
        
        # Statistiques générales
        stats = {
            "avg_lap_time": float(valid_laps["lap_time"].mean()) if not valid_laps.empty else None,
            "std_lap_time": float(valid_laps["lap_time"].std()) if not valid_laps.empty else None,
            "dnf_count": len(dnf_results),
            "dnf_rate": float(len(dnf_results) / len(final_results)) if final_results else 0
        }
        
        return {
            "final_classification": final_classification,
            "best_lap": best_lap_info,
            "statistics": stats,
            "race_data": race_df
        }
    
    def visualize_race_analysis(self, race_results: Dict, circuit_name: str, 
                              weather_condition: str) -> None:
        """Visualise l'analyse de la course avec des graphiques"""
        race_df = race_results["race_data"]
        final_classification = pd.DataFrame(race_results["final_classification"])
        
        # Créer une figure avec plusieurs sous-graphiques
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Analyse de Course MotoGP - {circuit_name} ({weather_condition})', 
                    fontsize=16, fontweight='bold')
        
        # 1. Évolution des positions pour le top 6
        ax1 = axes[0, 0]
        top_6_pilots = final_classification.head(6)["name"].tolist()
        colors = plt.cm.tab10(np.linspace(0, 1, 10))[:6]
        
        for i, pilot_name in enumerate(top_6_pilots):
            pilot_data = race_df[race_df["name"] == pilot_name]
            if not pilot_data.empty and "position" in pilot_data.columns:
                valid_data = pilot_data[pilot_data["position"].notna()]
                if not valid_data.empty:
                    ax1.plot(valid_data["lap"], valid_data["position"], 
                            marker='o', linewidth=2, markersize=4, 
                            label=pilot_name, color=colors[i])
        
        ax1.set_xlabel('Tour')
        ax1.set_ylabel('Position')
        ax1.set_title('Évolution des positions - Top 6')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.invert_yaxis()  # Position 1 en haut
        
        # 2. Temps au tour pour le top 6
        ax2 = axes[0, 1]
        
        for i, pilot_name in enumerate(top_6_pilots):
            pilot_data = race_df[race_df["name"] == pilot_name]
            if not pilot_data.empty and "lap_time" in pilot_data.columns:
                valid_data = pilot_data[pilot_data["lap_time"].notna()]
                if not valid_data.empty:
                    ax2.plot(valid_data["lap"], valid_data["lap_time"], 
                            marker='o', linewidth=2, markersize=4, 
                            label=pilot_name, color=colors[i])
        
        ax2.set_xlabel('Tour')
        ax2.set_ylabel('Temps au tour')
        ax2.set_title('Évolution des temps au tour - Top 6')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 3. Écarts par rapport au leader
        ax3 = axes[1, 0]
        
        # Trouver le leader à chaque tour
        leader_times = {}
        for lap in race_df["lap"].unique():
            lap_data = race_df[race_df["lap"] == lap]
            if not lap_data.empty:
                positions = lap_data[lap_data["position"] == 1]
                if not positions.empty:
                    leader = positions.iloc[0]
                    leader_times[lap] = leader["cumulative_time"]
        
        for i, pilot_name in enumerate(top_6_pilots[1:], 1):  # Exclure le leader
            pilot_data = race_df[race_df["name"] == pilot_name]
            if not pilot_data.empty and "cumulative_time" in pilot_data.columns:
                gaps = []
                laps = []
                
                for _, row in pilot_data.iterrows():
                    lap = row["lap"]
                    if lap in leader_times and not pd.isna(row["cumulative_time"]):
                        gap = row["cumulative_time"] - leader_times[lap]
                        gaps.append(gap)
                        laps.append(lap)
                
                if gaps:
                    ax3.plot(laps, gaps, 
                            marker='o', linewidth=2, markersize=4, 
                            label=pilot_name, color=colors[i])
        
        ax3.set_xlabel('Tour')
        ax3.set_ylabel('Écart au leader (s)')
        ax3.set_title('Évolution des écarts au leader')
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.3)
        
        # 4. Distribution des temps au tour par équipe
        ax4 = axes[1, 1]
        
        teams = race_df["team"].unique()
        team_lap_times = []
        team_labels = []
        
        for team in teams:
            team_data = race_df[race_df["team"] == team]
            if not team_data.empty and "lap_time" in team_data.columns:
                valid_times = team_data["lap_time"].dropna()
                if not valid_times.empty:
                    team_lap_times.append(valid_times)
                    team_labels.append(team)
        
        if team_lap_times:
            ax4.boxplot(team_lap_times, tick_labels=team_labels)  # Utiliser tick_labels au lieu de labels
            ax4.set_ylabel('Temps au tour')
            ax4.set_title('Distribution des temps au tour par équipe')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        
        # Sauvegarder le graphique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"{self.data_dir}/race_analysis_{timestamp}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Analyse graphique sauvegardée dans {self.data_dir}/race_analysis_{timestamp}.png")
    
    def cluster_pilots_by_performance(self) -> Dict:
        """Groupe les pilotes par performances similaires"""
        # Préparer les données pour le clustering
        performance_data = []
        for pilot in self.pilots:
            performance_data.append([
                pilot.qualifying_pace,
                pilot.race_pace,
                pilot.start_performance,
                pilot.overtaking,
                pilot.defending,
                pilot.wet_performance,
                pilot.consistency
            ])
        
        # Normaliser les données
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(performance_data)
        
        # Appliquer K-means
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        # Organiser les résultats
        cluster_results = {0: [], 1: [], 2: [], 3: []}
        
        for i, pilot in enumerate(self.pilots):
            cluster_id = clusters[i]
            cluster_results[cluster_id].append({
                "name": pilot.name,
                "team": pilot.team,
                "qualifying_pace": pilot.qualifying_pace,
                "race_pace": pilot.race_pace,
                "consistency": pilot.consistency,
                "career_wins": pilot.career_wins
            })
        
        # Trier chaque cluster par race_pace
        for cluster_id in cluster_results:
            cluster_results[cluster_id].sort(key=lambda x: x["race_pace"], reverse=True)
        
        return cluster_results
    
    # Fonction auxiliaire pour convertir les types numpy en types Python standards
    def _convert_to_serializable(self, obj):
        """Convertit les types numpy en types Python standards pour la sérialisation JSON"""
        # NumPy 2.0 compatibility
        if hasattr(np, 'integer') and isinstance(obj, np.integer):
            return int(obj)
        elif hasattr(np, 'floating') and isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.int64) or isinstance(obj, np.int32) or isinstance(obj, np.int16) or isinstance(obj, np.int8):
            return int(obj)
        elif isinstance(obj, np.float64) or isinstance(obj, np.float32) or isinstance(obj, np.float16):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(i) for i in obj]
        else:
            return obj
    
    def run_complete_simulation(self, circuit_name: str, weather_condition: str = "dry") -> Dict:
        """Exécute une simulation complète: qualification + course + analyse"""
        print(f"\nSimulation MotoGP - {circuit_name} ({weather_condition})")
        print("=" * 60)
        
        # 1. Qualification
        print("\nSimulation des qualifications...")
        qualifying_results = self.simulate_qualifying(circuit_name, weather_condition)
        
        print("\nRésultats des qualifications (Top 10):")
        for _, row in qualifying_results.head(10).iterrows():
            print(f"{int(row['position']):2d}. {row['name']:<20} - {row['lap_time']:.3f}s")
        
        # 2. Course
        print("\nSimulation de la course...")
        race_results_df = self.simulate_race(circuit_name, qualifying_results, weather_condition)
        
        # 3. Analyse
        print("\nAnalyse des résultats...")
        race_analysis = self.analyze_race_results(race_results_df, qualifying_results)
        
        # 4. Affichage des résultats
        print("\nCLASSEMENT FINAL")
        print("=" * 60)
        
        for result in race_analysis["final_classification"]:
            if result["status"] == "Running":
                position = result["final_position"]
                quali_pos = result["qualifying_position"]
                print(f"{position:2d}. {result['name']:<20} - {result['points']} pts (Q: {quali_pos})")
            else:
                quali_pos = result["qualifying_position"]
                laps = result["laps_completed"]
                print(f"DNF. {result['name']:<20} - {result['status']} (Q: {quali_pos}, Tours: {laps})")
        
        if race_analysis["best_lap"]:
            print(f"\nMEILLEUR TOUR: {race_analysis['best_lap']['name']} - "
                 f"Tour {race_analysis['best_lap']['lap']} - "
                 f"{race_analysis['best_lap']['time']:.3f}s")
        
        # 5. Visualisation
        print("\nGénération des graphiques d'analyse...")
        self.visualize_race_analysis(race_analysis, circuit_name, weather_condition)
        
        # 6. Sauvegarde des résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{self.data_dir}/race_results_{timestamp}.json"
        
        # Convertir les données en types Python standards pour la sérialisation JSON
        serializable_race_analysis = self._convert_to_serializable(race_analysis)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_race_analysis, f, ensure_ascii=False, indent=2)
        
        print(f"\nRésultats sauvegardés dans {results_file}")
        
        return race_analysis

# Exécution du programme principal
if __name__ == "__main__":
    print("MotoGP - Simulateur basé sur des données réelles")
    print("=" * 50)
    
    # Créer le simulateur
    simulator = MotoGPRealDataSimulator()
    
    # Afficher les pilotes disponibles
    print(f"\nPilotes ({len(simulator.pilots)}):")
    for i, pilot in enumerate(simulator.pilots, 1):
        print(f"{i:2d}. {pilot.name:<20} ({pilot.team})")
    
    # Afficher les circuits disponibles
    print(f"\nCircuits ({len(simulator.circuits)}):")
    for i, circuit in enumerate(simulator.circuits, 1):
        print(f"{i:2d}. {circuit.name:<30} ({circuit.country})")
    
    # Analyse des pilotes par clusters de performance
    print("\nAnalyse des groupes de performance:")
    clusters = simulator.cluster_pilots_by_performance()
    
    for cluster_id, pilots in clusters.items():
        if pilots:
            avg_pace = sum(p["race_pace"] for p in pilots) / len(pilots)
            print(f"\nGroupe {cluster_id+1} (Niveau de performance: {avg_pace:.2f}):")
            for pilot in pilots:
                print(f"  - {pilot['name']:<20} ({pilot['team']}) - Victoires: {pilot['career_wins']}")
    
    # Simulation d'une course complète
    print("\nLancement d'une simulation complète...")
    race_analysis = simulator.run_complete_simulation("Mugello Circuit", "dry")
    
    print("\nSimulation terminée!")