class HeaterAgent:
    def __init__(self):
        self.previous_action = "OFF"   # initial state

    def decide(self, temperature):
        print(f"\nCurrent Temperature: {temperature}°C")
        
        # Rule 1: Too Cold
        if temperature < 18:
            if self.previous_action != "ON":
                self.previous_action = "ON"
                print("Action: Turning Heater ON")
            else:
                print("Action: Heater already ON (No change)")

        # Rule 2: Too Hot
        elif temperature > 24:
            if self.previous_action != "OFF":
                self.previous_action = "OFF"
                print("Action: Turning Heater OFF")
            else:
                print("Action: Heater already OFF (No change)")

        # Rule 3: Comfortable Range
        else:
            print(f"Action: Keeping Heater {self.previous_action}")

# ----------------------------
# Testing the Agent
# ----------------------------

agent = HeaterAgent()

temperatures = [16, 17, 20, 25, 23, 15, 15]

for temp in temperatures:
    agent.decide(temp)