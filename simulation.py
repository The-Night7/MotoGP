import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple
import random

# Configuration des graphiques en français
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

@dataclass
class PilotProfile:
    """Profil d'un pilote MotoGP avec ses caractéristiques"""
    name: str
    team: str
    # Coefficients de performance (0.8 à 1.0, 1.0 = parfait)
    corner_speed: float      # Vitesse en virage
    braking: float          # Efficacité de freinage
    acceleration: float     # Accélération
    consistency: float      # Régularité (moins de variation)
    tire_management: float  # Gestion des pneus
    risk_factor: float      # Prise de risque (plus élevé = plus rapide mais plus d'erreurs)
    experience: float       # Expérience (influence la stratégie)
    
@dataclass
class BikeSpecs:
    """Spécifications techniques d'une moto MotoGP"""
    power: float           # Puissance en kW
    mass: float           # Masse en kg
    drag_coeff: float     # Coefficient de traînée
    frontal_area: float   # Surface frontale en m²
    downforce_coeff: float # Coefficient d'appui
    tire_grip: float      # Adhérence des pneus

@dataclass
class CircuitSegment:
    """Segment de circuit"""
    type: str             # 'straight', 'corner', 'chicane'
    length: float         # Longueur en mètres
    radius: float         # Rayon pour les virages (None pour lignes droites)
    elevation: float      # Dénivelé en mètres
    difficulty: float     # Difficulté (0-1)

class MotoGPSimulator:
    def __init__(self):
        self.pilots = self._create_pilots()
        self.bikes = self._create_bikes()
        self.circuit = self._create_circuit()
        self.air_density = 1.2  # kg/m³
        self.gravity = 9.81     # m/s²
        
    def _create_pilots(self) -> List[PilotProfile]:
        """Crée les profils des pilotes MotoGP 2024-2025"""
        return [
            # Champions et top riders
            PilotProfile("Pecco Bagnaia", "Ducati", 0.95, 0.94, 0.92, 0.93, 0.95, 0.85, 0.90),
            PilotProfile("Jorge Martin", "Pramac Ducati", 0.94, 0.93, 0.95, 0.88, 0.90, 0.90, 0.85),
            PilotProfile("Marc Marquez", "Gresini Ducati", 0.98, 0.96, 0.94, 0.85, 0.88, 0.95, 0.98),
            PilotProfile("Enea Bastianini", "Ducati", 0.92, 0.91, 0.93, 0.90, 0.92, 0.88, 0.87),
            
            # Autres constructeurs - top niveau
            PilotProfile("Fabio Quartararo", "Yamaha", 0.93, 0.92, 0.89, 0.94, 0.93, 0.82, 0.92),
            PilotProfile("Brad Binder", "KTM", 0.90, 0.93, 0.91, 0.89, 0.87, 0.92, 0.88),
            PilotProfile("Pedro Acosta", "KTM", 0.91, 0.89, 0.92, 0.86, 0.85, 0.94, 0.75),
            PilotProfile("Maverick Vinales", "Aprilia", 0.91, 0.90, 0.90, 0.87, 0.89, 0.86, 0.90),
            
            # Milieu de grille
            PilotProfile("Franco Morbidelli", "Pramac Ducati", 0.89, 0.88, 0.87, 0.91, 0.90, 0.80, 0.89),
            PilotProfile("Marco Bezzecchi", "VR46 Ducati", 0.88, 0.87, 0.89, 0.85, 0.86, 0.87, 0.82),
            PilotProfile("Alex Marquez", "Gresini Ducati", 0.87, 0.86, 0.88, 0.88, 0.87, 0.83, 0.85),
            PilotProfile("Aleix Espargaro", "Aprilia", 0.89, 0.90, 0.86, 0.92, 0.91, 0.81, 0.94),
            
            # Autres pilotes
            PilotProfile("Jack Miller", "KTM", 0.86, 0.87, 0.88, 0.84, 0.85, 0.89, 0.87),
            PilotProfile("Fabio Di Giannantonio", "VR46 Ducati", 0.85, 0.84, 0.86, 0.83, 0.84, 0.86, 0.80),
            PilotProfile("Raul Fernandez", "Trackhouse Aprilia", 0.84, 0.83, 0.85, 0.82, 0.83, 0.85, 0.78),
            PilotProfile("Augusto Fernandez", "KTM", 0.83, 0.82, 0.84, 0.85, 0.84, 0.82, 0.79),
            
            # Rookies et pilotes en développement
            PilotProfile("Luca Marini", "Honda", 0.82, 0.83, 0.83, 0.86, 0.85, 0.81, 0.83),
            PilotProfile("Joan Mir", "Honda", 0.85, 0.86, 0.82, 0.89, 0.88, 0.79, 0.88),
            PilotProfile("Takaaki Nakagami", "Honda", 0.81, 0.82, 0.81, 0.84, 0.83, 0.84, 0.86),
            PilotProfile("Lorenzo Savadori", "Aprilia", 0.80, 0.81, 0.82, 0.83, 0.82, 0.87, 0.82),
        ]
    
    def _create_bikes(self) -> dict:
        """Crée les spécifications des motos par équipe"""
        return {
            "Ducati": BikeSpecs(220, 220, 0.58, 0.38, 0.08, 1.45),
            "Pramac Ducati": BikeSpecs(218, 221, 0.59, 0.38, 0.075, 1.44),
            "Gresini Ducati": BikeSpecs(217, 222, 0.60, 0.39, 0.07, 1.43),
            "VR46 Ducati": BikeSpecs(216, 223, 0.61, 0.39, 0.07, 1.42),
            "Yamaha": BikeSpecs(210, 218, 0.62, 0.40, 0.06, 1.41),
            "KTM": BikeSpecs(215, 225, 0.63, 0.41, 0.065, 1.40),
            "Aprilia": BikeSpecs(212, 219, 0.61, 0.39, 0.065, 1.42),
            "Trackhouse Aprilia": BikeSpecs(211, 220, 0.62, 0.40, 0.06, 1.41),
            "Honda": BikeSpecs(205, 224, 0.65, 0.42, 0.055, 1.38),
        }
    
    def _create_circuit(self) -> List[CircuitSegment]:
        """Crée un circuit fictif inspiré de Mugello/Silverstone"""
        return [
            CircuitSegment("straight", 1200, None, -5, 0.3),      # Ligne droite principale
            CircuitSegment("corner", 180, 120, 2, 0.7),          # Virage rapide
            CircuitSegment("straight", 800, None, 0, 0.2),        # Ligne droite moyenne
            CircuitSegment("chicane", 150, 60, 0, 0.9),          # Chicane technique
            CircuitSegment("corner", 200, 150, -3, 0.6),         # Virage moyen
            CircuitSegment("straight", 600, None, 5, 0.3),        # Montée
            CircuitSegment("corner", 220, 200, 0, 0.5),          # Virage large
            CircuitSegment("corner", 160, 80, -2, 0.8),          # Épingle
            CircuitSegment("straight", 900, None, 0, 0.2),        # Retour ligne droite
            CircuitSegment("corner", 190, 140, 0, 0.6),          # Dernier virage
        ]
    
    def calculate_segment_time(self, pilot: PilotProfile, bike: BikeSpecs, 
                             segment: CircuitSegment, entry_speed: float, 
                             tire_wear: float, lap_number: int) -> Tuple[float, float]:
        """Calcule le temps de passage sur un segment et la vitesse de sortie"""
        
        # Facteurs d'usure et de fatigue
        tire_factor = 1.0 - (tire_wear * (1.0 - pilot.tire_management) * 0.1)
        fatigue_factor = 1.0 - (lap_number * 0.001 * (1.0 - pilot.consistency))
        
        if segment.type == "straight":
            return self._calculate_straight_time(pilot, bike, segment, entry_speed, 
                                               tire_factor, fatigue_factor)
        else:
            return self._calculate_corner_time(pilot, bike, segment, entry_speed, 
                                             tire_factor, fatigue_factor)
    
    def _calculate_straight_time(self, pilot: PilotProfile, bike: BikeSpecs, 
                               segment: CircuitSegment, entry_speed: float,
                               tire_factor: float, fatigue_factor: float) -> Tuple[float, float]:
        """Calcule le temps sur une ligne droite"""
        
        # Paramètres physiques
        power = bike.power * 1000 * pilot.acceleration * tire_factor * fatigue_factor
        mass = bike.mass
        drag_area = bike.drag_coeff * bike.frontal_area
        
        # Vitesse maximale théorique
        v_max = (2 * power / (self.air_density * drag_area)) ** (1/3)
        v_max = min(v_max, 95)  # Limite réaliste ~340 km/h
        
        # Simulation numérique simple
        v = entry_speed
        distance = 0
        time = 0
        dt = 0.01
        
        while distance < segment.length:
            # Accélération due à la puissance
            power_acc = power / (mass * max(v, 10))
            
            # Décélération due à la traînée
            drag_acc = 0.5 * self.air_density * drag_area * v * v / mass
            
            # Effet de l'élévation
            elevation_acc = self.gravity * segment.elevation / segment.length
            
            # Accélération nette
            acceleration = power_acc - drag_acc - elevation_acc
            
            # Mise à jour
            v += acceleration * dt
            v = max(v, 5)  # Vitesse minimale
            distance += v * dt
            time += dt
            
            if time > 30:  # Sécurité
                break
        
        # Ajout de variabilité basée sur la prise de risque
        risk_variation = np.random.normal(0, 0.02 * pilot.risk_factor)
        time *= (1 + risk_variation)
        
        return time, v
    
    def _calculate_corner_time(self, pilot: PilotProfile, bike: BikeSpecs, 
                             segment: CircuitSegment, entry_speed: float,
                             tire_factor: float, fatigue_factor: float) -> Tuple[float, float]:
        """Calcule le temps dans un virage"""
        
        # Vitesse maximale en virage basée sur l'adhérence
        grip = bike.tire_grip * pilot.corner_speed * tire_factor * fatigue_factor
        
        # Appui aérodynamique (effet limité en MotoGP)
        downforce_effect = 1 + bike.downforce_coeff * (entry_speed ** 2) / 1000
        effective_grip = grip * downforce_effect
        
        # Vitesse maximale en virage
        if segment.radius:
            v_corner_max = np.sqrt(effective_grip * self.gravity * segment.radius)
        else:
            v_corner_max = entry_speed * 0.6  # Pour les chicanes
        
        # Vitesse d'entrée ajustée selon le freinage du pilote
        braking_efficiency = pilot.braking * tire_factor * fatigue_factor
        v_entry_adjusted = min(entry_speed, v_corner_max / braking_efficiency)
        
        # Vitesse dans le virage
        v_corner = min(v_corner_max, v_entry_adjusted)
        
        # Temps de parcours
        if segment.type == "chicane":
            # Les chicanes sont plus complexes
            time = segment.length / (v_corner * 0.8)
            exit_speed = v_corner * 0.7
        else:
            time = segment.length / v_corner
            exit_speed = v_corner * 0.9
        
        # Facteur de difficulté
        difficulty_factor = 1 + segment.difficulty * 0.1 * (1 - pilot.experience)
        time *= difficulty_factor
        
        # Variabilité basée sur la prise de risque et la régularité
        risk_variation = np.random.normal(0, 0.03 * pilot.risk_factor * (1 - pilot.consistency))
        time *= (1 + risk_variation)
        
        return time, exit_speed
    
    def simulate_lap(self, pilot: PilotProfile, lap_number: int, 
                    tire_wear: float = 0.0) -> Tuple[float, List[float]]:
        """Simule un tour complet"""
        
        bike = self.bikes[pilot.team]
        total_time = 0
        segment_times = []
        current_speed = 50  # Vitesse de départ
        
        for segment in self.circuit:
            segment_time, exit_speed = self.calculate_segment_time(
                pilot, bike, segment, current_speed, tire_wear, lap_number
            )
            
            total_time += segment_time
            segment_times.append(segment_time)
            current_speed = exit_speed
        
        return total_time, segment_times
    
    def simulate_race(self, num_laps: int = 25, show_progress: bool = True) -> pd.DataFrame:
        """Simule une course complète"""
        
        results = []
        
        for lap in range(1, num_laps + 1):
            if show_progress and lap % 5 == 0:
                print(f"Simulation du tour {lap}/{num_laps}...")
            
            # Calcul de l'usure des pneus
            tire_wear = (lap - 1) / num_laps
            
            for pilot in self.pilots:
                lap_time, segment_times = self.simulate_lap(pilot, lap, tire_wear)
                
                results.append({
                    'lap': lap,
                    'pilot': pilot.name,
                    'team': pilot.team,
                    'lap_time': lap_time,
                    'tire_wear': tire_wear,
                    'segment_times': segment_times
                })
        
        return pd.DataFrame(results)
    
    def analyze_results(self, results_df: pd.DataFrame) -> dict:
        """Analyse les résultats de la course"""
        
        # Temps cumulés
        results_df['cumulative_time'] = results_df.groupby('pilot')['lap_time'].cumsum()
        
        # Classement final
        final_results = results_df[results_df['lap'] == results_df['lap'].max()].copy()
        final_results = final_results.sort_values('cumulative_time')
        final_results['position'] = range(1, len(final_results) + 1)
        final_results['gap'] = final_results['cumulative_time'] - final_results['cumulative_time'].iloc[0]
        
        # Meilleur tour
        best_lap = results_df.loc[results_df['lap_time'].idxmin()]
        
        # Statistiques par pilote
        pilot_stats = results_df.groupby('pilot').agg({
            'lap_time': ['mean', 'std', 'min'],
            'cumulative_time': 'last'
        }).round(3)
        
        return {
            'final_classification': final_results,
            'best_lap': best_lap,
            'pilot_statistics': pilot_stats,
            'race_data': results_df
        }

# Création et lancement de la simulation
print("🏁 Simulation MotoGP - Tous les profils de pilotes")
print("=" * 50)

simulator = MotoGPSimulator()

# Affichage des pilotes
print(f"\n📋 Pilotes engagés ({len(simulator.pilots)}) :")
for i, pilot in enumerate(simulator.pilots, 1):
    print(f"{i:2d}. {pilot.name:<20} ({pilot.team})")

print(f"\n🏁 Circuit : {len(simulator.circuit)} segments, ~{sum(s.length for s in simulator.circuit)/1000:.1f} km")

# Simulation d'une course de 20 tours
print("\n🚀 Lancement de la simulation (20 tours)...")
race_results = simulator.simulate_race(num_laps=20)

print("✅ Simulation terminée ! Analyse des résultats...")
analysis = simulator.analyze_results(race_results)

# Affichage des résultats
print("\n🏆 CLASSEMENT FINAL")
print("=" * 60)

final_classification = analysis['final_classification']
for idx, row in final_classification.iterrows():
    gap_str = f"+{row['gap']:.3f}s" if row['gap'] > 0 else "---"
    print(f"{row['position']:2d}. {row['pilot']:<20} ({row['team']:<15}) {gap_str:>10}")

print(f"\n⚡ MEILLEUR TOUR")
print("=" * 40)
best_lap = analysis['best_lap']
print(f"Pilote: {best_lap['pilot']}")
print(f"Tour: {best_lap['lap']}")
print(f"Temps: {best_lap['lap_time']:.3f}s")
print(f"Équipe: {best_lap['team']}")

print(f"\n📊 STATISTIQUES GÉNÉRALES")
print("=" * 50)
race_data = analysis['race_data']
print(f"Meilleur temps de course: {race_data['lap_time'].min():.3f}s")
print(f"Temps moyen par tour: {race_data['lap_time'].mean():.3f}s")
print(f"Écart-type: {race_data['lap_time'].std():.3f}s")

# Analyse par constructeur
print(f"\n🏭 PERFORMANCE PAR CONSTRUCTEUR")
print("=" * 45)
constructor_performance = race_data.groupby('team').agg({
    'lap_time': ['mean', 'min', 'count']
}).round(3)

constructor_avg = race_data.groupby('team')['lap_time'].mean().sort_values()
for team, avg_time in constructor_avg.items():
    pilot_count = race_data[race_data['team'] == team]['pilot'].nunique()
    print(f"{team:<20}: {avg_time:.3f}s (moy.) - {pilot_count} pilote(s)")

print(f"\n📈 ÉVOLUTION DES PERFORMANCES")
print("=" * 40)
# Comparaison premier vs dernier tour
first_lap_avg = race_data[race_data['lap'] == 1]['lap_time'].mean()
last_lap_avg = race_data[race_data['lap'] == 20]['lap_time'].mean()
degradation = last_lap_avg - first_lap_avg

print(f"Temps moyen tour 1: {first_lap_avg:.3f}s")
print(f"Temps moyen tour 20: {last_lap_avg:.3f}s")
print(f"Dégradation: {degradation:.3f}s ({degradation/first_lap_avg*100:.1f}%)")

# Création des graphiques d'analyse
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('🏁 Analyse de la Course MotoGP - Simulation Complète', fontsize=16, fontweight='bold')

# 1. Évolution des temps au tour pour le top 6
ax1 = axes[0, 0]
top_6_pilots = final_classification.head(6)['pilot'].tolist()
colors = ['#FF0000', '#00FF00', '#0000FF', '#FF8000', '#8000FF', '#00FFFF']

for i, pilot in enumerate(top_6_pilots):
    pilot_data = race_data[race_data['pilot'] == pilot]
    ax1.plot(pilot_data['lap'], pilot_data['lap_time'], 
             marker='o', linewidth=2, markersize=4, 
             label=pilot, color=colors[i])

ax1.set_xlabel('Tour')
ax1.set_ylabel('Temps au tour (s)')
ax1.set_title('Évolution des temps - Top 6')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)

# 2. Classement cumulé (positions)
ax2 = axes[0, 1]
# Calcul des positions à chaque tour
positions_data = []
for lap in range(1, 21):
    lap_data = race_data[race_data['lap'] == lap].copy()
    lap_data = lap_data.sort_values('cumulative_time')
    lap_data['position'] = range(1, len(lap_data) + 1)
    positions_data.append(lap_data)

positions_df = pd.concat(positions_data)

for i, pilot in enumerate(top_6_pilots):
    pilot_positions = positions_df[positions_df['pilot'] == pilot]
    ax2.plot(pilot_positions['lap'], pilot_positions['position'], 
             marker='s', linewidth=2, markersize=4,
             label=pilot, color=colors[i])

ax2.set_xlabel('Tour')
ax2.set_ylabel('Position')
ax2.set_title('Évolution des positions - Top 6')
ax2.invert_yaxis()  # Position 1 en haut
ax2.set_yticks(range(1, 21))
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True, alpha=0.3)

# 3. Performance par constructeur (boxplot)
ax3 = axes[1, 0]
teams = race_data['team'].unique()
team_times = [race_data[race_data['team'] == team]['lap_time'].values for team in teams]

bp = ax3.boxplot(team_times, labels=teams, patch_artist=True)
colors_box = plt.cm.Set3(np.linspace(0, 1, len(teams)))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)

ax3.set_ylabel('Temps au tour (s)')
ax3.set_title('Distribution des temps par constructeur')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)

# 4. Écarts au leader par tour
ax4 = axes[1, 1]
leader_times = race_data[race_data['pilot'] == 'Pecco Bagnaia']['cumulative_time'].values

for i, pilot in enumerate(top_6_pilots[1:], 1):  # Exclure le leader
    pilot_data = race_data[race_data['pilot'] == pilot]
    gaps = pilot_data['cumulative_time'].values - leader_times
    ax4.plot(pilot_data['lap'], gaps, 
             marker='o', linewidth=2, markersize=4,
             label=pilot, color=colors[i])

ax4.set_xlabel('Tour')
ax4.set_ylabel('Écart au leader (s)')
ax4.set_title('Évolution des écarts au leader')
ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Graphique supplémentaire : Heatmap des performances
fig2, ax = plt.subplots(1, 1, figsize=(14, 10))

# Préparation des données pour la heatmap
pivot_data = race_data.pivot(index='pilot', columns='lap', values='lap_time')
pivot_data = pivot_data.reindex(final_classification['pilot'])  # Ordonner par classement final

# Création de la heatmap
im = ax.imshow(pivot_data.values, cmap='RdYlGn_r', aspect='auto')

# Configuration des axes
ax.set_xticks(range(len(pivot_data.columns)))
ax.set_xticklabels(pivot_data.columns)
ax.set_yticks(range(len(pivot_data.index)))
ax.set_yticklabels(pivot_data.index)

# Rotation des labels
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
plt.setp(ax.get_yticklabels(), rotation=0, ha="right")

# Titre et labels
ax.set_xlabel('Tour')
ax.set_ylabel('Pilote (classé par position finale)')
ax.set_title('Heatmap des temps au tour - Plus foncé = Plus rapide', pad=20)

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Temps au tour (s)', rotation=270, labelpad=20)

plt.tight_layout()
plt.show()

# Analyse détaillée des profils de pilotes
print("\n🔍 ANALYSE DÉTAILLÉE DES PROFILS DE PILOTES")
print("=" * 60)

# Analyse des caractéristiques vs performance
pilot_analysis = []
for pilot in simulator.pilots:
    pilot_race_data = race_data[race_data['pilot'] == pilot.name]
    avg_time = pilot_race_data['lap_time'].mean()
    consistency_race = pilot_race_data['lap_time'].std()
    final_pos = final_classification[final_classification['pilot'] == pilot.name]['position'].iloc[0]
    
    pilot_analysis.append({
        'pilot': pilot.name,
        'team': pilot.team,
        'avg_time': avg_time,
        'consistency_race': consistency_race,
        'final_position': final_pos,
        'corner_speed': pilot.corner_speed,
        'braking': pilot.braking,
        'acceleration': pilot.acceleration,
        'consistency_profile': pilot.consistency,
        'tire_management': pilot.tire_management,
        'risk_factor': pilot.risk_factor,
        'experience': pilot.experience
    })

pilot_df = pd.DataFrame(pilot_analysis)

# Top 5 dans chaque catégorie
print("\n🏆 TOP 5 PAR CATÉGORIE DE COMPÉTENCE")
print("-" * 50)

categories = [
    ('Vitesse en virage', 'corner_speed'),
    ('Freinage', 'braking'), 
    ('Accélération', 'acceleration'),
    ('Régularité', 'consistency_profile'),
    ('Gestion pneus', 'tire_management'),
    ('Expérience', 'experience')
]

for cat_name, cat_col in categories:
    print(f"\n{cat_name}:")
    top_5 = pilot_df.nlargest(5, cat_col)[['pilot', cat_col]]
    for idx, row in top_5.iterrows():
        print(f"  {row[cat_col]:.3f} - {row['pilot']}")

# Corrélations entre profil et performance
print(f"\n📊 CORRÉLATIONS PROFIL vs PERFORMANCE")
print("-" * 45)

correlations = {}
performance_cols = ['avg_time', 'final_position']
skill_cols = ['corner_speed', 'braking', 'acceleration', 'consistency_profile', 
              'tire_management', 'risk_factor', 'experience']

for perf_col in performance_cols:
    print(f"\nCorrélations avec {perf_col.replace('_', ' ')}:")
    for skill_col in skill_cols:
        corr = pilot_df[skill_col].corr(pilot_df[perf_col])
        correlations[f"{skill_col}_vs_{perf_col}"] = corr
        direction = "↓" if corr < 0 else "↑"
        strength = "forte" if abs(corr) > 0.5 else "modérée" if abs(corr) > 0.3 else "faible"
        print(f"  {skill_col.replace('_', ' '):<15}: {corr:+.3f} {direction} ({strength})")

print(f"\n🎯 ANALYSE DES ÉCARTS DE PERFORMANCE")
print("-" * 45)

# Écart entre le meilleur et le moins bon
best_time = pilot_df['avg_time'].min()
worst_time = pilot_df['avg_time'].max()
time_gap = worst_time - best_time

print(f"Meilleur temps moyen: {best_time:.3f}s")
print(f"Moins bon temps moyen: {worst_time:.3f}s")
print(f"Écart total: {time_gap:.3f}s ({time_gap/best_time*100:.1f}%)")

# Groupes de performance
print(f"\n🏁 GROUPES DE PERFORMANCE")
print("-" * 30)

# Définition des groupes basés sur les positions finales
group1 = pilot_df[pilot_df['final_position'] <= 5]
group2 = pilot_df[(pilot_df['final_position'] > 5) & (pilot_df['final_position'] <= 10)]
group3 = pilot_df[(pilot_df['final_position'] > 10) & (pilot_df['final_position'] <= 15)]
group4 = pilot_df[pilot_df['final_position'] > 15]

groups = [
    ("Groupe Elite (Top 5)", group1),
    ("Groupe Milieu+ (6-10)", group2), 
    ("Groupe Milieu- (11-15)", group3),
    ("Groupe Queue (16-20)", group4)
]

for group_name, group_data in groups:
    if len(group_data) > 0:
        print(f"\n{group_name}:")
        avg_skills = group_data[skill_cols].mean()
        for skill in skill_cols:
            print(f"  {skill.replace('_', ' '):<15}: {avg_skills[skill]:.3f}")

# Sauvegarde des résultats détaillés
pilot_df.to_csv('/home/user/motogp_simulation_results.csv', index=False)
race_data.to_csv('/home/user/motogp_race_data.csv', index=False)

print(f"\n💾 Résultats sauvegardés:")
print(f"  - Analyse pilotes: /home/user/motogp_simulation_results.csv")
print(f"  - Données de course: /home/user/motogp_race_data.csv")
