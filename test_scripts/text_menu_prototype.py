def text_based_menu():
    print("Welcome to Jarvis!")
    print("1. Text-based interaction")
    print("2. Voice-based interaction")
    print("3. Wake word detection")
    print("4. Exit")
    
    while True:
        choice = input("Select an option (1, 2, 3, 4): ")
    
        if choice == "1":
            from backend.brain import interaction_loop
            interaction_loop(False)
    
        elif choice == "2":
            from backend.brain import interaction_loop
            interaction_loop(True)
        elif choice == "3":
            # For wake word detection, you would implement a continuous listening loop that triggers the interaction_loop when the wake word is detected.
            print("Wake word detection is not implemented yet.")
        elif choice == "4":
            print("Exiting AI Assistant. Goodbye!")
            exit()
    
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")