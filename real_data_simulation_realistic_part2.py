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