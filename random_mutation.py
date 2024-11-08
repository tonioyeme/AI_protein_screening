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

# Function to generate all single mutations for each position
def generate_all_single_mutations(sequence, num_mutations):
    mutated_sequences = set()
    for _ in range(num_mutations):
        for pos in range(len(sequence)):
            mutated_sequence = mutate_sequence_once(sequence, pos)
            mutated_sequences.add(mutated_sequence)
    return list(mutated_sequences)

# Main function to process multiple protein chains
def main(input_file, output_file):
    try:
        # Attempt to open and load input JSON file
        with open(input_file, "r") as file:
            data = json.load(file)
            print("Input data loaded successfully:", data)  # Debugging line

        results = []

        for protein in data.get("proteinChains", []):
            name = protein.get("name")
            original_sequence = protein.get("sequence")
            num_mutations = protein.get("mutation", 1)

            # Check for required fields
            if not name or not original_sequence:
                print(f"Skipping entry with missing name or sequence: {protein}")
                continue
            if not isinstance(num_mutations, int) or num_mutations <= 0:
                print(f"Invalid mutation count for {name}. Skipping.")
                continue

            # Generate mutated sequences
            mutated_sequences = generate_all_single_mutations(original_sequence, num_mutations)
            print(f"Mutated sequences for {name}: {len(mutated_sequences)} generated")  # Debugging line
            
            # Add results for this protein
            results.append({
                "name": name,
                "original_sequence": original_sequence,
                "num_mutations": num_mutations,
                "mutated_sequences": mutated_sequences
            })

        # Write all results to the output JSON file
        with open(output_file, "w") as file:
            json.dump({"proteinChains": results}, file, indent=4)
            print(f"Output successfully written to {output_file}")  # Debugging line

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Input file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

input_file = "input.json"
output_file = "output.json"
main(input_file, output_file)