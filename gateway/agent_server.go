package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// TelemetryData defines the structure of incoming simulation metrics from Python
type TelemetryData struct {
	Step      int     `json:"step"`
	AgentID   int     `json:"agent_id"`
	Energy    float64 `json:"energy"`
	Strategy  string  `json:"strategy"`
	XPosition float64 `json:"x"`
	YPosition float64 `json:"y"`
}

func telemetryHandler(w http.ResponseWriter, r *http.Request) {
	// Hume sirf POST requests chahiye kyunki Python data bhejega
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST requests are allowed", http.StatusMethodNotAllowed)
		return
	}

	var data TelemetryData
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Microsecond high-throughput processing logs
	fmt.Printf("[TELEMETRY] Step: %d | Agent: %d | Energy: %.2f | Strategy: %s | Pos: (%.2f, %.2f)\n",
		data.Step, data.AgentID, data.Energy, data.Strategy, data.XPosition, data.YPosition)

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status": "received"}`))
}

func main() {
	http.HandleFunc("/telemetry", telemetryHandler)
	port := ":8080"
	fmt.Printf("[+] Go Telemetry Gateway listening on http://localhost%s...\n", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
