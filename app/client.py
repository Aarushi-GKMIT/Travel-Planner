from agents.orchestrator.graph import orchestrator_graph

def main():
    while True:
        query = input("\nEnter your travel query (type exit to quit): ")
        if query.lower() == "exit":
            break
        
        result = orchestrator_graph.invoke({
            "user_query": query
        })

        print("res: ", result)

        print("\nLLM Response:\n", result['answer'])

if __name__ == "__main__":
    main()
