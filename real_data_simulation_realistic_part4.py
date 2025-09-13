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
    
    def format_time_gap(self, seconds: float) -> str:
        """Formate un écart de temps en format lisible"""
        if seconds is None:
            return ""
        
        if seconds < 0.1:
            return f"{seconds:.3f}s"
        elif seconds < 60:
            return f"+{seconds:.3f}s"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"+{minutes}m {remaining_seconds:.3f}s"
    
    def run_complete_simulation(self, circuit_name: str, weather_condition: str = "dry") -> Dict:
        """Exécute une simulation complète: qualification + course + analyse"""
        print(f"\n🏁 Simulation MotoGP - {circuit_name} ({weather_condition})")
        print("=" * 60)
        
        # 1. Qualification
        print("\nSimulation des qualifications...")
        qualifying_results = self.simulate_qualifying(circuit_name, weather_condition)
        
        print("\n📋 Résultats des qualifications (Top 10):")
        for _, row in qualifying_results.head(10).iterrows():
            print(f"{int(row['position']):2d}. {row['name']:<20} - {row['lap_time']:.3f}s")
        
        # 2. Course
        print("\nSimulation de la course...")
        race_results_df = self.simulate_race(circuit_name, qualifying_results, weather_condition)
        
        # 3. Analyse
        print("\nAnalyse des résultats...")
        race_analysis = self.analyze_race_results(race_results_df, qualifying_results)
        
        # 4. Affichage des résultats
        print("\n🏆 CLASSEMENT FINAL")
        print("=" * 60)
        
        for result in race_analysis["final_classification"]:
            if result["status"] == "Running":
                position = result["final_position"]
                quali_pos = result["qualifying_position"]
                gap = self.format_time_gap(result["gap_to_leader"]) if result["gap_to_leader"] is not None else ""
                print(f"{position:2d}. {result['name']:<20} - {result['points']} pts {gap:<10} (Q: {quali_pos})")
            else:
                quali_pos = result["qualifying_position"]
                laps = result["laps_completed"]
                print(f"DNF. {result['name']:<20} - {result['status']} (Q: {quali_pos}, Tours: {laps})")
        
        if race_analysis["best_lap"]:
            print(f"\n⚡ MEILLEUR TOUR: {race_analysis['best_lap']['name']} - "
                 f"Tour {race_analysis['best_lap']['lap']} - "
                 f"{race_analysis['best_lap']['time']:.3f}s")
        
        # 5. Visualisation
        print("\nGénération des graphiques d'analyse...")
        self.visualize_race_analysis(race_analysis, circuit_name, weather_condition)
        
        # 6. Sauvegarde des résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{self.data_dir}/race_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            # Convertir DataFrame en liste pour la sérialisation JSON
            serializable_race_analysis = self._convert_to_serializable(race_analysis)
            json.dump(serializable_race_analysis, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Résultats sauvegardés dans {results_file}")
        
        return race_analysis

# Exécution du programme principal
if __name__ == "__main__":
    print("🏍️ MotoGP - Simulateur basé sur des données réelles")
    print("=" * 50)
    
    # Créer le simulateur
    simulator = MotoGPRealDataSimulator()
    
    # Afficher les pilotes disponibles
    print(f"\n📋 Pilotes ({len(simulator.pilots)}):")
    for i, pilot in enumerate(simulator.pilots, 1):
        print(f"{i:2d}. {pilot.name:<20} ({pilot.team})")
    
    # Afficher les circuits disponibles
    print(f"\n🏁 Circuits ({len(simulator.circuits)}):")
    for i, circuit in enumerate(simulator.circuits, 1):
        print(f"{i:2d}. {circuit.name:<30} ({circuit.country})")
    
    # Analyse des pilotes par clusters de performance
    print("\n🔍 Analyse des groupes de performance:")
    clusters = simulator.cluster_pilots_by_performance()
    
    for cluster_id, pilots in clusters.items():
        if pilots:
            avg_pace = sum(p["race_pace"] for p in pilots) / len(pilots)
            print(f"\nGroupe {cluster_id+1} (Niveau de performance: {avg_pace:.2f}):")
            for pilot in pilots:
                print(f"  - {pilot['name']:<20} ({pilot['team']}) - Victoires: {pilot['career_wins']}")
    
    # Simulation d'une course complète
    print("\n🚀 Lancement d'une simulation complète...")
    race_analysis = simulator.run_complete_simulation("Mugello Circuit", "dry")
    
    print("\n✅ Simulation terminée!")