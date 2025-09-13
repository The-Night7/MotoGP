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
                # Augmenter le taux d'abandon pour plus de réalisme
                dnf_chance = pilot.raw_data.get("dnf_rate", 0.2)
                if random.random() < dnf_chance:
                    dnf_pilots.append(pilot.name)
                    # Déterminer le tour d'abandon (plus probable en début ou fin de course)
                    lap_distribution = [1] * 3 + [i for i in range(2, race_laps-1)] + [race_laps-1] * 2
                    dnf_laps[pilot.name] = random.choice(lap_distribution)
        
        # Simuler chaque tour
        positions = {row["name"]: idx + 1 for idx, row in grid.iterrows()}
        cumulative_times = {row["name"]: 0 for _, row in grid.iterrows()}
        
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
                
                # Facteur de fatigue du pilote (augmente la variabilité en fin de course)
                fatigue_factor = 1 + (lap / race_laps) * 0.05 * (1 - pilot.consistency)
                
                # Variabilité (plus grande pour créer des écarts plus réalistes)
                variability = random.uniform(-0.04, 0.04) * fatigue_factor
                
                # Incidents aléatoires (erreurs, dépassements ratés, etc.)
                incident_chance = 0.05 * (1 - pilot.consistency)
                if random.random() < incident_chance:
                    # Petite erreur qui coûte du temps
                    variability += random.uniform(0.02, 0.08)
                
                # Temps au tour
                lap_time = (100 - performance * 20) * position_factor * tire_factor * (1 + variability) * weather_factor
                
                # Enregistrer le temps au tour
                lap_times[pilot_name] = lap_time
                cumulative_times[pilot_name] += lap_time
                
                # Ajouter aux données de course
                race_data.append({
                    "lap": lap,
                    "name": pilot_name,
                    "team": pilot.team,
                    "position": current_position,
                    "lap_time": lap_time,
                    "cumulative_time": cumulative_times[pilot_name],
                    "status": "Running"
                })
            
            # Mettre à jour les positions pour le prochain tour (sauf au dernier tour)
            if lap < race_laps:
                # Trier les pilotes par temps cumulé
                active_pilots = [p for p in positions.keys() if p not in dnf_pilots or dnf_laps[p] >= lap]
                active_pilots.sort(key=lambda p: cumulative_times.get(p, float('inf')))
                
                # Mettre à jour les positions
                for pos, pilot_name in enumerate(active_pilots, 1):
                    positions[pilot_name] = pos
            
            # Ajouter les DNF pour ce tour
            for pilot_name in dnf_pilots:
                if dnf_laps[pilot_name] == lap:
                    pilot = next((p for p in self.pilots if p.name == pilot_name), None)
                    if pilot:
                        # Déterminer la cause de l'abandon
                        dnf_causes = ["Accident", "Chute", "Problème technique", "Problème moteur", 
                                     "Pneus", "Électronique", "Collision"]
                        dnf_cause = random.choice(dnf_causes)
                        
                        race_data.append({
                            "lap": lap,
                            "name": pilot_name,
                            "team": pilot.team,
                            "position": None,
                            "lap_time": None,
                            "cumulative_time": cumulative_times.get(pilot_name, 0),
                            "status": f"DNF - {dnf_cause}"
                        })
        
        # Convertir en DataFrame
        race_df = pd.DataFrame(race_data)
        
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
            
            # Calculer l'écart avec le leader pour les pilotes qui terminent
            gap_to_leader = None
            if status == "Running" and position > 1:
                # Trouver le temps du leader au dernier tour
                leader_data = race_df[(race_df["lap"] == max_lap) & (race_df["position"] == 1)]
                if not leader_data.empty:
                    leader_time = leader_data.iloc[0]["cumulative_time"]
                    gap_to_leader = last_lap_data["cumulative_time"] - leader_time
            
            final_results.append({
                "name": pilot_name,
                "team": last_lap_data["team"],
                "final_position": int(position) if position and not pd.isna(position) else None,
                "qualifying_position": int(quali_position) if not pd.isna(quali_position) else None,
                "status": status,
                "points": int(points) if not pd.isna(points) else 0,
                "laps_completed": int(max_lap) if not pd.isna(max_lap) else 0,
                "gap_to_leader": float(gap_to_leader) if gap_to_leader is not None else None
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
            "dnf_rate": float(len(dnf_results) / len(final_results)) if final_results else 0,
            "finishers_count": len(running_results),
            "avg_gap": float(np.mean([r["gap_to_leader"] for r in running_results if r["gap_to_leader"] is not None]))
                      if running_results else None
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
            ax4.boxplot(team_lap_times, labels=team_labels)
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