# Cognitive Multi-Agent Simulator Automation Toolkit

.PHONY: init build-backend run-gateway run-simulation clean help

help:
	@echo "Available commands:"
	@echo "  make init           - Install Python dependencies"
	@echo "  make build-backend  - Compile the high-speed C++ Environment Engine"
	@echo "  make run-gateway    - Start the Golang telemetry server"
	@echo "  make run-sim        - Run the PyTorch Cognitive Training loop"
	@echo "  make clean          - Clean compiled build binaries"

init:
	pip install -r requirements.txt || pip install torch numpy gymnasium pybind11 requests

build-backend:
	python setup.py build_ext --inplace

run-gateway:
	cd gateway && go run agent_server.go

run-sim:
	python train.py

clean:
	rm -rf build/ *.so *.pyd gateway/agent_server
