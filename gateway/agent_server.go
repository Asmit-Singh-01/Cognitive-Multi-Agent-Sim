package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
)

// AgentState defines the data we track for cognitive analysis
type AgentState struct {
	AgentID   int       `json:"agent_id"`
	Position  []float64 `json:"position"`
	Action    int       `json:"action"`
	Cognitive float64   `json:"cognitive_bias_level"`
}

var (
	stateStore = make(map[int]AgentState)
	mutex      sync.Mutex
)

// updateState handles incoming data from the Python/C++ engine
func updateState(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var state AgentState
	err := json.NewDecoder(r.Body).Decode(&state)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	mutex.Lock()
	stateStore[state.AgentID] = state
	mutex.Unlock()

	fmt.Printf("[GO SERVER] Updated Agent %d State (Bias Level: %.2f)\n", state.AgentID, state.Cognitive)
	w.WriteHeader(http.StatusOK)
}

// getState allows visualization tools or monitoring dashboards to fetch current environment state
func getState(w http.ResponseWriter, r *http.Request) {
	mutex.Lock()
	defer mutex.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(stateStore)
}

func main() {
	http.HandleFunc("/update", updateState)
	http.HandleFunc("/state", getState)

	fmt.Println("🚀 Go Agent Gateway running on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

