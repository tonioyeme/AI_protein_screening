import random
import json

# List of all amino acids
amino_acids = "ACDEFGHIKLMNPQRSTVWY"

# Function to generate a single mutation
def mutate_sequence_once(sequence, pos):
    sequence = list(sequence)
    current_aa = sequence[pos]
    new_aa = random.choice(amino_acids)
    while new_aa == current_aa:
        new_aa = random.choice(amino_acids)
    sequence[pos] = new_aa
    return "".join(sequence)

# Function to generate all single mutations
def generate_all_single_mutations(sequence, num_mutations):
    mutated_sequences = set()
    for _ in range(num_mutations):
        for pos in range(len(sequence)):
            mutated_sequence = mutate_sequence_once(sequence, pos)
            mutated_sequences.add(mutated_sequence)
    return list(mutated_sequences)

# Main function to read input, perform mutations, and write output
def main(input_file, output_file):
    try:
        with open(input_file, "r") as file:
            data = json.load(file)

        print("Loaded input data")

        # Accessing nested format in 'proteinChain'
        original_sequence = data.get("proteinChain", {}).get("sequence")
        num_mutations = data.get("proteinChain", {}).get("mutation", 1)

        if original_sequence is None:
            raise ValueError("Error: 'sequence' is missing in input file under 'proteinChain'.")
        if not isinstance(num_mutations, int) or num_mutations <= 0:
            raise ValueError("Error: 'mutation' must be a positive integer.")

        # Generate mutated sequences
        mutated_sequences = generate_all_single_mutations(original_sequence, num_mutations)
        
        output_data = {
            "proteinChain": {
                "original_sequence": original_sequence,
                "num_mutations": num_mutations,
                "mutated_sequences": mutated_sequences
            }
        }

        with open(output_file, "w") as file:
            json.dump(output_data, file, indent=4)

        print(f"Generated {len(mutated_sequences)} mutated sequences and saved to {output_file}")

    except json.JSONDecodeError:
        print("Error: Input file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = "input.json"
output_file = "output.json"
main(input_file, output_file)
